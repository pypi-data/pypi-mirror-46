# =========================================================================================================
# File: ContentGAN_TrainingScheme.py
# Author: Elad Dvash
#
# Description:
# This file contains an implementation of a content-loss GAN
# and supports multi-input, multi-output generators and discriminators
# =========================================================================================================

import keras
from keras.models import Model
import numpy as np
from .Base_TrainingScheme import GAN_TrainingScheme
from ..utils.gan_utils import get_model_input, get_model_output, set_layer_name, extend, prepare_compile, listify


class ContentGAN_TrainingScheme(GAN_TrainingScheme):
    def __init__(self, **kwargs):
        self.has_content_network = False
        super(ContentGAN_TrainingScheme, self).__init__(**kwargs)

    def compile_generator(self, model, generator, discriminator, content_network=None,
                          discriminator_loss=None, generator_loss=None, content_loss=None,
                          generator_metrics=[], discriminator_metrics=[], content_metrics=[],
                          generator_loss_weight=1, discriminator_loss_weight=1, content_loss_weight=1,
                          optimizer=None, **kwargs):

        if content_network is None:
            return super(ContentGAN_TrainingScheme, self).compile_generator(model, generator, discriminator,
                                                                            discriminator_loss, generator_loss,
                                                                            generator_metrics, discriminator_metrics,
                                                                            generator_loss_weight,
                                                                            discriminator_loss_weight, optimizer,
                                                                            **kwargs)

        """Compile a Generator."""
        if 'loss' in kwargs and discriminator_loss is None:
            discriminator_loss = kwargs['loss']
        if 'metrics' in kwargs and discriminator_metrics is None:
            discriminator_metrics = kwargs['metrics']
        if 'loss_weight' in kwargs and discriminator_loss_weight is None:
            discriminator_loss_weight = kwargs['loss_weight']

        discriminator.trainable = False
        content_network.trainable = False
        generator.trainable = True

        model_shape = get_model_input(generator)
        inp = [keras.layers.Input(shape[1:]) for shape in model_shape] if isinstance(model_shape, list) else \
            keras.layers.Input(model_shape[1:])

        gen_out, gen_names = set_layer_name(generator(inp), generator.name)
        dis_out, dis_names = set_layer_name(discriminator(gen_out), discriminator.name)
        content_out, content_names = set_layer_name(content_network(gen_out), content_network.name)

        # ----- Generator -----

        inputs = []
        extend(inputs, inp)

        outputs = []
        if generator_loss is not None:
            self.has_generator_multioutput = True
            extend(outputs, gen_out)
        else:
            gen_names = []

        if content_loss is not None:
            extend(outputs, content_out)
        else:
            content_names = []

        if discriminator_loss is not None:
            extend(outputs, dis_out)
        else:
            dis_names = []

        generator_loss = listify(generator_loss) * (len(gen_names) if len(listify(generator_loss)) == 1 else 1)
        discriminator_loss = listify(discriminator_loss) * (
        len(dis_names) if len(listify(discriminator_loss)) == 1 else 1)
        content_loss = listify(content_loss) * (len(content_names) if len(listify(content_loss)) == 1 else 1)
        generator_metrics = listify(generator_metrics) * (len(gen_names) if len(listify(generator_metrics)) == 1 else 1)
        discriminator_metrics = listify(discriminator_metrics) * (
        len(dis_names) if len(listify(discriminator_metrics)) == 1 else 1)
        content_metrics = listify(content_metrics) * (len(content_names) if len(listify(content_metrics)) == 1 else 1)
        generator_loss_weight = listify(generator_loss_weight) * (
        len(gen_names) if len(listify(generator_loss_weight)) == 1 else 1)
        discriminator_loss_weight = listify(discriminator_loss_weight) * (
        len(dis_names) if len(listify(discriminator_loss_weight)) == 1 else 1)
        content_loss_weight = listify(content_loss_weight) * (
        len(content_names) if len(listify(content_loss_weight)) == 1 else 1)

        l, m, w = prepare_compile(gen_names + content_names + dis_names,
                                  generator_loss + content_loss + discriminator_loss,
                                  generator_metrics + content_metrics + discriminator_metrics,
                                  generator_loss_weight + content_loss_weight + discriminator_loss_weight)

        generator_model = Model(inputs=inputs, outputs=outputs)
        generator_model.compile(optimizer=optimizer, loss=l, metrics=m, loss_weights=w)
        # ----- Generator -----

        discriminator.trainable = True
        content_network.trainable = True

        return generator_model

    def train_generator(self, model, generator, x, y, batch_size, sample_weight=None, **kwargs):
        # Generator Training
        if not self.has_content_network:
            return super(ContentGAN_TrainingScheme, self).train_generator(model, generator, x, y, batch_size,
                                                                          sample_weight, **kwargs)

        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        y = listify(y)
        content_vectors = y[-1:]
        y = y[:-1]
        if self.has_generator_multioutput:
            loss = generator.train_on_batch(x, y + content_vectors + self.ones,
                                            sample_weight=sample_weight)  # x, [y_gen_out, y_content_out, 1]
        else:
            loss = generator.train_on_batch(x, content_vectors + self.ones,
                                            sample_weight=sample_weight)  # x, [y_content_out, 1]
        return loss

    def test_on_generator(self, model, generator, x, y, batch_size, sample_weight=None):
        # Generator Testing
        if not self.has_content_network:
            return super(ContentGAN_TrainingScheme, self).test_on_generator(model, generator, x, y, batch_size,
                                                                            sample_weight)

        out_shape = get_model_output(model.discriminator_model(), batch_size)
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        y = listify(y)
        content_vectors = y[-1:]
        y = y[:-1]
        if self.has_generator_multioutput:
            loss = generator.test_on_batch(x, y + content_vectors + self.ones,
                                           sample_weight=sample_weight)  # x, [y_gen_out, y_content_out, 1]
        else:
            loss = generator.test_on_batch(x, content_vectors + self.ones,
                                           sample_weight=sample_weight)  # x, [y_content_out, 1]
        return loss
