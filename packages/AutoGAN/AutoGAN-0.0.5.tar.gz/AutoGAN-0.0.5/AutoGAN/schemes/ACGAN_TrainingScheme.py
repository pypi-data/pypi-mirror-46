# =========================================================================================================
# File: ACGAN_TrainingScheme.py
# Author: Elad Dvash
#
# Description:
# This file contains an implementation of an Auxiliary Classifier GAN (https://arxiv.org/abs/1610.09585)
# and supports multi-input, multi-output generators and discriminators
# =========================================================================================================

from .Base_TrainingScheme import GAN_TrainingScheme
import numpy as np
from ..utils.gan_utils import get_model_output, listify


class ACGAN_TrainingScheme(GAN_TrainingScheme):
    def train_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None, **kwargs):
        # Discriminator Training
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        assert isinstance(out_shape, list), "outputs must be a list in an ACGAN"
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        self.ones[-1], self.zeros[-1] = y[-1], x[-1]
        y = y[:-1]
        loss = discriminator.train_on_batch(y + x, self.ones + self.zeros, sample_weight=sample_weight)
        return loss

    def train_generator(self, model, generator, x, y, batch_size, sample_weight=None, **kwargs):
        # Generator Training
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        assert isinstance(out_shape, list), "outputs must be a list in an ACGAN"
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape
        self.ones[-1] = x[-1]

        y = listify(y)

        if self.has_generator_multioutput:
            loss = generator.train_on_batch(x, y + self.ones, sample_weight=sample_weight)  # x, [y, 1]
        else:
            loss = generator.train_on_batch(x, self.ones, sample_weight=sample_weight)  # x, 1
        return loss

    def test_on_discriminator(self, model, discriminator, x, y, batch_size, sample_weight=None):
        # Discriminator Testing
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        assert isinstance(out_shape, list), "outputs must be a list in an ACGAN"
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape

        y = listify(y)
        x = listify(x)

        self.ones[-1], self.zeros[-1] = y[-1], x[-1]
        y = y[:-1]
        loss = discriminator.test_on_batch(y + x, self.ones + self.zeros, sample_weight=sample_weight)
        return loss

    def test_on_generator(self, model, generator, x, y, batch_size, sample_weight=None):
        # Generator Testing
        out_shape = get_model_output(model.discriminator_model(), batch_size)
        assert isinstance(out_shape, list), "outputs must be a list in an ACGAN"
        if self.out_shape != out_shape or self.out_shape is None:
            self.ones = [np.ones(out_shape)] if not isinstance(out_shape, list) else [np.ones(shape) for shape in
                                                                                      out_shape]
            self.zeros = [np.zeros(out_shape)] if not isinstance(out_shape, list) else [np.zeros(shape) for shape in
                                                                                        out_shape]
            self.out_shape = out_shape
        self.ones[-1] = x[-1]

        y = listify(y)

        if self.has_generator_multioutput:
            loss = generator.test_on_batch(x, y + self.ones, sample_weight=sample_weight)  # x, [y, 1]
        else:
            loss = generator.test_on_batch(x, self.ones, sample_weight=sample_weight)  # x, 1
        return loss
