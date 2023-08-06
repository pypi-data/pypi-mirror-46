# =========================================================================================================
# File: IWGAN_TrainingScheme.py
# Author: Elad Dvash
#
# Description:
# This file contains an implementation of an IWGAN-GP (https://arxiv.org/abs/1704.00028)
# and supports multi-input, multi-output generators and discriminators
# =========================================================================================================

import keras
from keras import backend as K
import numpy as np
from .Base_TrainingScheme import GAN_TrainingScheme
from keras.layers.merge import _Merge
from keras.models import Model
from functools import partial
from ..utils.gan_utils import get_model_input, get_model_output, set_layer_name, extend, prepare_compile, listify


# -----------------------------------------------------------------------------------------------------------------
#  IWGAN Training Scheme
# -----------------------------------------------------------------------------------------------------------------

class IWGAN_TrainingScheme(GAN_TrainingScheme):
    def __init__(self, batch_size, **kwargs):
        super(IWGAN_TrainingScheme, self).__init__(**kwargs)
        self.batch_size = batch_size
        self.mones = None

    def compile_discriminator(self, model, generator, discriminator, optimizer=None, gp_weight=10,
                              metrics=[], **kwargs):

        discriminator.trainable = True
        generator.trainable = False

        model_shape = get_model_input(generator)
        inp = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
              keras.layers.Input(model_shape[1:])

        in_gen = generator(inp)
        model_shape = get_model_input(discriminator)
        in_real = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
                  keras.layers.Input(model_shape[1:])

        dis_out_real, dis_out_real_names = set_layer_name(discriminator(in_real), discriminator.name + "_real")
        dis_out_fake, dis_out_fake_names = set_layer_name(discriminator(in_gen), discriminator.name + "_fake")

        if isinstance(in_real, list):
            averaged_samples = [RandomWeightedAverage(self.batch_size)([in_real[i], in_gen[i]])
                                for i in range(len(in_real))]
        else:
            averaged_samples = RandomWeightedAverage(self.batch_size)([in_real, in_gen])

        averaged_samples_out, avg_samples_out_names = set_layer_name(discriminator(averaged_samples),
                                                                     discriminator.name+"_avg")

        partial_gp_loss = [partial(gradient_penalty_loss, averaged_samples=averaged_samples,
                                   gradient_penalty_weight=gp_weight) for _ in range(len(averaged_samples_out))]
        for i, gp in enumerate(partial_gp_loss):
            gp.__name__ = 'gradient_penalty_%d' % i

        # ----- Discriminator -----
        inputs = []
        extend(inputs, in_real)
        extend(inputs, inp)

        outputs = []
        extend(outputs, dis_out_real)
        extend(outputs, dis_out_fake)
        extend(outputs, averaged_samples_out)

        names = dis_out_real_names + dis_out_fake_names + avg_samples_out_names
        loss = [wasserstein_loss]
        metrics = listify([metrics])
        if len(metrics) == 1:
            metrics = [metrics[0]] * len(dis_out_real_names)
        elif all([not isinstance(m, list) for m in metrics]):
            metrics = [metrics] * len(dis_out_real_names)

        l, m, _ = prepare_compile(names,
                                  loss * 2 + partial_gp_loss,
                                  metrics * 2)

        discriminator_model = Model(inputs=inputs, outputs=outputs)
        discriminator_model.compile(optimizer=optimizer, loss=l, metrics=m)

        # ----- Discriminator -----

        generator.trainable = True
        return discriminator_model

    def train_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None, **kwargs):
        # Discriminator Training
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) \
                                             else [np.ones(shape) for shape in out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) \
                                               else [np.zeros(shape) for shape in out_shape]
            self.mones = [-np.ones(out_shape)] if not isinstance(out_shape, list) \
                                               else [-np.ones(shape) for shape in out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        loss = discriminator.train_on_batch(y + x,
                                            self.ones +
                                            self.mones +
                                            self.zeros,
                                            sample_weight=None)

        return loss

    def test_on_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None):
        # Discriminator Testing
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) \
                                             else [np.ones(shape) for shape in out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) \
                                               else [np.zeros(shape) for shape in out_shape]
            self.mones = [-np.ones(out_shape)] if not isinstance(out_shape, list) \
                                               else [-np.ones(shape) for shape in out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        loss = discriminator.test_on_batch(y + x,
                                           self.ones +
                                           self.mones +
                                           self.zeros,
                                           sample_weight=None)
        return loss


class RandomWeightedAverage(_Merge):
    def __init__(self, batch_size, **kwargs):
        super(RandomWeightedAverage, self).__init__(**kwargs)
        self.batch_size = batch_size

    def _merge_function(self, inputs):
        weights = K.random_uniform((self.batch_size, 1, 1, 1))
        return (weights * inputs[0]) + ((1 - weights) * inputs[1])


def wasserstein_loss(y_true, y_pred):
    return K.mean(y_true * y_pred)


def gradient_penalty_loss(y_true, y_pred, averaged_samples, gradient_penalty_weight):
    gradients = K.gradients(y_pred, averaged_samples)[0]
    gradients_sqr = K.square(gradients)
    gradients_sqr_sum = K.sum(gradients_sqr, axis=np.arange(1, len(gradients_sqr.shape)))
    gradient_l2_norm = K.sqrt(gradients_sqr_sum)
    gradient_penalty = gradient_penalty_weight * K.square(1 - gradient_l2_norm)
    grads = K.mean(gradient_penalty)
    return grads


def zcgp_loss(y_true, y_pred, averaged_samples, gradient_penalty_weight):
    gradients = K.gradients(y_pred, averaged_samples)[0]
    gradients_sqr = K.square(gradients)
    gradients_sqr_sum = K.sum(gradients_sqr, axis=np.arange(1, len(gradients_sqr.shape)))
    gradient_l2_norm = K.sqrt(gradients_sqr_sum)
    gradient_penalty = K.square(gradient_l2_norm)
    grads = gradient_penalty_weight * K.mean(gradient_penalty)
    return grads


class IWGAN_ZCGP_TrainingScheme(IWGAN_TrainingScheme):
    def __init__(self, **kwargs):
        super(IWGAN_ZCGP_TrainingScheme, self).__init__(0, **kwargs)
        self.batches_seen = 0
        self.has_true_gp = False
        self.has_fake_gp = False

    def compile_discriminator(self, model, generator, discriminator, loss=None, optimizer=None,
                              gp_weight_true=10, gp_weight_fake=0, metrics=[], **kwargs):

        discriminator.trainable = True
        generator.trainable = False

        model_shape = get_model_input(generator)
        inp = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        in_gen = generator(inp)
        model_shape = get_model_input(discriminator)
        in_real = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        dis_out_real, dis_out_real_names = set_layer_name(discriminator(in_real), discriminator.name + "_real")
        dis_out_fake, dis_out_fake_names = set_layer_name(discriminator(in_gen), discriminator.name + "_fake")

        if gp_weight_true > 0:
            self.has_true_gp = True
            averaged_samples_out, avg_samples_out_names = set_layer_name(discriminator(in_real),
                                                                         discriminator.name + "_avg")

            partial_gp_loss = [partial(zcgp_loss, averaged_samples=in_real,
                                       gradient_penalty_weight=gp_weight_true) for _ in range(len(averaged_samples_out))]
            for i, gp in enumerate(partial_gp_loss):
                gp.__name__ = 'gradient_penalty_%d' % i
        else:
            averaged_samples_out = []
            avg_samples_out_names = []
            partial_gp_loss = []

        if gp_weight_fake > 0:
            self.has_fake_gp = True
            averaged_samples_fake_out, avg_samples_fake_out_names = set_layer_name(discriminator(generator(inp)),
                                                                                   discriminator.name + "_fake_avg")

            partial_gp_fake_loss = [partial(zcgp_loss, averaged_samples=inp,
                                            gradient_penalty_weight=gp_weight_fake) for _ in
                                    range(len(averaged_samples_out))]
            for i, gp in enumerate(partial_gp_fake_loss):
                gp.__name__ = 'gradient_penalty_fake_%d' % i
        else:
            averaged_samples_fake_out = []
            avg_samples_fake_out_names = []
            partial_gp_fake_loss = []
        # ----- Discriminator -----
        inputs = []
        extend(inputs, in_real)
        extend(inputs, inp)

        outputs = []
        extend(outputs, dis_out_real)
        extend(outputs, dis_out_fake)
        extend(outputs, averaged_samples_out)
        extend(outputs, averaged_samples_fake_out)

        names = dis_out_real_names + dis_out_fake_names + avg_samples_out_names + avg_samples_fake_out_names
        loss = [wasserstein_loss]
        metrics = listify([metrics])
        if len(metrics) == 1:
            metrics = [metrics[0]] * len(dis_out_real_names)
        elif all([not isinstance(m, list) for m in metrics]):
            metrics = [metrics] * len(dis_out_real_names)

        l, m, _ = prepare_compile(names,
                                  loss * 2 + partial_gp_loss + partial_gp_fake_loss,
                                  metrics * 2)

        discriminator_model = Model(inputs=inputs, outputs=outputs)
        discriminator_model.compile(optimizer=optimizer, loss=l, metrics=m)

        # ----- Discriminator -----

        generator.trainable = True
        return discriminator_model

    def train_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None,
                            sigma_noise=0.1, noise_batches=10000, **kwargs):
        # Discriminator Training
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) \
                else [np.ones(shape) for shape in out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) \
                else [np.zeros(shape) for shape in out_shape]
            self.mones = [-np.ones(out_shape)] if not isinstance(out_shape, list) \
                else [-np.ones(shape) for shape in out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)
        if sigma_noise != 0 and noise_batches != 0 and self.batches_seen < noise_batches:
            for yi in y:
                yi += np.random.normal(scale=max(sigma_noise * (1 - self.batches_seen / noise_batches), 0),
                                       size=yi.shape)

        loss = discriminator.train_on_batch(y + x,
                                            self.ones +
                                            self.mones +
                                            self.zeros * (int(self.has_true_gp) + int(self.has_fake_gp)),
                                            sample_weight=None)
        self.batches_seen += 1
        return loss

    def test_on_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None):
        # Discriminator Testing
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) \
                else [np.ones(shape) for shape in out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) \
                else [np.zeros(shape) for shape in out_shape]
            self.mones = [-np.ones(out_shape)] if not isinstance(out_shape, list) \
                else [-np.ones(shape) for shape in out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        loss = discriminator.test_on_batch(y + x,
                                           self.ones +
                                           self.mones +
                                           self.zeros * (int(self.has_true_gp) + int(self.has_fake_gp)),
                                           sample_weight=None)
        return loss
