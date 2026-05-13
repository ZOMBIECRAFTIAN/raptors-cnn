"""
Verificación del entorno PyTorch.

Corre con:
    conda activate raptors-pt
    python verify_setup.py

Verifica:
    1. Versión de Python.
    2. Versiones de PyTorch y torchvision.
    3. Disponibilidad de CUDA y nombre de la GPU.
    4. Capacidad de crear un tensor en GPU y hacer una operación básica.
    5. Carga de un modelo pre-entrenado de torchvision (ResNet50).
    6. Disponibilidad de librerías auxiliares (timm, grad-cam, sklearn, etc.).
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

    # 2. PyTorch
    section("2. PyTorch")
    try:
        import torch
        check(f"torch {torch.__version__}", True)
        import torchvision
        check(f"torchvision {torchvision.__version__}", True)
    except Exception as e:
        check("torch / torchvision no se pudieron importar", False, str(e))
        return 1

    # 3. CUDA / GPU
    section("3. CUDA y GPU NVIDIA")
    cuda_ok = torch.cuda.is_available()
    check("torch.cuda.is_available()", cuda_ok)
    if cuda_ok:
        check(f"GPU detectada", True, torch.cuda.get_device_name(0))
        check(f"Versión de CUDA con que se compiló PyTorch", True, torch.version.cuda or "—")
        check(f"cuDNN habilitado", torch.backends.cudnn.is_available(),
              str(torch.backends.cudnn.version()))
        try:
            free_b, total_b = torch.cuda.mem_get_info(0)
            check("Memoria GPU", True,
                  f"{free_b / 1e9:.1f} GB libres de {total_b / 1e9:.1f} GB totales")
        except Exception:
            pass
    else:
        check("GPU NVIDIA no detectada", False,
              "El entrenamiento será mucho más lento. Verifica drivers / instalación CUDA.")
        failures += 1

    # 4. Operación de prueba en GPU
    section("4. Operación de prueba")
    try:
        device = torch.device("cuda" if cuda_ok else "cpu")
        a = torch.randn(2048, 2048, device=device)
        b = torch.randn(2048, 2048, device=device)
        c = a @ b
        check(f"Multiplicación de matrices 2048×2048 en {device}", True,
              f"resultado shape {tuple(c.shape)}, norma {c.norm().item():.2e}")
    except Exception as e:
        check("Falló la operación de prueba", False, str(e))
        failures += 1

    # 5. Modelo pre-entrenado
    section("5. Carga de modelo pre-entrenado")
    try:
        from torchvision.models import resnet50, ResNet50_Weights
        model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
        n_params = sum(p.numel() for p in model.parameters()) / 1e6
        check(f"ResNet-50 pre-entrenado en ImageNet", True, f"{n_params:.2f} M parámetros")
    except Exception as e:
        check("No se pudo cargar ResNet-50", False, str(e))
        failures += 1

    # 6. Librerías auxiliares
    section("6. Librerías auxiliares")
    libs = [
        "numpy", "pandas", "sklearn", "PIL", "matplotlib",
        "tqdm", "yaml", "cv2",
        "timm", "albumentations", "pytorch_grad_cam",
    ]
    for lib in libs:
        try:
            __import__(lib)
            check(lib, True)
        except Exception:
            check(lib, False, "no instalada (puede ser opcional)")

    # Resumen
    section("Resumen")
    if failures == 0:
        print("\n  🎉  Entorno PyTorch listo. Ya puedes empezar a entrenar.\n")
        return 0
    else:
        print(f"\n  ⚠️   Hay {failures} problema(s) crítico(s) que resolver antes de entrenar.\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
