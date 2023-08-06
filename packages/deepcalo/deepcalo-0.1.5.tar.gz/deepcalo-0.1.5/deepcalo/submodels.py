import numpy as np
import keras as ks
import keras.backend as K
from keras_contrib.applications.resnet import ResNet
from keras_drop_block import DropBlock2D

from .model_components import get_activation, get_downsampling, deserialize_layer_reg, crop, get_norm_act, get_dense_norm_act


def get_top(input_shape, units=[256,256,1], final_activation=None,
            initialization='orthogonal', activation=None, normalization=None,
            layer_reg={}, dropout=None):
    '''Creates a model for the dense top.'''

    input = ks.layers.Input(input_shape)
    tns = input

    # Flatten if needed
    if len(input_shape) > 1:
        tns = ks.layers.Flatten()(tns)

    # Hidden layers
    tns = get_dense_norm_act(tns, units=units[:-1],
                             initialization=initialization,
                             activation=activation,
                             normalization=normalization,
                             layer_reg=layer_reg,
                             dropout=dropout)

    # Output neuron(s)
    tns = ks.layers.Dense(units[-1], activation=final_activation)(tns)

    return ks.models.Model(input, tns, name='top')


def get_cnn(input_shape, FiLM_input_shapes=None,
            cnn_type='simple', conv_dim=2, n_init_filters=32, block_depths=[1,2,2],
            init_kernel_size=3, rest_kernel_size=3,
            downsampling=None, min_size_for_downsampling=6, globalavgpool=False,
            use_squeeze_and_excite=False, squeeze_and_excite_ratio=16,
            cardinality=1, FiLM_tns=None, initialization='orthogonal',
            activation=None, normalization=None, layer_reg={}, dropout=None):
    '''
    Returns a CNN model.

    Args:
    -----
        input_shape : *tuple*

        FiLM_input_shapes : *list of tuples or None*
             The shapes of the list of outputs of the FiLM generator, consisting
             of the biases and scalings to be applied to each feature map in the
             first convolutional layer of each block in the CNN.
             If None, FiLM conditioning will not be used.

        **kwargs :
            See the docs in the README for a description of the rest of the
            arguments.

    Returns:
    --------
        *Instantiated Keras model*
    '''

    # Input
    input = ks.layers.Input(input_shape)
    tns = input

    if FiLM_input_shapes is not None:
        inputs_FiLM = {}
        for i,FiLM_input_shape in enumerate(FiLM_input_shapes):
            inputs_FiLM[f'FiLM_{i}'] = ks.layers.Input(FiLM_input_shape, name=f'FiLM_gen_output_{i}')
        FiLM_tns_list = [inputs_FiLM[key] for key in inputs_FiLM]

    # Skip everything else if cnn_type is 'res18'
    # You can return other readily available models from keras_contrib here
    if cnn_type == 'res18':
        return ResNet(input_shape=input_shape,
                      block='basic',
                      repetitions=[2,2,2,2],
                      include_top=False,
                      initial_strides=(1,1),
                      initial_kernel_size=init_kernel_size,
                      final_pooling='avg')

    # If chosen, reshape to be able to use 3D convolutions (with number of channels now being 1)
    if conv_dim == 3:
        input_shape_tmp = tns._keras_shape[1:] # Batch size (None) should not be included
        tns = ks.layers.Reshape(input_shape_tmp + (1,))(tns)
        if FiLM_input_shapes is not None:
            raise Exception('3D convolutions and FiLM layers are currently not compatible.')

    # Define squeeze and excite module
    def squeeze_excite_module(input, ratio=16):
        ''' Create a channel-wise squeeze-excite block

        From https://github.com/titu1994/keras-squeeze-excite-network/blob/master/se.py

        Args:
            input: input tensor
            n_filters: number of output filters (feature maps)
        Returns: a keras tensor
        References
        -   [Squeeze and Excitation Networks](https://arxiv.org/abs/1709.01507)
        '''

        tns = input
        n_filters = tns._keras_shape[-1]
        se_shape = (1, 1, n_filters)

        if n_filters // ratio < 1:
            raise AssertionError('Please make sure that the number '
                                 'of incoming channels is not less '
                                 'than the ratio in the squeeze_excite_module.')

        tns = ks.layers.GlobalAveragePooling2D()(tns)
        tns = ks.layers.Reshape(se_shape)(tns)
        tns = ks.layers.Dense(n_filters // ratio, activation='relu',
                              kernel_initializer=initialization,
                              use_bias=False)(tns)
        tns = ks.layers.Dense(n_filters, activation='sigmoid',
                              kernel_initializer=initialization,
                              use_bias=False)(tns)

        return ks.layers.multiply([input, tns])

    # Define convolutional module
    def conv_module(tns, n_filters, kernel_size=3, cardinality=1,
                    cnn_type='simple', downsample=False, FiLM_tns=None):

        def conv_drop_norm_act(tns, kernel_size=3, cardinality=1, use_bias=True,
                               norm_first=False, FiLM_tns=None):
            """Convenience function to use for both simple and res type CNNs."""

            def _get_norm_act_dropblock(tns):

                tns = get_norm_act(tns, activation, normalization, FiLM_tns)

                # Dropblock
                if dropout is not None:
                    if conv_dim == 3:
                        raise Exception('3D convolutions and DrobBlock layers are '
                                        'currently not compatible.')
                    if not isinstance(dropout, dict):
                        raise TypeError('Please pass a dict of keyword arguments to '
                                        'the DropBlock layer in the CNN.')
                    else:
                        tns = DropBlock2D(**dropout)(tns)

                return tns

            # Normalization first
            if norm_first:
                tns = _get_norm_act_dropblock(tns)

            # Convolution
            if conv_dim == 2:
                if cardinality==1:
                    tns = ks.layers.Conv2D(n_filters, kernel_size, use_bias=use_bias, padding='same',
                                           kernel_initializer=ks.initializers.get(initialization),
                                           **deserialize_layer_reg(layer_reg))(tns)
                elif cardinality > 1:
                    n_filters_in_per_split = int(tns._keras_shape[-1] / cardinality)
                    if n_filters_in_per_split < 1:
                        raise AssertionError('Please make sure that the number '
                                             'of incoming channels is not less '
                                             'than the cardinality.')
                    n_filters_out_per_split = int(n_filters / cardinality)

                    tns_pre_conv = tns
                    group_list = []
                    for c in range(cardinality):
                        tns = ks.layers.Lambda(lambda z: z[:, :, :, c * n_filters_in_per_split:(c + 1) * n_filters_in_per_split])(tns_pre_conv)
                        tns = ks.layers.Conv2D(n_filters_out_per_split, kernel_size, use_bias=use_bias, padding='same',
                                               kernel_initializer=ks.initializers.get(initialization),
                                               **deserialize_layer_reg(layer_reg))(tns)
                        group_list.append(tns)
                    tns = ks.layers.concatenate(group_list)
                else:
                    raise Exception('Please make sure that cardinality > 0.')

            elif conv_dim == 3:
                if not type(kernel_size)==tuple:
                    kernel_size = (kernel_size,)*2 + (2,)
                if cardinality != 1:
                    print('WARNING: 3D convolutions and grouped convolutions are '
                          'currently not compatible: cardinality != 1 is ignored.')
                tns = ks.layers.Conv3D(n_filters, kernel_size, use_bias=use_bias, padding='same',
                                       kernel_initializer=ks.initializers.get(initialization),
                                       **deserialize_layer_reg(layer_reg))(tns)

            # Normalization last
            if not norm_first:
                tns = _get_norm_act_dropblock(tns)

            return tns

        # Downsample
        if downsample and downsampling is not None:
            # Check if H,W are dynamic - if yes, do downsampling and hope for the best
            if all(dim is None for dim in tns._keras_shape[1:3]):
                tns = get_downsampling(tns, downsampling)
            else:
                # Check that both height and width are at least min_size_for_downsampling
                if all(dim >= min_size_for_downsampling for dim in tns._keras_shape[1:3]):
                    tns = get_downsampling(tns, downsampling)

        if cnn_type == 'simple':
            tns = conv_drop_norm_act(tns, kernel_size=kernel_size,
                                     cardinality=cardinality, use_bias=True,
                                     norm_first=False, FiLM_tns=FiLM_tns)

            if use_squeeze_and_excite:
                tns = squeeze_excite_module(tns, squeeze_and_excite_ratio)

        elif cnn_type == 'res':
            # Project shortcut so it has compatible number of output feature maps
            if downsample:
                if conv_dim == 2:
                    shortcut = ks.layers.Conv2D(n_filters, (1,1), padding='same',
                                           kernel_initializer=ks.initializers.get(initialization),
                                           **deserialize_layer_reg(layer_reg))(tns)
                elif conv_dim == 3:
                    shortcut = ks.layers.Conv3D(n_filters, (1,1,1), padding='same',
                                           kernel_initializer=ks.initializers.get(initialization),
                                           **deserialize_layer_reg(layer_reg))(tns)
            else:
                shortcut = tns

            # First conv
            tns = conv_drop_norm_act(tns, kernel_size=kernel_size,
                                     cardinality=cardinality,
                                     use_bias=normalization is None,
                                     norm_first=True, FiLM_tns=None)

            # Second conv
            tns = conv_drop_norm_act(tns, kernel_size=kernel_size,
                                     cardinality=cardinality, use_bias=True,
                                     norm_first=True, FiLM_tns=FiLM_tns)

            if use_squeeze_and_excite:
                tns = squeeze_excite_module(tns, squeeze_and_excite_ratio)

            # Add
            tns = ks.layers.Add()([tns, shortcut])

        return tns

    # First block (simple convolution, no matter type chosen)
    for j in range(block_depths[0]):
        tns = conv_module(tns, n_init_filters, kernel_size=init_kernel_size,
                          cardinality=1, cnn_type='simple', downsample=False,
                          FiLM_tns=(FiLM_tns_list[0] if FiLM_input_shapes is not None and j==0 else None))

    # Remaining blocks
    n_filters = n_init_filters

    for i,depth in enumerate(block_depths[1:]):
        n_filters *= 2
        for j in range(depth):
            tns = conv_module(tns, n_filters, kernel_size=rest_kernel_size,
                              cardinality=cardinality, cnn_type=cnn_type, downsample=(j==0),
                              FiLM_tns=(FiLM_tns_list[i+1] if FiLM_input_shapes is not None and j==0 else None))

    # Apply global average pooling to reduce the number of features, or simply flatten
    if globalavgpool:
        if conv_dim == 2:
            tns = ks.layers.GlobalAveragePooling2D()(tns)
        elif conv_dim == 3:
            tns = ks.layers.GlobalAveragePooling3D()(tns)
    else:
        # Dynamic flatten
        if all(dim is None for dim in tns._keras_shape[1:3]):
            tns = ks.layers.Lambda(lambda x: K.batch_flatten(x))(tns)
        # Normal flatten
        else:
            tns = ks.layers.Flatten()(tns)

    return ks.models.Model(inputs=(input if FiLM_input_shapes is None else [input] + FiLM_tns_list),
                           outputs=tns, name='cnn')


