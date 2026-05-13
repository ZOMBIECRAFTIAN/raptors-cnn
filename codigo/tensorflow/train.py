"""
Pipeline de entrenamiento — TensorFlow / Keras.

Equivalente al de PyTorch: dos etapas (feature extraction + fine-tuning),
mismas métricas, mismos hiperparámetros, misma estructura de datos.
"""
import argparse
import random

import numpy as np
import tensorflow as tf
from tensorflow.keras import callbacks, optimizers, losses, metrics

import config
from data_loader import build_datasets, class_weights
from model import build_model, freeze_backbone, unfreeze_all


def set_seed(seed: int = config.SEED) -> None:
    random.seed(seed); np.random.seed(seed); tf.random.set_seed(seed)


def get_callbacks(stage_name, patience):
    return [
        callbacks.ModelCheckpoint(
            filepath=str(config.CHECKPOINT_DIR / f"best_{stage_name}.keras"),
            monitor="val_accuracy", mode="max",
            save_best_only=True, save_weights_only=False, verbose=1,
        ),
        callbacks.EarlyStopping(
            monitor="val_accuracy", mode="max",
            patience=patience, restore_best_weights=True, verbose=1,
        ),
        callbacks.TensorBoard(log_dir=str(config.LOGS_DIR / stage_name)),
    ]


def compile_model(model, lr, label_smoothing, weight_decay=None):
    opt = optimizers.AdamW(learning_rate=lr, weight_decay=weight_decay) if weight_decay else optimizers.Adam(learning_rate=lr)
    model.compile(
        optimizer=opt,
        loss=losses.SparseCategoricalCrossentropy(from_logits=False, label_smoothing=label_smoothing),
        metrics=[metrics.SparseCategoricalAccuracy(name="accuracy"),
                 metrics.SparseTopKCategoricalAccuracy(k=3, name="top3_acc")],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", default="resnet50",
                        choices=["resnet50", "efficientnet_b3", "mobilenet_v3_large", "convnext_tiny"])
    parser.add_argument("--skip-stage1", action="store_true")
    parser.add_argument("--smoke-test", action="store_true",
                        help="corre 1 epoch por etapa sólo para verificar que el pipeline funciona")
    args = parser.parse_args()

    set_seed()
    if args.smoke_test:
        config.STAGE1["epochs"] = 1
        config.STAGE2["epochs"] = 1
        config.STAGE2["early_stopping_patience"] = 0
        print("\n⚡ Smoke-test mode: 1 epoch por etapa.\n")

    train_ds, val_ds, _ = build_datasets()
    cw = class_weights(train_ds)
    print(f"Class weights: {cw}")

    model = build_model(args.arch)

    # ----- Etapa 1 -----
    if not args.skip_stage1:
        freeze_backbone(model)
        compile_model(model, lr=config.STAGE1["lr"], label_smoothing=config.STAGE1["label_smoothing"])
        print(f"\n[Etapa 1] entrenando con backbone congelado por {config.STAGE1['epochs']} epochs")
        model.fit(train_ds, validation_data=val_ds, epochs=config.STAGE1["epochs"],
                  class_weight=cw, callbacks=get_callbacks("stage1", patience=5))
        # Recargar el mejor checkpoint antes de la etapa 2
        model.load_weights(str(config.CHECKPOINT_DIR / "best_stage1.keras"))

    # ----- Etapa 2 -----
    unfreeze_all(model)
    compile_model(model,
                  lr=config.STAGE2["lr"],
                  label_smoothing=config.STAGE2["label_smoothing"],
                  weight_decay=config.STAGE2["weight_decay"])
    print(f"\n[Etapa 2] fine-tuning por hasta {config.STAGE2['epochs']} epochs")
    model.fit(train_ds, validation_data=val_ds, epochs=config.STAGE2["epochs"],
              class_weight=cw,
              callbacks=get_callbacks("stage2", patience=config.STAGE2["early_stopping_patience"]))

    final_path = config.CHECKPOINT_DIR / "best_stage2.keras"
    print(f"\nMejor modelo guardado en: {final_path}")


if __name__ == "__main__":
    main()
