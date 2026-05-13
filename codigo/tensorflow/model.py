"""
Definición de modelos — TensorFlow / Keras.

Las cuatro arquitecturas son las mismas que en la implementación PyTorch:
ResNet50, EfficientNetB3, MobileNetV3Large y ConvNeXtTiny.
"""
import tensorflow as tf
from tensorflow.keras import layers, models, applications

import config
from data_loader import get_augmentation


def build_model(arch: str = "resnet50", pretrained: bool = True) -> tf.keras.Model:
    arch = arch.lower()
    weights = "imagenet" if pretrained else None

    if arch == "resnet50":
        base = applications.ResNet50(weights=weights, include_top=False,
                                     input_shape=(config.INPUT_SIZE, config.INPUT_SIZE, 3))
        preprocess = applications.resnet50.preprocess_input
    elif arch == "efficientnet_b3":
        base = applications.EfficientNetB3(weights=weights, include_top=False,
                                           input_shape=(config.INPUT_SIZE, config.INPUT_SIZE, 3))
        preprocess = applications.efficientnet.preprocess_input
    elif arch == "mobilenet_v3_large":
        base = applications.MobileNetV3Large(weights=weights, include_top=False,
                                             input_shape=(config.INPUT_SIZE, config.INPUT_SIZE, 3))
        preprocess = applications.mobilenet_v3.preprocess_input
    elif arch == "convnext_tiny":
        base = applications.ConvNeXtTiny(weights=weights, include_top=False,
                                         input_shape=(config.INPUT_SIZE, config.INPUT_SIZE, 3))
        preprocess = applications.convnext.preprocess_input
    else:
        raise ValueError(f"Arquitectura desconocida: {arch}")

    inputs = layers.Input(shape=(config.INPUT_SIZE, config.INPUT_SIZE, 3))
    x = get_augmentation()(inputs)
    x = preprocess(x)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(config.NUM_CLASSES, activation="softmax", name="predictions")(x)

    model = models.Model(inputs, outputs, name=f"raptor_{arch}")
    model.base_model = base    # referencia para freeze/unfreeze
    return model


def freeze_backbone(model):
    model.base_model.trainable = False


def unfreeze_all(model):
    model.base_model.trainable = True


def count_parameters(model):
    return sum(int(np.prod(v.shape)) for v in model.trainable_variables)


# imports diferidos para no obligar a numpy si no se usa count_parameters
import numpy as np  # noqa: E402