def get_FiLM_generator(input_shape, n_blocks, n_init_filters, units=[256,256],
                       initialization='orthogonal', activation=None,
                       normalization=None, layer_reg={}, dropout=None):

    # Inputs
    input = ks.layers.Input(input_shape, name='FiLM_scalars')

    # Calculate how many biases and scaling factors are needed
    n_outputs = 2 * n_init_filters * (2**n_blocks - 1)

    # Hidden layers
    tns = get_dense_norm_act(input, units=units,
                             initialization=initialization,
                             activation=activation,
                             normalization=normalization,
                             layer_reg=layer_reg,
                             dropout=dropout)

    # Output neurons
    tns = ks.layers.Dense(n_outputs, **deserialize_layer_reg(layer_reg))(tns)

    # Reshape such that it is transparent which outputs should modify which conv outputs
    tns_list = []
    start = 0
    stop = 2 * n_init_filters
    for i in range(n_blocks):
        tns_list.append(crop(1, start, stop)(tns))
        start, stop = stop, stop + 2 * n_init_filters * 2**(i+1)

    return ks.models.Model(input, tns_list, name='FiLM_generator')


def get_time_net(units=[64,64], use_res=False, final_activation='pgauss_f',
                 final_activation_init=[0.5], initialization='orthogonal',
                 activation=None, normalization=None, layer_reg={}, dropout=None):

    # Do pixel-wise transformation
    input = ks.layers.Input((1,))
    tns = input

    # Hidden layers
    tns = get_dense_norm_act(tns, units=units,
                             initialization=initialization,
                             activation=activation,
                             normalization=normalization,
                             layer_reg=layer_reg,
                             dropout=dropout)

    # Output neuron
    if units:
        tns = ks.layers.Dense(1)(tns)
        if use_res:
            tns = ks.layers.Add()([input, tns])

    # Apply gate activation
    tns = get_activation(final_activation)(tns)

    # Make model
    model = ks.models.Model(input, tns, name='time_net')

    # Set initial weights, if using a parametric activation function
    if final_activation.lower() in ['pgauss', 'pgauss_f', 'pgauss_flipped']: # TODO: Doesn't cover all aliases
        init_weights = [np.array([init],dtype='float32') for init in final_activation_init]
        model.layers[-1].set_weights(init_weights)

    return model


