"""
selector_galeria_gui.py - Selector manual de imagenes para la Species Guide

Mini app Tkinter que recorre las 53 especies del proyecto y, para cada
una, te muestra en grid TODAS las fotos disponibles en
datos/processed/train/{especie}/. Haces click en la que quieres usar
para la galeria y el script:

  1) la redimensiona a 600 px de ancho (manteniendo proporcion)
  2) la guarda como JPG optimizado en
     codigo/pytorch/app_flask/static/img/species/{especie}.jpg
  3) avanza automaticamente a la siguiente especie

Atajos de teclado:
    [Enter]        -> selecciona la primera imagen visible (rapido)
    [Espacio]      -> saltar especie (no asigna nada, queda como esta)
    [Flecha izq]   -> volver a la especie anterior
    [Flecha der]   -> siguiente especie
    [E]            -> abrir la carpeta de la especie en el Explorador (Windows)
    [Esc]          -> cerrar app

Uso:
    python scripts/dataset/selector_galeria_gui.py
    python scripts/dataset/selector_galeria_gui.py --only-missing
    python scripts/dataset/selector_galeria_gui.py --start Buteo_jamaicensis
    python scripts/dataset/selector_galeria_gui.py --thumb 180

Requiere: Pillow (ya esta en environment.yml). Tkinter viene con Python.

Autor: Brian Fernandez Baez - mayo 2026
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image, ImageTk
except ImportError:
    print("ERROR: falta Pillow. Instala con:  pip install Pillow")
    sys.exit(1)

import tkinter as tk
from tkinter import ttk, messagebox

VALID_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
ROOT = Path(__file__).resolve().parents[2]


def cargar_lista_especies() -> list[str]:
    """Lee config.SPECIES sin importar torch (solo regex)."""
    import re
    cfg = ROOT / "codigo" / "pytorch" / "config.py"
    if not cfg.exists():
        messagebox.showerror("Error", f"No encuentro {cfg}")
        sys.exit(1)
    text = cfg.read_text(encoding="utf-8")
    m = re.search(r"SPECIES\s*=\s*\[(.*?)\]", text, re.DOTALL)
    if not m:
        messagebox.showerror("Error", "No pude parsear SPECIES en config.py")
        sys.exit(1)
    return sorted(set(re.findall(r"['\"]([A-Za-z_]+)['\"]", m.group(1))))


def listar_imagenes(carpeta: Path) -> list[Path]:
    if not carpeta.exists():
        return []
    return sorted([p for p in carpeta.iterdir()
                   if p.is_file() and p.suffix.lower() in VALID_EXT],
                  key=lambda p: p.stat().st_size, reverse=True)


# ============================================================================
class App(tk.Tk):
    """Selector visual de imagenes para la galeria de la GUI Flask."""

    def __init__(self, especies: list[str], src_root: Path, dst_root: Path,
                 thumb: int = 160, only_missing: bool = False,
                 start: str | None = None):
        super().__init__()
        self.title("Selector de galeria - raptors-cnn")
        self.geometry("1300x820")
        self.configure(bg="#1F3A5F")

        self.especies_all = especies
        self.src_root = src_root
        self.dst_root = dst_root
        self.dst_root.mkdir(parents=True, exist_ok=True)
        self.thumb = thumb
        self.only_missing = only_missing

        # Filtra especies si --only-missing
        if only_missing:
            self.especies = [s for s in especies
                             if not (dst_root / f"{s}.jpg").exists()]
            if not self.especies:
                messagebox.showinfo("Listo", "Todas las especies ya tienen imagen.")
                self.destroy()
                return
        else:
            self.especies = list(especies)

        # Indice inicial
        self.idx = 0
        if start and start in self.especies:
            self.idx = self.especies.index(start)

        self._thumbs_refs: list[ImageTk.PhotoImage] = []
        self._build_ui()
        self._render_especie()

        # Atajos de teclado
        self.bind("<Return>", lambda e: self._seleccionar_primera())
        self.bind("<space>", lambda e: self._siguiente())
        self.bind("<Right>", lambda e: self._siguiente())
        self.bind("<Left>", lambda e: self._anterior())
        self.bind("<e>", lambda e: self._abrir_carpeta())
        self.bind("<E>", lambda e: self._abrir_carpeta())
        self.bind("<Escape>", lambda e: self.destroy())

    # ----- UI build -----
    def _build_ui(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", padding=6, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#1F3A5F",
                        foreground="white", font=("Segoe UI", 16, "bold"))
        style.configure("Sub.TLabel", background="#1F3A5F",
                        foreground="#A8C7E8", font=("Segoe UI", 11))
        style.configure("Info.TLabel", background="#1F3A5F",
                        foreground="#FFD680", font=("Segoe UI", 10, "italic"))

        # Header
        header = tk.Frame(self, bg="#1F3A5F")
        header.pack(fill=tk.X, padx=18, pady=(14, 6))

        self.lbl_title = ttk.Label(header, text="", style="Header.TLabel")
        self.lbl_title.pack(side=tk.LEFT)
        self.lbl_progress = ttk.Label(header, text="", style="Sub.TLabel")
        self.lbl_progress.pack(side=tk.RIGHT)

        self.lbl_sub = ttk.Label(self, text="", style="Sub.TLabel")
        self.lbl_sub.pack(fill=tk.X, padx=18, pady=(0, 4))

        self.lbl_hint = ttk.Label(
            self,
            text=("Click en una imagen para usarla en la galeria. "
                  "Atajos: [Enter]=primera  [Espacio/->]=saltar  "
                  "[<-]=anterior  [E]=abrir carpeta  [Esc]=salir"),
            style="Info.TLabel")
        self.lbl_hint.pack(fill=tk.X, padx=18, pady=(0, 8))

        # Scrollable grid
        cont = tk.Frame(self, bg="#1F3A5F")
        cont.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 8))

        self.canvas = tk.Canvas(cont, bg="#1F3A5F",
                                highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(cont, orient=tk.VERTICAL,
                               command=self.canvas.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scroll.set)

        self.grid_frame = tk.Frame(self.canvas, bg="#1F3A5F")
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.grid_frame, anchor="nw")

        self.grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self.canvas_window, width=e.width))
        # Scroll con rueda
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Footer botones
        footer = tk.Frame(self, bg="#1F3A5F")
        footer.pack(fill=tk.X, padx=18, pady=(0, 14))

        ttk.Button(footer, text="<- Anterior", command=self._anterior).pack(side=tk.LEFT)
        ttk.Button(footer, text="Saltar / Siguiente ->",
                   command=self._siguiente).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(footer, text="Abrir carpeta (E)",
                   command=self._abrir_carpeta).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(footer, text="Cerrar (Esc)",
                   command=self.destroy).pack(side=tk.RIGHT)

    def _on_mousewheel(self, event) -> None:
        delta = -1 * int(event.delta / 120)
        self.canvas.yview_scroll(delta, "units")

    # ----- Render -----
    def _render_especie(self) -> None:
        if self.idx >= len(self.especies):
            messagebox.showinfo("Listo",
                                "Terminaste de revisar todas las especies.")
            self.destroy()
            return

        sp = self.especies[self.idx]
        sp_dir = self.src_root / sp
        files = listar_imagenes(sp_dir)
        existente = self.dst_root / f"{sp}.jpg"

        n_total_global = len(self.especies_all)
        actual_global = self.especies_all.index(sp) + 1
        sufijo = " (*ya tiene)" if existente.exists() else ""
        self.lbl_title.config(text=f"{sp}{sufijo}")
        self.lbl_progress.config(
            text=f"{self.idx + 1} / {len(self.especies)}   "
                 f"(global {actual_global}/{n_total_global})")
        self.lbl_sub.config(
            text=f"Carpeta: {sp_dir}   |   {len(files)} imagen(es) disponibles")

        # Limpia grid previo
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self._thumbs_refs.clear()

        if not files:
            tk.Label(self.grid_frame,
                     text=("Esta especie no tiene imagenes en el dataset.\n"
                           "Usa scripts\\windows\\descargar_v1_1.bat "
                           "<CODIGO> para descargar."),
                     bg="#1F3A5F", fg="#FFD680",
                     font=("Segoe UI", 12)).pack(pady=40)
            return

        # Grid de thumbnails (4 columnas)
        cols = 5
        for i, fp in enumerate(files):
            try:
                with Image.open(fp) as im:
                    im = im.convert("RGB")
                    im.thumbnail((self.thumb, self.thumb), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(im)
            except Exception:
                continue
            self._thumbs_refs.append(photo)

            cell = tk.Frame(self.grid_frame, bg="#2E5985",
                            highlightbackground="#A8C7E8",
                            highlightthickness=1)
            cell.grid(row=i // cols, column=i % cols, padx=6, pady=6,
                      sticky="nsew")

            btn = tk.Button(cell, image=photo,
                            command=lambda p=fp: self._seleccionar(p),
                            bg="#2E5985", activebackground="#FFD680",
                            bd=0, cursor="hand2")
            btn.pack(padx=4, pady=4)

            cap = tk.Label(cell, text=fp.name[:28],
                           bg="#2E5985", fg="white",
                           font=("Consolas", 8))
            cap.pack(pady=(0, 2))

        # Marca la actual si existe
        if existente.exists():
            tk.Label(
                self.grid_frame,
                text=f"NOTA: ya hay una imagen seleccionada para esta especie. "
                     f"Si haces click en otra, la sobreescribe.",
                bg="#1F3A5F", fg="#FFD680", font=("Segoe UI", 10, "italic")
            ).grid(row=(len(files) // cols) + 1, column=0, columnspan=cols, pady=8)

        self.canvas.yview_moveto(0.0)

    # ----- Acciones -----
    def _seleccionar(self, src_path: Path) -> None:
        sp = self.especies[self.idx]
        dst = self.dst_root / f"{sp}.jpg"
        try:
            with Image.open(src_path) as im:
                im = im.convert("RGB")
                w, h = im.size
                target_w = 600
                if w > target_w:
                    nuevo_h = int(h * (target_w / w))
                    im = im.resize((target_w, nuevo_h), Image.LANCZOS)
                im.save(dst, "JPEG", quality=88, optimize=True)
        except Exception as e:
            messagebox.showerror("Error al guardar",
                                 f"No pude procesar la imagen:\n{e}")
            return
        # avanza
        self._siguiente()

    def _seleccionar_primera(self) -> None:
        sp = self.especies[self.idx]
        files = listar_imagenes(self.src_root / sp)
        if files:
            self._seleccionar(files[0])

    def _siguiente(self) -> None:
        self.idx += 1
        self._render_especie()

    def _anterior(self) -> None:
        if self.idx > 0:
            self.idx -= 1
            self._render_especie()

    def _abrir_carpeta(self) -> None:
        sp = self.especies[self.idx]
        ruta = (self.src_root / sp).resolve()
        if not ruta.exists():
            messagebox.showwarning("Aviso", f"La carpeta {ruta} no existe.")
            return
        try:
            if sys.platform.startswith("win"):
                os.startfile(str(ruta))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(ruta)])
            else:
                subprocess.Popen(["xdg-open", str(ruta)])
        except Exception as e:
            messagebox.showerror("Error", f"No pude abrir el explorador:\n{e}")


# ============================================================================
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Selector visual de imagenes para la Species Guide.")
    ap.add_argument("--source", default="datos/processed/train",
                    help="Carpeta fuente con subcarpetas por especie")
    ap.add_argument("--dest", default="codigo/pytorch/app_flask/static/img/species",
                    help="Carpeta destino de la galeria")
    ap.add_argument("--thumb", type=int, default=160,
                    help="Tamano del thumbnail en pixeles (default 160)")
    ap.add_argument("--only-missing", action="store_true",
                    help="Mostrar solo especies que aun no tienen imagen")
    ap.add_argument("--start",
                    help="Empezar desde una especie especifica (e.g. Buteo_jamaicensis)")
    args = ap.parse_args()

    especies = cargar_lista_especies()
    src = Path(args.source)
    dst = Path(args.dest)
    if not src.is_absolute():
        src = ROOT / src
    if not dst.is_absolute():
        dst = ROOT / dst
    src = src.resolve()
    dst = dst.resolve()

    if not src.exists():
        print(f"ERROR: no existe la carpeta fuente {src}")
        sys.exit(1)

    app = App(especies, src, dst, thumb=args.thumb,
              only_missing=args.only_missing, start=args.start)
    app.mainloop()


if __name__ == "__main__":
    main()
