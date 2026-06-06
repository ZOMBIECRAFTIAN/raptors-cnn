"""
comparar_arquitecturas.py

Orquesta la comparativa formal de las 4 arquitecturas CNN del proyecto sobre
las 53 especies de rapaces diurnas de Mexico:

    - ResNet-50          (baseline maduro, 25.6 M params)
    - EfficientNet-B3    (mejor accuracy-por-param, 12.2 M params)
    - MobileNetV3-Large  (lightweight para movil/edge, 5.5 M params)
    - ConvNeXt-Tiny      (SOTA 2022, 28.6 M params)

Uso:
    python comparar_arquitecturas.py --train         # entrena las 4 en serie (largo)
    python comparar_arquitecturas.py --evaluate      # evalua si los pesos ya existen
    python comparar_arquitecturas.py --report        # solo genera CSV + figuras
    python comparar_arquitecturas.py --all           # train + evaluate + report
    python comparar_arquitecturas.py --arch resnet50 --train   # solo una

Produce:
    metricas_arquitecturas.csv
    figures/
        accuracy_por_arquitectura.png
        f1_macro_vs_parametros.png
        latencia_vs_accuracy.png
        confusion_matrix_<arch>.png

Requiere: el entorno raptors-pt activo y haber corrido el split del dataset.
Tiempo: ~4-8 horas por arquitectura en RTX 3050 (16-32 horas las 4 en serie).

Autor: Brian Fernandez Baez - mayo 2026
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

# Importes seguros: si torch no existe (lectura desde otros lados), no rompe.
try:
    import torch
    TORCH_OK = True
except ImportError:
    TORCH_OK = False

ROOT = Path(__file__).resolve().parents[2]
PYTORCH_DIR = ROOT / "codigo" / "pytorch"
OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUT_DIR / "metricas_arquitecturas.csv"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

ARQUITECTURAS = ["resnet50", "efficientnet_b3", "mobilenet_v3_large", "convnext_tiny"]

# Metadatos a priori (de Torchvision / papers)
META = {
    "resnet50":           {"params_M": 25.6, "input": 224, "flops_G": 4.1, "imagenet_acc": 80.4},
    "efficientnet_b3":    {"params_M": 12.2, "input": 300, "flops_G": 1.8, "imagenet_acc": 81.6},
    "mobilenet_v3_large": {"params_M":  5.5, "input": 224, "flops_G": 0.22, "imagenet_acc": 75.2},
    "convnext_tiny":      {"params_M": 28.6, "input": 232, "flops_G": 4.5, "imagenet_acc": 82.1},
}


# ---------------------------------------------------------------------------
def run_cmd(args: list[str]) -> int:
    """Ejecuta un comando python en codigo/pytorch/ y devuelve el exitcode."""
    print(f"\n>>> {' '.join(args)}\n")
    proc = subprocess.run(args, cwd=str(PYTORCH_DIR))
    return proc.returncode


def entrenar(arch: str) -> dict:
    """Entrena una arquitectura y mide tiempo + VRAM."""
    print(f"\n{'=' * 70}\n  ENTRENANDO {arch}\n{'=' * 70}")
    t0 = time.time()
    vram_max = 0.0

    if TORCH_OK and torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    code = run_cmd([sys.executable, "train.py", "--arch", arch])

    elapsed_h = (time.time() - t0) / 3600.0
    if TORCH_OK and torch.cuda.is_available():
        vram_max = torch.cuda.max_memory_allocated() / (1024 ** 3)

    return {
        "arch": arch,
        "train_status": "OK" if code == 0 else "FAIL",
        "train_hours": round(elapsed_h, 2),
        "vram_GB": round(vram_max, 2) if vram_max else None,
    }


def evaluar(arch: str) -> dict:
    """Evalua una arquitectura ya entrenada. Asume best_stage2.pt."""
    print(f"\n{'=' * 70}\n  EVALUANDO {arch}\n{'=' * 70}")
    ckpt_dir = PYTORCH_DIR / "outputs" / "checkpoints"
    weights = ckpt_dir / f"best_stage2_{arch}.pt"
    if not weights.exists():
        weights = ckpt_dir / "best_stage2.pt"
    if not weights.exists():
        print(f"  WARNING: no hay pesos en {weights} - saltando")
        return {"arch": arch, "eval_status": "NO_WEIGHTS"}

    code = run_cmd([sys.executable, "evaluate.py", "--arch", arch,
                    "--weights", str(weights)])

    # Leer outputs/metrics_<arch>.json si evaluate.py lo produce
    metrics_json = PYTORCH_DIR / "outputs" / f"metrics_{arch}.json"
    res = {"arch": arch, "eval_status": "OK" if code == 0 else "FAIL"}
    if metrics_json.exists():
        try:
            data = json.loads(metrics_json.read_text(encoding="utf-8"))
            res.update({
                "accuracy":    data.get("accuracy"),
                "f1_macro":    data.get("f1_macro"),
                "top3_acc":    data.get("top3_accuracy"),
                "model_size_MB": data.get("model_size_mb", data.get("model_size_MB")),
                "latency_ms":  data.get("latency_ms_per_image"),
            })
        except Exception as e:
            print(f"  WARNING: error leyendo {metrics_json.name}: {e}")
    return res


def cargar_o_inicializar_csv() -> dict[str, dict]:
    """Carga el CSV existente o devuelve dict vacio."""
    if not CSV_PATH.exists():
        return {arch: {"arch": arch, **META[arch]} for arch in ARQUITECTURAS}
    import csv
    out: dict[str, dict] = {}
    with CSV_PATH.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["arch"]] = row
    for arch in ARQUITECTURAS:
        if arch not in out:
            out[arch] = {"arch": arch, **META[arch]}
    return out


def guardar_csv(filas: dict[str, dict]) -> None:
    import csv
    columnas = ["arch", "params_M", "input", "flops_G", "imagenet_acc",
                "accuracy", "f1_macro", "top3_acc",
                "train_status", "train_hours", "vram_GB",
                "model_size_MB", "latency_ms", "eval_status"]
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        for arch in ARQUITECTURAS:
            w.writerow(filas[arch])
    print(f"\n  CSV escrito: {CSV_PATH}")


def generar_figuras(filas: dict[str, dict]) -> None:
    """Genera las figuras comparativas."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  WARNING: matplotlib no disponible, omito figuras.")
        return

    archs = ARQUITECTURAS
    nombres = [a.replace("_", "-") for a in archs]

    # Fig 1: accuracy por arquitectura (test set del proyecto + ImageNet de referencia)
    fig, ax = plt.subplots(figsize=(9, 5))
    x = list(range(len(archs)))
    acc_proj = [_to_float(filas[a].get("accuracy")) for a in archs]
    acc_im = [_to_float(filas[a].get("imagenet_acc")) for a in archs]
    ax.bar([i - 0.2 for i in x], acc_proj, 0.4, label="Rapaces (test)", color="#2E5985")
    ax.bar([i + 0.2 for i in x], acc_im, 0.4, label="ImageNet (referencia)", color="#A8C7E8")
    ax.set_xticks(x); ax.set_xticklabels(nombres, rotation=15, ha="right")
    ax.set_ylabel("Accuracy (%)"); ax.set_ylim(0, 100)
    ax.set_title("Accuracy por arquitectura - 53 rapaces de Mexico")
    ax.legend(); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "accuracy_por_arquitectura.png", dpi=140)
    plt.close(fig)

    # Fig 2: F1-macro vs parametros (eficiencia)
    fig, ax = plt.subplots(figsize=(8, 5))
    for a in archs:
        x_val = _to_float(filas[a].get("params_M"))
        y_val = _to_float(filas[a].get("f1_macro"))
        ax.scatter(x_val, y_val, s=200, alpha=0.7)
        ax.annotate(a.replace("_", "-"), (x_val, y_val),
                    textcoords="offset points", xytext=(8, 6), fontsize=9)
    ax.set_xlabel("Parametros (millones)"); ax.set_ylabel("F1-macro sobre rapaces")
    ax.set_title("Eficiencia: F1-macro vs. parametros del modelo")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "f1_macro_vs_parametros.png", dpi=140)
    plt.close(fig)

    # Fig 3: latencia vs accuracy (trade-off Pareto)
    fig, ax = plt.subplots(figsize=(8, 5))
    for a in archs:
        x_val = _to_float(filas[a].get("latency_ms"))
        y_val = _to_float(filas[a].get("accuracy"))
        ax.scatter(x_val, y_val, s=200, alpha=0.7)
        ax.annotate(a.replace("_", "-"), (x_val, y_val),
                    textcoords="offset points", xytext=(8, 6), fontsize=9)
    ax.set_xlabel("Latencia inferencia (ms/imagen)")
    ax.set_ylabel("Accuracy sobre rapaces (%)")
    ax.set_title("Trade-off Pareto: velocidad vs. precision")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "latencia_vs_accuracy.png", dpi=140)
    plt.close(fig)

    print(f"  Figuras escritas en {FIG_DIR}")