def get_scalar_net(input_shape, units=[256,256],
                   initialization='orthogonal', activation=None,
                   normalization=None, layer_reg={}, dropout=None):
    '''Creates a model for processing (representing) the scalar variables.'''

    input = ks.layers.Input(input_shape)
    tns = input

    # Flatten if needed
    if len(input_shape) > 1:
        tns = ks.layers.Flatten()(tns)

    tns = get_dense_norm_act(tns, units=units,
                             initialization=initialization,
                             activation=activation,
                             normalization=normalization,
                             layer_reg=layer_reg,
                             dropout=dropout)

    return ks.models.Model(input, tns, name='scalar_net')


def get_track_net(input_shape, phi_units=[256,256], rho_units=[256,256],
                  initialization='orthogonal', activation=None,
                  normalization=None, layer_reg={}, dropout=None):
    '''
    Creates a model for processing (representing) tracks, of which there can
    be a varying amount for each event.

    The input should have shape (n_tracks, n_features) (note that batch_size
    should not be included), where n_tracks is the maximum amount of tracks in
    the whole dataset, and where n_features is the number of features for each
    track. If a given datapoint has fewer than n_tracks tracks, the rest should
    be zero-padded. These padded tracks are subsequently masked out.
    '''

    # Inputs
    input = ks.layers.Input(input_shape)
    tns = input

    apply_mask = True

    # Implement mask manually. For why this is necessary, see https://github.com/keras-team/keras/issues/10320
    if apply_mask:
        # Construct
        mask = ks.layers.Lambda(lambda x: K.cast(K.all(K.not_equal(x, 0), axis=2), 'float32'), name='mask')(tns)

    # Define the inner model (phi), passed to TimeDistributed
    input_inner = ks.layers.Input((input_shape[-1],))

    tns_inner = get_dense_norm_act(input_inner, units=phi_units,
                                  initialization=initialization,
                                  activation=activation,
                                  normalization=normalization,
                                  layer_reg=layer_reg,
                                  dropout=dropout)

    inner_model = ks.models.Model(input_inner, tns_inner, name='phi')

    # Pass each track through the inner_model
    tns = ks.layers.TimeDistributed(inner_model)(tns)

    if apply_mask:
        # Reshape mask so that it can be multiplied with the output of TimeDistributed
        mask = ks.layers.Lambda(lambda x: K.expand_dims(x), name='expand')(mask)

        # Apply the mask
        tns = ks.layers.multiply([mask, tns])

    # Sum the outputs of inner_model for each track (to invoke permutation invariance)
    tns = ks.layers.Lambda(lambda x: K.sum(x, axis=1), name='sum')(tns)

    # Pass the summed outputs through the final transformation (rho)
    tns = get_dense_norm_act(tns, units=rho_units,
                             initialization=initialization,
                             activation=activation,
                             normalization=normalization,
                             layer_reg=layer_reg,
                             dropout=dropout)

    return ks.models.Model(input, tns, name='track_net')
