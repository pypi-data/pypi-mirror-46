import os
import sys
import copy
import h5py
import traceback
import argparse
import numpy as np
from glob import glob
import pickle
import keras as ks
import keras.backend as K

# Internal imports
from .utils import save_dict, query_yes_no, drop_key, boolify
from .model_components import get_loss_function, get_optimizer, upsample_img
from .submodels import get_time_net, get_cnn, get_top, get_scalar_net, get_track_net, get_FiLM_generator
from .data_generator import DataGenerator
from .callbacks import LRFinder, CyclicLR, SGDRScheduler, ModelCheckpoint


class ModelContainer:
    """
    A class for organizing the creation, training and evaluation of models.

    Please see the [README](https://gitlab.com/ffaye/deepcalo/blob/master/README.md)
    for documentation.
    """

    def __init__(self, data, params, dirs, save_figs=True, verbose=True):
        self.data = data
        self.params = params
        self.dirs = dirs
        self.save_figs = save_figs
        self.verbose = verbose

        # Load specific layers of previously trained model
        if self.params['pretrained_model']['use']:
            self._collect_pretrained_weights(**drop_key(self.params['pretrained_model'],'use'))

        # Create model
        self.model = self.get_model(self.params)

        # Plot the models
        try:
            if save_figs:
                self._plot_models()
        except Exception:
            if self.verbose:
                print('Plot of model failed. Continuing. '
                      'Here is the traceback:\n')
                traceback.print_exc()


    def get_model(self, params):

        # Inputs
        inputs = {}

        # Images
        self._non_time_img_names = []
        if 'images' in self.data['train'] and boolify(self.data['train']['images']):
            for img_name in self.data['train']['images']:
                inputs[img_name] = ks.layers.Input(shape=self.data['train']['images'][img_name].shape[1:], name=img_name)
                if not img_name.startswith('time'):
                    self._non_time_img_names.append(img_name)

        # Scalars
        if 'scalars' in self.data['train'] and boolify(self.data['train']['scalars']):
            inputs['scalars'] = ks.layers.Input(shape=self.data['train']['scalars'].shape[1:], name='scalars')

        # Tracks
        if 'tracks' in self.data['train'] and boolify(self.data['train']['tracks']):
            inputs['tracks'] = ks.layers.Input(shape=self.data['train']['tracks'].shape[1:], name='tracks')

        # Make copy that can be overwritten, such that inputs are not
        tns_branches = {name:inputs[name] for name in inputs}

        # Create submodels and connect them
        # ----------------------------------------------------------------------
        # Scalar net
        # ----------------------------------------------------------------------
        if 'scalars' in self.data['train'] and boolify(self.data['train']['scalars']):
            # Get scalar network
            self.scalar_net = get_scalar_net(input_shape=tns_branches['scalars']._keras_shape[1:],
                                             **drop_key(params['scalar_net'],'connect_to'))

            # Apply scalar network
            tns_branches['scalars'] = self.scalar_net(tns_branches['scalars'])

        # ----------------------------------------------------------------------
        # Track net
        # ----------------------------------------------------------------------
        if 'tracks' in self.data['train'] and boolify(self.data['train']['tracks']):
            # Get track network
            self.track_net = get_track_net(input_shape=tns_branches['tracks']._keras_shape[1:],
                                           **drop_key(params['track_net'],'connect_to'))

            # Apply track network
            tns_branches['tracks'] = self.track_net(tns_branches['tracks'])

        if 'images' in self.data['train'] and boolify(self.data['train']['images']):
            # ------------------------------------------------------------------
            # Time net
            # ------------------------------------------------------------------
            if any(img_name.startswith('time') for img_name in self.data['train']['images']):
                # Get gate
                self.time_net = get_time_net(**drop_key(params['time_net'],'merge_method'))

                # Apply time net to non-time images
                for img_name in self._non_time_img_names:
                    tns_branches[img_name] = self._apply_time_net(tns_branches[img_name], tns_branches[f'time_{img_name}'],
                                                                  merge_method=params['time_net']['merge_method'])

            # ------------------------------------------------------------------
            # Upsampling (do as late in the chain as possible, to save computation)
            # ------------------------------------------------------------------
            if params['upsampling']['use']:
                wanted_height, wanted_width = params['upsampling']['wanted_size']

                # Determine upsampling size for each non-time image
                for img_name in self._non_time_img_names:
                    shape = tns_branches[img_name]._keras_shape
                    size = (int(np.max((1,np.round(wanted_height/shape[1])))), int(np.max((1,np.round(wanted_width/shape[2])))))

                    # Upsample with found size
                    tns_branches[img_name] = upsample_img(tns_branches[img_name], normalize=True, size=size,
                                                          **drop_key(params['upsampling'],['use','wanted_size']))

            # Concatenate images into a single tensor before passing it to the CNN
            img = [tns_branches[img_name] for img_name in self._non_time_img_names]
            img = self._unpack_tns_list(img)

            # ------------------------------------------------------------------
            # FiLM generator
            # ------------------------------------------------------------------
            if params['FiLM_gen']['use']:
                # Prepare input
                FiLM_gen_input = []

                # Scalars
                if 'scalars' in self.data['train'] and boolify(self.data['train']['scalars']) and 'FiLM_gen' in params['scalar_net']['connect_to']:
                    FiLM_gen_input.append(tns_branches['scalars'])

                # Tracks
                if 'tracks' in self.data['train'] and boolify(self.data['train']['tracks']) and 'FiLM_gen' in params['track_net']['connect_to']:
                    FiLM_gen_input.append(tns_branches['tracks'])

                # Concatenate inputs into a single tensor before passing it to the FiLM generator
                FiLM_gen_input = self._unpack_tns_list(FiLM_gen_input)

                # Get FiLM generator
                self.FiLM_gen = get_FiLM_generator(FiLM_gen_input._keras_shape[1:],
                                                   n_blocks=len(params['cnn']['block_depths']),
                                                   n_init_filters=params['cnn']['n_init_filters'],
                                                   **drop_key(params['FiLM_gen'],'use'))

                # Apply FiLM generator
                FiLM_gen_output_list = self.FiLM_gen(FiLM_gen_input)

            # ------------------------------------------------------------------
            # CNN
            # ------------------------------------------------------------------
            if 'images' in self.data['train'] and boolify(self.data['train']['images']):
                # Get CNN
                self.cnn = get_cnn(input_shape=img._keras_shape[1:],
                                   FiLM_input_shapes=([out._keras_shape[1:] for out in FiLM_gen_output_list] if params['FiLM_gen']['use'] else None),
                                   **params['cnn'])

                # Apply CNN
                cnn_output = self.cnn((img if not params['FiLM_gen']['use'] else [img] + FiLM_gen_output_list))

                # --------------------------------------------------------------
                # Collect CNN model that includes the upsampling
                # --------------------------------------------------------------
                # Collect image inputs
                inputs_cnn_with_upsampling = []

                # Images
                for img_name in self.data['train']['images']:
                    inputs_cnn_with_upsampling.append(inputs[img_name])

                if params['FiLM_gen']['use']:
                    # If scalar net connect_to FiLM
                    inputs_cnn_with_upsampling.append(inputs['scalars'])

                    # If track net connect_to FiLM
                if 'tracks' in self.data['train'] and boolify(self.data['train']['tracks']):
                    inputs_cnn_with_upsampling.append(inputs['tracks'])

                self.cnn_with_upsampling = ks.models.Model(inputs=inputs_cnn_with_upsampling, outputs=cnn_output)

        # ----------------------------------------------------------------------
        # Top
        # ----------------------------------------------------------------------
        # Prepare input
        top_input = []

        # Add CNN output
        if 'images' in self.data['train'] and boolify(self.data['train']['images']):
            top_input.append(cnn_output)

        # Add scalars
        if 'scalars' in self.data['train'] and boolify(self.data['train']['scalars']) and 'top' in params['scalar_net']['connect_to']:
            top_input.append(tns_branches['scalars'])

        # Add tracks
        if 'tracks' in self.data['train'] and boolify(self.data['train']['tracks']) and 'top' in params['track_net']['connect_to']:
            top_input.append(tns_branches['tracks'])

        # Concatenate inputs into a single tensor before passing it to the top
        top_input = self._unpack_tns_list(top_input)

        # Get top
        self.top = get_top(input_shape=top_input._keras_shape[1:], **params['top'])

        # Apply top
        output = self.top(top_input)

        # ----------------------------------------------------------------------
        # Full model
        # ----------------------------------------------------------------------
        # Make the full model
        model = ks.models.Model(inputs=[inputs[name] for name in inputs], outputs=output)

        # Load pretrained weights
        if params['pretrained_model']['use']:
            # Set the pretrained weights
            for name in params['pretrained_model']['layers_to_load']:
                model.get_layer(name).set_weights(self.pretrained_weights[name])
                if self.verbose:
                    print(f'Loaded pretrained weights for layer with name {name} into current model.')

            # Freeze the set layers
            if type(params['pretrained_model']['freeze_loaded_layers']) == bool:
                if params['pretrained_model']['freeze_loaded_layers']:
                    for name in params['pretrained_model']['layers_to_load']:
                        model.get_layer(name).trainable = False
                        if self.verbose:
                            print(f'Froze layer with name {name}.')

            else: # 'freeze_loaded_layers' should be a list of booleans of same length as 'layers_to_load'
                assert(len(params['pretrained_model']['layers_to_load'])==len(params['pretrained_model']['freeze_loaded_layers']))
                for name,freeze in zip(params['pretrained_model']['layers_to_load'],params['pretrained_model']['freeze_loaded_layers']):
                    model.get_layer(name).trainable = not freeze
                    if self.verbose and freeze:
                        print(f'Froze layer with name {name}.')

        if self.verbose:
            model.summary()

        # Distribute batch across n_gpus if n > 1
        if self.params['n_gpus'] > 1:
            model = ks.utils.multi_gpu_model(model, gpus=self.params['n_gpus'])

        # Choose weighted or unweighted metric kwargs, depending on use of sample_weights
        if params['metrics'] is not None:
            metrics = [get_loss_function(name) for name in params['metrics']]
            if 'sample_weights' in self.data['train'] and boolify(self.data['train']['sample_weights']):
                metrics_kwargs = {'weighted_metrics':metrics}
            else:
                metrics_kwargs = {'metrics':metrics}
        else:
            metrics_kwargs = {}

        # Compile
        model.compile(loss=get_loss_function(params['loss']),
                      optimizer=get_optimizer(params['optimizer']),
                      **metrics_kwargs)

        # Save initial model
        if self.dirs is not None:
            model.save(self.dirs['saved_models'] + f'model.{0:04d}-nan.hdf5')

        return model


    def _unpack_tns_list(self, tns_list):

        assert(len(tns_list) > 0)
        if len(tns_list) > 1:
            return ks.layers.Concatenate()(tns_list)
        else:
            return tns_list[0]


    def _apply_time_net(self, img, img_time, merge_method='concatenate'):

        # Flatten input
        input_shape = img_time._keras_shape[1:] # Batch size (None) should not be included
        flattened_img_time = ks.layers.Reshape((np.prod(input_shape),1))(img_time)

        # Let all pixels pass through the function defined by the gate model
        img_gated = ks.layers.TimeDistributed(self.time_net)(flattened_img_time)

        # Convert back to original shape
        img_gated = ks.layers.Reshape(input_shape)(img_gated)

        # Apply the gate by doing element-wise multiplication
        img_gated = ks.layers.multiply([img, img_gated])

        if merge_method == 'multiply':
            img_out = img_gated

        elif merge_method == 'concatenate':
            img_out = ks.layers.concatenate([img, img_gated])

        return img_out


    def _collect_pretrained_weights(self, weights_path, params_path=None,
                                    layers_to_load=['cnn'],
                                    freeze_loaded_layers=True):

        # First we build the pretrained model, so we can extract the desired weights
        # If not given, assume that params_path is in parent folder to weights_path
        if params_path is None:
            params_path = weights_path.rsplit('/',2)[0] + '/hyperparams.pkl'

        # Load parameters
        with open(params_path, "rb") as f:
            params = pickle.load(f)

        # Avoid recursion
        params['pretrained_model']['use'] = False

        # Construct model
        if self.verbose:
            print('Getting pretrained model.')
        # Note that this will save plots of architectures, but that these will
        # be overwritten when the new model is created
        pretrained_model = self.get_model(params)

        # Load trained weights into the model
        pretrained_model.load_weights(weights_path)

        # Put the wanted pretrained weights into dictionary
        self.pretrained_weights = {name:pretrained_model.get_layer(name).get_weights() for name in layers_to_load}


    def train(self):

        # Get dataset lengths
        self.n_points = {set_name:self.data[set_name]['targets'].shape[0] for set_name in self.data}

        # If using a data generator, the number of points in each set must be provided
        if self.params['data_generator']['use']:
            self.n_points = self.params['data_generator']['n_points']

        # NOTE: batch_size should not be divided by n_gpus!
        self._steps_per_epoch = {set_name:np.ceil(self.n_points[set_name] / self.params['batch_size']) for set_name in self.n_points}

        # Get callbacks
        callbacks = self._get_callbacks()

        # Use normal .fit(), when all data can fit in memory
        if not self.params['data_generator']['use']:

            # Prepare weights
            if 'sample_weights' in self.data['train'] and boolify(self.data['train']['sample_weights']):
                self.sample_weights = self.data['train']['sample_weights']
                self.sample_weights_val = (self.data['val']['sample_weights'],)
            else:
                self.sample_weights = None
                self.sample_weights_val = ()

            # Use learning rate finder
            if self.params['lr_finder']['use']:
                lr_range = self._use_lr_finder()
                if self.params['lr_schedule']['name'] is not None and lr_range is not None:
                    self.params['lr_schedule']['range'] = lr_range
                    save_dict(dict={'input_lr_range' : lr_range}, path=self.dirs['log'] + 'hyperparams.txt')
                # Plot learning rate finder results, with chosen upper and lower learning rate
                self._lrf.plot_loss_vs_lr(chosen_limits=self.params['lr_schedule']['range'])
                self._lrf.plot_lr()

            # Organize training data
            x_train, y_train = self._organize_data('train')
            x_val, y_val = self._organize_data('val')

            # Fit (and catch keyboard interrupt)
            try:
                self.model.fit(x_train, y_train,
                               batch_size=self.params['batch_size'],
                               epochs=self.params['epochs'],
                               sample_weight=self.sample_weights,
                               validation_data=(x_val, y_val)+self.sample_weights_val,
                               verbose=self.verbose,
                               callbacks=callbacks)
            except KeyboardInterrupt:
                if query_yes_no('Evaluate model?'):
                    self.evaluate()
                else:
                    print('Exiting without evaluating.')
                    sys.exit()

        # Use DataGenerator instead
        else:
            # Instantiate data generators
            datagen_train = DataGenerator(set_name='train',
                                          load_kwargs=self.params['data_generator']['load_kwargs'],
                                          n_samples=self.n_points['train'],
                                          batch_size=self.params['batch_size'])
            datagen_val = DataGenerator(set_name='val',
                                        load_kwargs=self.params['data_generator']['load_kwargs'],
                                        n_samples=self.n_points['val'],
                                        batch_size=self.params['batch_size'])

            # Fit (and catch keyboard interrupt)
            try:
                self.model.fit_generator(datagen_train,
                                         steps_per_epoch=self._steps_per_epoch['train'],
                                         epochs=self.params['epochs'],
                                         validation_data=datagen_val,
                                         validation_steps=self._steps_per_epoch['val'],
                                         max_queue_size=self.params['data_generator']['max_queue_size'],
                                         workers=self.params['data_generator']['n_workers'],
                                         use_multiprocessing=(self.params['data_generator']['n_workers'] > 1),
                                         verbose=self.verbose,
                                         callbacks=callbacks)
            except KeyboardInterrupt:
                if query_yes_no('Evaluate model?'):
                    self.evaluate()
                else:
                    print('Exiting without evaluating.')
                    sys.exit()


    def _organize_data(self, set_name):
        '''Data should be added in the same order as inputs.'''

        x = []

        if 'images' in self.data['train'] and boolify(self.data[set_name]['images']):
            # Images
            for img_name in self.data[set_name]['images']:
                x.append(self.data[set_name]['images'][img_name])

        # Scalars
        if 'scalars' in self.data['train'] and boolify(self.data[set_name]['scalars']):
            x.append(self.data[set_name]['scalars'])

        # Tracks
        if 'tracks' in self.data['train'] and boolify(self.data[set_name]['tracks']):
            x.append(self.data[set_name]['tracks'])

        # Targets
        y = self.data[set_name]['targets']

        return x,y


    def _use_lr_finder(self):

        epochs = self.params['lr_finder']['epochs']

        self._lrf = LRFinder(min_lr=self.params['lr_finder']['scan_range'][0],
                       max_lr=self.params['lr_finder']['scan_range'][1],
                       steps_per_epoch=self._steps_per_epoch['train'],
                       epochs=epochs,
                       fig_dir=self.dirs['lr_finder'])

        if self.verbose:
            print('Finding best learning rate(s)...')

        # Use normal .fit(), when all data can fit in memory
        if not self.params['data_generator']['use']:

            # Organize training data
            x_train, y_train = self._organize_data('train')

            # Fit while scanning linearly in learning rate
            self.model.fit(x_train, y_train,
                           batch_size=self.params['batch_size'],
                           epochs=epochs,
                           sample_weight=self.sample_weights,
                           verbose=self.verbose,
                           callbacks=[self._lrf])

        # Use DataGenerator instead
        else:
            # Instantiate data generator
            datagen_train = DataGenerator(set_name='train',
                                          load_kwargs=self.params['data_generator']['load_kwargs'],
                                          n_samples=self.n_points['train'],
                                          batch_size=self.params['batch_size'])

            # Fit while scanning linearly in learning rate
            self.model.fit_generator(datagen_train,
                                     epochs=epochs,
                                     max_queue_size=self.params['data_generator']['max_queue_size'],
                                     workers=self.params['data_generator']['n_workers'],
                                     use_multiprocessing=(self.params['data_generator']['n_workers'] > 1),
                                     verbose=self.verbose,
                                     callbacks=[self._lrf])

        if self.verbose:
            print(f"Saved learning rate finder results in {self.dirs['lr_finder']}.")

        # Restore initial model
        self._load_best_weights()

        if self.params['lr_finder']['prompt_for_input'] and self.params['lr_schedule']['name'] is not None:

            successfully_entered = False

            while not successfully_entered:
                try:
                    min_lr = float(eval(input("Please enter min_lr: ")))
                    print("You entered " + str(min_lr))
                    max_lr = float(eval(input("Please enter max_lr: ")))
                    print("You entered " + str(max_lr))
                    successfully_entered = True
                except Exception:
                    print("Invalid input. Please try again. A valid input would be e.g. '3*1e-2'.")

            return min_lr, max_lr


    def _get_callbacks(self):

        history = ks.callbacks.History()
        tensorboard = ks.callbacks.TensorBoard(log_dir=self.dirs['log'])
        modelcheckpoint = ModelCheckpoint(filepath=self.dirs['saved_models'] +
                                          '/{epoch:04d}-{val_loss:.4f}',
                                          save_best_only=True)

        callbacks = [history, tensorboard, modelcheckpoint]

        if self.params['use_earlystopping']:
            earlystopping = ks.callbacks.EarlyStopping(min_delta=0.001, patience=150)
            callbacks.append(earlystopping)

        if self.params['lr_schedule']['name'] == 'SGDR':
            lr_callback = SGDRScheduler(min_lr=self.params['lr_schedule']['range'][0],
                                        max_lr=self.params['lr_schedule']['range'][1],
                                        steps_per_epoch=self._steps_per_epoch['train'],
                                        lr_decay=1.0,
                                        cycle_length=5,
                                        mult_factor=1.5)
            callbacks.append(lr_callback)

        elif self.params['lr_schedule']['name'] == 'CLR':
            lr_callback = CyclicLR(base_lr=self.params['lr_schedule']['range'][0],
                                   max_lr=self.params['lr_schedule']['range'][1],
                                   step_size=self.params['lr_schedule']['step_size_factor']*self._steps_per_epoch['train'],
                                   mode='triangular')
            callbacks.append(lr_callback)

        return callbacks


    def evaluate(self):

        # Signal that evaluation has been attempted
        if not hasattr(self, 'evaluation_scores'):
            self.evaluation_scores = None

        # Load best model
        if self.params['restore_best_weights']:
            self._load_best_weights()

        # Predict on test set
        if 'test' in self.data:
            eval_set = 'test'
        else:
            eval_set = 'val'
        if self.verbose:
            print(f'Predicting on {eval_set} set.')

        # Use normal .predict() or .evaluate(), when all data can fit in memory
        if not self.params['data_generator']['use']:
            # Organize training data
            x_eval, _ = self._organize_data(eval_set)

            # Predict
            preds = self.model.predict(x_eval, batch_size=self.params['batch_size']).flatten()

            # Evaluate
            scores = self.model.evaluate(*self._organize_data(eval_set), batch_size=self.params['batch_size'],
                                         verbose=self.verbose)

        # Use DataGenerator instead
        else:
            # Instantiate data generator
            datagen_pred = DataGenerator(set_name=eval_set,
                                         load_kwargs=self.params['data_generator']['load_kwargs'],
                                         n_samples=self.n_points[eval_set],
                                         batch_size=self.params['batch_size'],
                                         predict=True)

            # Predict
            preds = self.model.predict_generator(datagen_pred,
                                                 max_queue_size=self.params['data_generator']['max_queue_size'],
                                                 workers=self.params['data_generator']['n_workers'],
                                                 use_multiprocessing=(self.params['data_generator']['n_workers'] > 1),
                                                 verbose=self.verbose).flatten()

            # Instantiate data generator
            datagen_eval = DataGenerator(set_name=eval_set,
                                         load_kwargs=self.params['data_generator']['load_kwargs'],
                                         n_samples=self.n_points[eval_set],
                                         batch_size=self.params['batch_size'],
                                         predict=False)

            # Evaluate
            scores = self.model.evaluate_generator(datagen_eval,
                                                   max_queue_size=self.params['data_generator']['max_queue_size'],
                                                   workers=self.params['data_generator']['n_workers'],
                                                   use_multiprocessing=(self.params['data_generator']['n_workers'] > 1),
                                                   verbose=self.verbose)

        # Save predictions
        np.save(self.dirs['log'] + 'predictions', preds)

        # Collect evaluation scores
        # If there are no metrics, make score iterable
        if not self.params['metrics']:
            scores = [scores]
        self.evaluation_scores = {name:score for name,score in zip(self.model.metrics_names,scores)}

        if self.verbose:
            print(f"Results saved in {self.dirs['log']}.")


    def _load_best_weights(self):

        pathnames = glob(self.dirs['saved_models'] + '*.hdf5')

        if len(pathnames) == 0:
            print(f"No models found in {self.dirs['saved_models']}. Continuing without loading model.")
        else:
            losses = [float(pathname.split('/')[-1].split('-',2)[1].split('.hdf5',1)[0]) for pathname in pathnames]
            best_path = pathnames[np.argsort(losses)[0]]
            self.model.load_weights(best_path)
            if self.verbose:
                if len(pathnames) > 1:
                    print(f'Loaded best weights for evaluation from {best_path}.')
                else:
                    print(f'Loaded initial weights from {best_path}.')


    def _plot_models(self):

        # Full
        ks.utils.plot_model(self.model, to_file=self.dirs['fig'] + 'architecture_full.pdf', show_shapes=True)

        # Top
        ks.utils.plot_model(self.top, to_file=self.dirs['fig'] + 'architecture_top.pdf', show_shapes=True)

        if 'images' in self.data['train'] and boolify(self.data['train']['images']):
            # CNN
            ks.utils.plot_model(self.cnn, to_file=self.dirs['fig'] + 'architecture_cnn.pdf', show_shapes=True)

            # FiLM generator
            if self.params['FiLM_gen']['use'] and self.data['train']['scalars']:
                ks.utils.plot_model(self.FiLM_gen, to_file=self.dirs['fig'] + 'architecture_FiLM_gen.pdf', show_shapes=True)

            # Time net
            if any(img_name.startswith('time') for img_name in self.data['train']['images']):
                ks.utils.plot_model(self.time_net, to_file=self.dirs['fig'] + 'architecture_time_net.pdf', show_shapes=True)

        # Scalar net
        if 'scalars' in self.data['train'] and boolify(self.data['train']['scalars']):
            ks.utils.plot_model(self.scalar_net, to_file=self.dirs['fig'] + 'architecture_scalar_net.pdf', show_shapes=True)

        # Track net
        if 'tracks' in self.data['train'] and boolify(self.data['train']['tracks']):
            ks.utils.plot_model(self.track_net, to_file=self.dirs['fig'] + 'architecture_track_net.pdf', show_shapes=True)