def _to_float(x) -> float:
    """Convierte a float o devuelve 0 si no puede."""
    try:
        return float(x) if x not in (None, "", "None") else 0.0
    except (TypeError, ValueError):
        return 0.0


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Comparativa de las 4 arquitecturas CNN del proyecto.")
    ap.add_argument("--train", action="store_true",
                    help="Entrenar las 4 arquitecturas en serie")
    ap.add_argument("--evaluate", action="store_true",
                    help="Evaluar arquitecturas ya entrenadas")
    ap.add_argument("--report", action="store_true",
                    help="Solo generar CSV + figuras desde resultados existentes")
    ap.add_argument("--all", action="store_true",
                    help="Equivale a --train --evaluate --report")
    ap.add_argument("--arch", choices=ARQUITECTURAS,
                    help="Solo procesar una arquitectura especifica")
    args = ap.parse_args()

    if args.all:
        args.train = args.evaluate = args.report = True
    if not any([args.train, args.evaluate, args.report]):
        ap.print_help()
        return

    archs = [args.arch] if args.arch else ARQUITECTURAS
    filas = cargar_o_inicializar_csv()

    if args.train:
        for a in archs:
            r = entrenar(a)
            filas[a].update(r)
            guardar_csv(filas)

    if args.evaluate:
        for a in archs:
            r = evaluar(a)
            filas[a].update(r)
            guardar_csv(filas)

    if args.report:
        generar_figuras(filas)
        print(f"\n{'=' * 70}\n  Reporte completo\n{'=' * 70}")
        print(f"  CSV:      {CSV_PATH}")
        print(f"  Figuras:  {FIG_DIR}")


if __name__ == "__main__":
    main()
