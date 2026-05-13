"""
Verificación del entorno TensorFlow.

Corre con:
    conda activate raptors-tf
    python verify_setup.py
"""
import sys
import platform


def section(title: str) -> None:
    bar = "=" * 70
    print(f"\n{bar}\n  {title}\n{bar}")


def check(label: str, ok: bool, detail: str = "") -> None:
    mark = "✓" if ok else "✗"
    print(f"  [{mark}] {label}" + (f"  →  {detail}" if detail else ""))


def main() -> int:
    failures = 0

    # 1. Python
    section("1. Python")
    py_ok = sys.version_info >= (3, 10)
    check(f"Python {platform.python_version()} (se requiere ≥ 3.10)", py_ok)
    failures += 0 if py_ok else 1

    # 2. TensorFlow
    section("2. TensorFlow")
    try:
        import tensorflow as tf
        check(f"tensorflow {tf.__version__}", True)
        check(f"keras {tf.keras.__version__}", True)
    except Exception as e:
        check("tensorflow no se pudo importar", False, str(e))
        return 1

    # 3. GPU
    section("3. GPU NVIDIA")
    gpus = tf.config.list_physical_devices("GPU")
    gpu_ok = len(gpus) > 0
    check(f"GPUs visibles para TensorFlow", gpu_ok, f"{len(gpus)} dispositivo(s)")
    if gpu_ok:
        for i, g in enumerate(gpus):
            details = tf.config.experimental.get_device_details(g)
            name = details.get("device_name", str(g))
            cc = details.get("compute_capability", "—")
            check(f"  GPU {i}", True, f"{name}  (compute capability {cc})")
        try:
            from tensorflow.python.platform import build_info
            check("Build CUDA", True, build_info.build_info.get("cuda_version", "—"))
            check("Build cuDNN", True, build_info.build_info.get("cudnn_version", "—"))
        except Exception:
            pass
    else:
        check("Sin GPU detectada", False,
              "Verifica drivers NVIDIA y la instalación tensorflow[and-cuda].")
        failures += 1

    # 4. Memory growth (evita que TF acapare toda la VRAM)
    section("4. Configuración de memoria")
    try:
        for g in gpus:
            tf.config.experimental.set_memory_growth(g, True)
        check("Memory growth habilitado en todas las GPUs", True)
    except Exception as e:
        check("No se pudo habilitar memory growth", False, str(e))

    # 5. Operación de prueba
    section("5. Operación de prueba en GPU")
    try:
        device = "/GPU:0" if gpu_ok else "/CPU:0"
        with tf.device(device):
            a = tf.random.normal((2048, 2048))
            b = tf.random.normal((2048, 2048))
            c = tf.linalg.matmul(a, b)
            norm = float(tf.norm(c))
        check(f"Mat-mul 2048×2048 en {device}", True, f"resultado norma {norm:.2e}")
    except Exception as e:
        check("Falló la operación de prueba", False, str(e))
        failures += 1

    # 6. Carga de modelo pre-entrenado
    section("6. Carga de modelo pre-entrenado")
    try:
        from tensorflow.keras.applications import ResNet50
        model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        n_params = model.count_params() / 1e6
        check("ResNet-50 pre-entrenado", True, f"{n_params:.2f} M parámetros")
    except Exception as e:
        check("No se pudo cargar ResNet-50", False, str(e))
        failures += 1

    # 7. Librerías auxiliares
    section("7. Librerías auxiliares")
    libs = ["numpy", "pandas", "sklearn", "PIL", "matplotlib", "tqdm", "yaml", "cv2", "albumentations"]
    for lib in libs:
        try:
            __import__(lib)
            check(lib, True)
        except Exception:
            check(lib, False, "no instalada (puede ser opcional)")

    # Resumen
    section("Resumen")
    if failures == 0:
        print("\n  🎉  Entorno TensorFlow listo. Ya puedes empezar a entrenar.\n")
        return 0
    else:
        print(f"\n  ⚠️   Hay {failures} problema(s) crítico(s) que resolver.\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
