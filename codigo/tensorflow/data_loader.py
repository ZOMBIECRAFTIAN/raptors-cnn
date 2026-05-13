"""
Carga de datos — TensorFlow / Keras.

Usa tf.keras.utils.image_dataset_from_directory sobre la misma estructura
de carpetas que la implementación de PyTorch para garantizar paridad.
"""
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

import config


def get_augmentation():
    """Pipeline de augmentation equivalente al de PyTorch."""
    return tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.04),       # ≈ ±15°
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.2),
        layers.RandomBrightness(0.2),
    ], name="augmentation")


def build_datasets(processed_dir=config.PROCESSED_DIR,
                   batch_size=config.BATCH_SIZE,
                   input_size=config.INPUT_SIZE):
    """Construye los datasets de train, val y test."""
    common = dict(
        labels="inferred",
        label_mode="int",
        class_names=config.SPECIES,
        image_size=(input_size, input_size),
        batch_size=batch_size,
    )
    train = tf.keras.utils.image_dataset_from_directory(processed_dir / "train", shuffle=True,  seed=config.SEED, **common)
    val   = tf.keras.utils.image_dataset_from_directory(processed_dir / "val",   shuffle=False, **common)
    test  = tf.keras.utils.image_dataset_from_directory(processed_dir / "test",  shuffle=False, **common)

    AUTOTUNE = tf.data.AUTOTUNE
    return (
        train.cache().prefetch(AUTOTUNE),
        val.cache().prefetch(AUTOTUNE),
        test.cache().prefetch(AUTOTUNE),
    )


def class_weights(train_ds):
    """w_i = N / (C * n_i) — equivalente al cálculo de PyTorch."""
    counts = np.zeros(config.NUM_CLASSES)
    for _, y in train_ds.unbatch():
        counts[int(y.numpy())] += 1
    total = counts.sum()
    return {i: float(total / (config.NUM_CLASSES * max(counts[i], 1))) for i in range(config.NUM_CLASSES)}
