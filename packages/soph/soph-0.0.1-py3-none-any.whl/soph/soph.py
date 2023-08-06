
import keras
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from keras import backend as K
from sklearn import metrics


def plot_decision_boundary(pred_func, x, y, ax=None, points=1e3, pal=dict(enumerate(sns.color_palette("husl", 4))),
                           margin_func=None, alpha=.1):
    """Plots the decision boundary for a function that generates a prediction.

    Args:
        pred_func (function): Function that returns integer category labels for `x`.
        x (array): [2 x n] array.
        y (array): any-dimensional array (will be flattened)
        ax (axis): matplotlib axis. None generates our own.
        points (floatlike): number of points we wish to generate
        pal: pallete of colors for each class label
        margin_func: optional function for generating margins (drawn at margin = ±1)
        alpha: transparency of scatterplot points

    Returns:
        None
    """
    if ax is None:
        fig, ax = plt.subplots()

    y_pred = pred_func(x)
    score = metrics.accuracy_score(y_pred.flatten(), y.flatten())

    sns.scatterplot(x=x[:, 0], y=x[:, 1], hue=y, alpha=alpha, edgecolor=None,
                    palette=pal, ax=ax)

    side_pts = int(np.sqrt(points))

    x0_min, x0_max = ax.get_xlim()
    x1_min, x1_max = ax.get_ylim()
    xx, yy = np.meshgrid(
        np.linspace(x0_min, x0_max, num=side_pts),
        np.linspace(x1_min, x1_max, num=side_pts))

    Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    ax.text((x0_min + x0_max)/2, x1_min + (x1_max - x1_min)*.1,
            f"acc: {score:.1%}", bbox=dict(boxstyle="round", fc="white",
                                           ec="black"))

    ax.contourf(xx, yy, Z, alpha=0.2, colors=list(pal.values()), zorder=-1)

    if not (margin_func is None):
        Z = margin_func(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

        # plot decision boundary and margins
        ax.contour(xx, yy, Z, colors='k', levels=[-1, 1], alpha=0.5,
                   linestyles=['--', '--'], zorder=0)


# epsilon set according to BIGGAN https://arxiv.org/pdf/1809.11096.pdf
def _l2normalizer(v, epsilon=1e-4):
    return v / (K.sum(v**2)**0.5 + epsilon)


def power_iteration(W, u, rounds=1):
    '''
    Accroding the paper, we only need to do power iteration one time.
    '''
    _u = u

    for i in range(rounds):
        _v = _l2normalizer(K.dot(_u, W))
        _u = _l2normalizer(K.dot(_v, K.transpose(W)))

    W_sn = K.sum(K.dot(_u, W) * _v)
    return W_sn, _u, _v


class Conv2D(keras.layers.Conv2D):
    def __init__(self, filters, spectral_normalization=False, **kwargs):
        self.spectral_normalization = spectral_normalization
        super(Conv2D, self).__init__(filters, **kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.

        self.u = self.add_weight(
            name='u',
            shape=(1, self.filters),
            initializer='uniform',
            trainable=False)

        #         self.kernel = self.add_weight(name='kernel',
        #                                       shape=(input_shape[1], self.output_dim),
        #                                       initializer='uniform',
        #                                       trainable=True)
        super(Conv2D, self).build(input_shape)
        # Be sure to call this at the end

    def compute_spectral_normal(self, training=True):
        # Spectrally Normalized Weight
        if self.spectral_normalization:
            # Get kernel tensor shape [kernel_h, kernel_w, in_channels, out_channels]
            W_shape = self.kernel.shape.as_list()

            # Flatten the Tensor
            # [out_channels, N]
            W_mat = K.reshape(self.kernel, [W_shape[-1], -1])

            W_sn, u, v = power_iteration(W_mat, self.u)

            if training:
                # Update estimated 1st singular vector
                self.u.assign(u)

            return self.kernel / W_sn
        else:
            return self.kernel

    def call(self, inputs, training=None):

        outputs = K.conv2d(
            inputs,
            self.compute_spectral_normal(training=training),
            strides=self.strides,
            padding=self.padding,
            data_format=self.data_format,
            dilation_rate=self.dilation_rate)

        if self.use_bias:
            outputs = K.bias_add(
                outputs, self.bias, data_format=self.data_format)

        if self.activation is not None:
            return self.activation(outputs)
        return outputs

    def compute_output_shape(self, input_shape):
        return super(Conv2D, self).compute_output_shape(input_shape)


class Conv2DTranspose(keras.layers.Conv2DTranspose):
    def __init__(self, spectral_normalization=False, **kwargs):
        self.spectral_normalization = spectral_normalization
        super(Conv2DTranspose, self).__init__(**kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.

        self.u = self.add_weight(
            name='u',
            shape=(1, self.filters),
            initializer='uniform',
            trainable=False)

        #         self.kernel = self.add_weight(name='kernel',
        #                                       shape=(input_shape[1], self.output_dim),
        #                                       initializer='uniform',
        #                                       trainable=True)
        super(Conv2DTranspose, self).build(input_shape)
        # Be sure to call this at the end

    def compute_spectral_normal(self, training=True):
        # Spectrally Normalized Weight
        if self.spectral_normalization:
            # Get kernel tensor shape [kernel_h, kernel_w, in_channels, out_channels]
            W_shape = self.kernel.shape.as_list()

            # Flatten the Tensor
            # [out_channels, N]
            W_mat = K.reshape(self.kernel, [W_shape[-2], -1])

            W_sn, u, v = power_iteration(W_mat, self.u)

            if training:
                # Update estimated 1st singular vector
                self.u.assign(u)

            return self.kernel / W_sn
        else:
            return self.kernel

    def call(self, inputs, training=None):
        input_shape = K.shape(inputs)
        batch_size = input_shape[0]
        if self.data_format == 'channels_first':
            h_axis, w_axis = 2, 3
        else:
            h_axis, w_axis = 1, 2

        height, width = input_shape[h_axis], input_shape[w_axis]
        kernel_h, kernel_w = self.kernel_size
        stride_h, stride_w = self.strides

        # Infer the dynamic output shape:
        out_height = keras.utils.conv_utils.deconv_length(
            height, stride_h, kernel_h, self.padding)
        out_width = keras.utils.conv_utils.deconv_length(
            width, stride_w, kernel_w, self.padding)
        if self.data_format == 'channels_first':
            output_shape = (batch_size, self.filters, out_height, out_width)
        else:
            output_shape = (batch_size, out_height, out_width, self.filters)

        outputs = K.conv2d_transpose(
            inputs,
            self.compute_spectral_normal(training=training),
            output_shape,
            self.strides,
            padding=self.padding,
            data_format=self.data_format,
            #             dilation_rate=self.dilation_rate
        )

        if self.use_bias:
            outputs = K.bias_add(
                outputs, self.bias, data_format=self.data_format)

        if self.activation is not None:
            return self.activation(outputs)
        return outputs

    def compute_output_shape(self, input_shape):
        return super(Conv2DTranspose, self).compute_output_shape(input_shape)


def act_layer(activation, name=None):

    if name is None:
        name = activation

    if activation == "lrelu":
        return keras.layers.LeakyReLU(.1, name=name)
    else:
        return keras.layers.Activation(
            activation, name=name)


def batch_norm():
    return keras.layers.BatchNormalization(momentum=0.9, epsilon=0.00002)


def build_discriminator(
    n_pixels=32,
    alpha=2,
    filter_dim=64,
    activation="relu",
    batch_normalization=False,
    spectral_normalization=False,
    initializer="glorot_uniform",
    use_bias=True,
    pooling="avg",
    name="Discriminator",
):

    # notes:
    # - don't use spectral norm and batch norm (see https://github.com/AlexiaJM/RelativisticGAN/blob/master/code/GAN_losses_iter.py)

    start_pow = np.log2(n_pixels) - 3

    img = keras.Input(shape=(n_pixels, n_pixels, 3))

    conv_block = img
    n_blocks = int(start_pow + 1)
    for i in range(n_blocks):
        n_filters = int(filter_dim * (alpha**i))

        # conv_block = Conv2D(
        #     n_filters,
        #     spectral_normalization=spectral_normalization,
        #     kernel_initializer=initializer,
        #     kernel_size=3,
        #     strides=1,
        #     padding="same",
        #     use_bias=use_bias,
        #     name=f"D{i}-k3s1-s{spectral_normalization}",
        # )(conv_block)
        #
        # if batch_normalization:
        #     conv_block = batch_norm()(conv_block)
        #
        # conv_block = act_layer(
        #     activation, name=f"D{i}.1-{activation}")(conv_block)

        conv_block = Conv2D(
            n_filters,
            spectral_normalization=spectral_normalization,
            kernel_initializer=initializer,
            kernel_size=4,
            strides=2,
            padding="same",
            use_bias=use_bias,
            name=f"D{i}-k4s2-s{spectral_normalization}",
        )(conv_block)

        if batch_normalization:
            conv_block = batch_norm()(conv_block)

        conv_block = act_layer(
            activation, name=f"D{i}.2-{activation}")(conv_block)

    conv_block = Conv2D(
        int(filter_dim * (alpha**n_blocks)),
        spectral_normalization=spectral_normalization,
        kernel_initializer=initializer,
        kernel_size=3,
        strides=1,
        padding="same",
        use_bias=use_bias,
        name=f"D{n_blocks}-k3s1-s{spectral_normalization}",
    )(conv_block)

    if batch_normalization:
        conv_block = batch_norm()(conv_block)

    conv_block = act_layer(
        activation, name=f"D{n_blocks}.1-{activation}")(conv_block)

    if pooling == "avg":
        h = keras.layers.GlobalAveragePooling2D()(conv_block)
    else:
        h = keras.layers.Flatten()(conv_block)

    class_block = keras.layers.Dense(1, kernel_initializer=initializer)(h)

    # class_block = act_layer(
    #     "sigmoid", name=f"Do-sigmoid")(class_block)

    return keras.Model(img, class_block, name="Discriminator")


def build_generator(
    n_pixels=32,
    latent_dim=128,
    alpha=2,
    filter_dim=64,
    kernel_size=3,
    activation="relu",
    batch_normalization=False,
    spectral_normalization=False,
    initializer="glorot_uniform",
    use_bias=True,
    upsample=True,
    name="Generator",
):

    start_pow = np.log2(n_pixels) - 2

    noise_input = keras.Input(shape=(latent_dim, ))

    noise_block = keras.layers.Dense(
        int(filter_dim * (alpha**start_pow)) * 4 * 4,
        input_dim=latent_dim,
        kernel_initializer=initializer,
        name=f"G-dense"
    )(noise_input)
    # noise_block = act_layer(activation, name=f"G.d-{activation}")(noise_block)
    noise_block = keras.layers.Reshape(
        (4, 4, int(filter_dim * (alpha**start_pow))))(noise_block)

    # if batch_normalization:
    #     noise_block = batch_norm()(noise_block)

    up_conv_block = noise_block

    n_blocks = int(start_pow)

    for i in range(1, n_blocks + 1):

        up_conv_block = Conv2DTranspose(
            int((alpha**(start_pow - i)) * filter_dim),
            spectral_normalization=spectral_normalization,
            kernel_initializer=initializer,
            kernel_size=4,
            strides=2,
            padding="same",
            use_bias=use_bias,
            name=f"G{i}-k4s2-s{spectral_normalization}"
        )(up_conv_block)

        if batch_normalization:
            up_conv_block = batch_norm()(up_conv_block)

        up_conv_block = act_layer(
            activation,
            name=f"G{i}-{activation}"
        )(up_conv_block)

    up_conv_block = Conv2D(
        3,
        spectral_normalization=spectral_normalization,
        kernel_initializer=initializer,
        kernel_size=3,
        strides=1,
        padding="same",
        use_bias=use_bias,
        name=f"Go-k3s1-s{spectral_normalization}"
    )(up_conv_block)

    up_conv_block = act_layer(
        "tanh",
        name=f"Go-tanh"
    )(up_conv_block)

    return keras.Model(noise_input, up_conv_block, name=name)
