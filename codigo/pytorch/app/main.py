"""
App Gradio del proyecto raptors-cnn.

Tres pestañas:
   1. Identificar imagen — upload PNG/JPG, predicción + Grad-CAM + seña
   2. Identificar video — upload MP4, procesamiento frame-by-frame + timeline
   3. Catálogo de señas — grid con las 14 especies y sus señas en IS

Uso:
    conda activate raptors-pt
    cd codigo/pytorch
    python -m app.main

Abre automáticamente http://127.0.0.1:7860 en el navegador.
"""
from __future__ import annotations
from pathlib import Path

import gradio as gr
from PIL import Image

from .config_app import (
    APP_TITLE, APP_DESCRIPTION, THEME_PRIMARY, THEME_ACCENT,
    SPECIES_DATA, SPECIES_ORDER,
    VIDEO_SAMPLE_EVERY_SECS, VIDEO_MAX_DURATION_SECS,
)
from .inference import get_classifier
from .video_processor import process_video
from .signs import get_sign_for_species
from .feedback import record_feedback, get_feedback_stats
from .observations import save_observation, get_observation_stats


# ============================================================================
#   Handlers de cada tab
# ============================================================================
def handle_image(image_pil: Image.Image | None):
    """Tab 1 — predicción sobre imagen subida. Devuelve también estados para Tab 4."""
    if image_pil is None:
        return (None, "Sube una imagen para identificar.", None, None, None,
                None, "", "", 0.0, None)  # 4 estados extra al final

    clf = get_classifier()
    if not clf.loaded:
        return (None, "❌ Modelo no cargado. Entrena primero con `python train.py --smoke-test`.",
                None, None, None, None, "", "", 0.0, None)

    pred = clf.predict(image_pil, top_k=5)
    if "error" in pred:
        return None, f"❌ {pred['error']}", None, None, None, None, "", "", 0.0, None

    # Resumen de predicción
    top1 = pred["topk"][0]
    summary_md = (
        f"## 🎯 {top1['code']} — {top1['common']}\n\n"
        f"*{top1['species']}* — confianza: **{top1['prob']*100:.1f} %**\n\n"
        f"### Top-5 alternativas\n\n"
        + "\n".join([
            f"- **{p['code']}** · *{p['species']}* — {p['prob']*100:.1f} %"
            for p in pred["topk"]
        ])
    )

    # Grad-CAM
    try:
        gradcam_img = clf.gradcam(image_pil, target_idx=pred["top1_idx"])
    except Exception as e:
        gradcam_img = None
        summary_md += f"\n\n*Grad-CAM no disponible: {e}*"

    # Seña
    sign_img, sign_desc, real_video = get_sign_for_species(top1["species"])
    sign_md = f"### 🤟 Seña en International Sign\n\n{sign_desc}"

    # También devolvemos estados para que el Tab 4 (corregir) los tenga listos
    return (gradcam_img, summary_md, sign_img, sign_md, _make_probs_table(pred),
            image_pil,                       # last_image_state
            top1["species"],                 # last_pred_species
            top1["code"],                    # last_pred_code
            top1["prob"],                    # last_pred_prob
            image_pil)                       # fb_image_preview


def _make_probs_table(pred):
    """Tabla compacta de todas las probabilidades."""
    return [
        [p["code"], p["species"], p["common"], f"{p['prob']*100:.2f} %"]
        for p in pred["topk"]
    ]


def handle_video(video_path: str | None,
                 sample_every: float,
                 min_confidence: float):
    """Tab 2 — procesamiento de video."""
    if not video_path:
        return None, "Sube un video para procesar.", None, None

    result = process_video(video_path,
                           sample_every=sample_every,
                           min_confidence=min_confidence)
    if "error" in result:
        return None, f"❌ {result['error']}", None, None

    best = result["best_detection"]
    summary_md = (
        f"## 📹 Procesamiento de video — {result['duration']:.1f} s\n\n"
        f"- **Frames muestreados con detección:** {result['n_samples']}\n"
        f"- **Mejor detección global:** {best['code']} ({best['common']}) "
        f"a los {best['t']:.1f} s con {best['prob']*100:.1f} % de confianza.\n"
    )

    # Mostrar también la seña de la mejor detección
    sign_img, _, _ = get_sign_for_species(best["species"])

    return (result["timeline_image"],
            summary_md,
            result["table_rows"],
            sign_img)


def handle_feedback_confirm(image_pil, predicted_species, predicted_code, predicted_prob, notes):
    """El usuario confirma que la predicción es correcta."""
    if image_pil is None or not predicted_species:
        return "⚠️ Primero identifica una imagen en el Tab 1."
    res = record_feedback(
        pil_image=image_pil, decision="confirm",
        predicted_species=predicted_species, predicted_code=predicted_code,
        predicted_prob=float(predicted_prob) if predicted_prob else 0.0,
        user_notes=notes or "",
    )
    if res["ok"]:
        return f"✅ Confirmación guardada para **{predicted_species}** (hash {res['hash']})."
    return f"❌ Error: {res.get('error')}"


def handle_feedback_correct(image_pil, predicted_species, predicted_code, predicted_prob,
                              true_code, notes):
    """El usuario corrige diciendo la especie correcta."""
    if image_pil is None:
        return "⚠️ Primero identifica una imagen en el Tab 1."
    if not true_code:
        return "⚠️ Selecciona la especie correcta del menú."
    # Mapear código → scientific name
    true_sci = None
    for sci in SPECIES_ORDER:
        if SPECIES_DATA[sci].code == true_code:
            true_sci = sci; break
    if not true_sci:
        return f"❌ Código '{true_code}' no reconocido."
    res = record_feedback(
        pil_image=image_pil, decision="correct",
        predicted_species=predicted_species or "—", predicted_code=predicted_code or "—",
        predicted_prob=float(predicted_prob) if predicted_prob else 0.0,
        true_species=true_sci, true_code=true_code,
        user_notes=notes or "",
    )
    if res["ok"]:
        return (f"📝 Corrección guardada. Era {predicted_code or '—'} → ahora {true_code} ({true_sci}).\n\n"
                f"Cuando acumules ≥ 50 correcciones, corre `python retrain_with_feedback.py` "
                f"para mejorar el modelo.")
    return f"❌ Error: {res.get('error')}"


def handle_save_observation(image_pil, predicted_species, predicted_code, predicted_prob,
                              latitude, longitude, location, notes):
    """Guardar observación científica con coordenadas opcionales."""
    if image_pil is None or not predicted_species:
        return "⚠️ Primero identifica una imagen."
    common = "—"
    for sci in SPECIES_ORDER:
        if sci == predicted_species:
            common = SPECIES_DATA[sci].common_name_en; break
    res = save_observation(
        pil_image=image_pil,
        species_scientific=predicted_species, species_common=common,
        species_code=predicted_code or "—",
        confidence=float(predicted_prob) if predicted_prob else 0.0,
        latitude=float(latitude) if latitude not in (None, "") else None,
        longitude=float(longitude) if longitude not in (None, "") else None,
        location_name=location or "",
        notes=notes or "",
    )
    if res["ok"]:
        return (f"📍 Observación **{res['observation_id']}** guardada.\n\n"
                f"Compatible con estándar Darwin Core. "
                f"Puedes exportar el CSV para subir a iNaturalist/eBird después.")
    return f"❌ Error: {res.get('error')}"


def refresh_stats():
    """Devuelve estadísticas formateadas del feedback + observaciones."""
    fb = get_feedback_stats()
    ob = get_observation_stats()
    md = (
        f"## 📊 Estadísticas del active learning\n\n"
        f"### Feedback acumulado\n\n"
        f"- **Total:** {fb['total']} correcciones\n"
        f"- **Por tipo:** {fb['by_decision']}\n"
        f"- **Por especie:** {fb['by_species']}\n"
        f"- **¿Listo para retrain?** {'✅ Sí — corre `python retrain_with_feedback.py`' if fb.get('ready_for_retrain') else '⏳ Necesitas ≥ 50 correcciones'}\n\n"
        f"### Observaciones guardadas\n\n"
        f"- **Total:** {ob['total']} avistamientos\n"
        f"- **Con GPS:** {ob['with_gps']}  ·  **Sin GPS:** {ob.get('without_gps', 0)}\n"
        f"- **Por especie:** {ob['by_species']}\n"
    )
    return md


def show_sign_for_code(species_code: str):
    """Tab 3 — busca la especie por código y muestra su tarjeta de seña."""
    for sci, info in SPECIES_DATA.items():
        if info.code == species_code:
            img, desc, _ = get_sign_for_species(sci)
            md = (
                f"## {info.code} — {info.common_name_en}\n\n"
                f"*{info.scientific_name}* · {info.common_name_es} · "
                f"{info.family} · abundancia {info.abundance}\n\n"
                f"### 🤟 Descripción de la seña\n\n{desc}\n\n"
                f"### 🔍 Caracteres diagnósticos\n\n{info.field_marks}"
            )
            return img, md
    return None, "Especie no encontrada."


# ============================================================================
#   UI principal
# ============================================================================
def build_interface() -> gr.Blocks:
    """Construye la interfaz Gradio completa."""

    # Inicializar el clasificador en startup
    clf = get_classifier()
    load_status = "✅ Modelo cargado" if clf.loaded else "⚠️ Sin modelo (corre el smoke-test primero)"

    custom_css = """
    .gradio-container {max-width: 1400px !important; margin: auto;}
    .species-button {min-width: 80px;}
    footer {visibility: hidden;}
    """

    with gr.Blocks(theme=gr.themes.Soft(primary_hue="green", secondary_hue="orange"),
                   css=custom_css, title="raptors-cnn") as demo:

        # ----- Header -----
        gr.Markdown(f"# {APP_TITLE}")
        gr.Markdown(APP_DESCRIPTION)
        gr.Markdown(f"**Estado del modelo:** {load_status}")

        # ----- Tabs -----
        with gr.Tabs():

            # ============================================
            # TAB 1 — Identificar imagen
            # ============================================
            with gr.Tab("📷 Identificar imagen"):
                gr.Markdown("Sube una fotografía de un ave rapaz **en vuelo** y el modelo intentará identificarla.")
                with gr.Row():
                    with gr.Column(scale=1):
                        img_input = gr.Image(label="Imagen de entrada",
                                              type="pil", height=400)
                        img_btn = gr.Button("🦅 Identificar", variant="primary", size="lg")
                    with gr.Column(scale=1):
                        img_gradcam = gr.Image(label="Grad-CAM — dónde 'mira' el modelo", height=400)

                with gr.Row():
                    with gr.Column(scale=2):
                        img_summary = gr.Markdown(label="Resultado")
                        img_probs_table = gr.Dataframe(
                            headers=["Código", "Nombre científico", "Nombre común", "Probabilidad"],
                            label="Top-5 predicciones",
                            interactive=False,
                            wrap=True,
                        )
                    with gr.Column(scale=1):
                        img_sign = gr.Image(label="🤟 Seña en International Sign", height=400)
                        img_sign_md = gr.Markdown()

                # NOTA: el click se conecta DESPUÉS de definir los estados del Tab 4.
                # Lo hacemos al final del build_interface().
                img_btn_handle = (img_btn, img_input,
                                  [img_gradcam, img_summary, img_sign, img_sign_md, img_probs_table])

            # ============================================
            # TAB 2 — Identificar video
            # ============================================
            with gr.Tab("📹 Identificar video"):
                gr.Markdown(
                    f"Sube un video corto (máx **{VIDEO_MAX_DURATION_SECS} segundos**). "
                    f"El sistema extrae un frame cada N segundos y predice la especie."
                )
                with gr.Row():
                    with gr.Column(scale=1):
                        vid_input = gr.Video(label="Video de entrada",
                                              height=300)
                        vid_sample = gr.Slider(0.5, 5.0, value=VIDEO_SAMPLE_EVERY_SECS,
                                                step=0.5, label="Muestrear 1 frame cada (segundos)")
                        vid_conf = gr.Slider(0.0, 1.0, value=0.30, step=0.05,
                                              label="Umbral mínimo de confianza")
                        vid_btn = gr.Button("📹 Procesar video", variant="primary")
                    with gr.Column(scale=1):
                        vid_sign = gr.Image(label="🤟 Seña de la mejor detección", height=400)

                vid_summary = gr.Markdown()
                vid_timeline = gr.Image(label="Timeline de detecciones")
                vid_table = gr.Dataframe(
                    headers=["Tiempo", "Código", "Nombre común", "Nombre científico", "Confianza"],
                    label="Detecciones por frame",
                    wrap=True,
                )

                vid_btn.click(
                    handle_video,
                    inputs=[vid_input, vid_sample, vid_conf],
                    outputs=[vid_timeline, vid_summary, vid_table, vid_sign],
                )

            # ============================================
            # TAB 3 — Catálogo de señas
            # ============================================
            with gr.Tab("🤟 Catálogo de señas IS"):
                gr.Markdown(
                    "Catálogo preliminar de **14 señas en International Sign** para las especies "
                    "objetivo. Las descripciones provienen del diseño original del autor "
                    "(co-creación con la comunidad sorda en curso)."
                )
                # Botones de las 14 especies
                with gr.Row():
                    cards = []
                    for sci in SPECIES_ORDER:
                        info = SPECIES_DATA[sci]
                        cards.append(gr.Button(f"{info.code}\n{info.common_name_en}",
                                               size="sm", elem_classes="species-button"))

                sign_img_display = gr.Image(label="Tarjeta de la seña", height=500)
                sign_md_display = gr.Markdown()

                # Hooks de cada botón
                for btn, sci in zip(cards, SPECIES_ORDER):
                    info = SPECIES_DATA[sci]
                    btn.click(
                        lambda code=info.code: show_sign_for_code(code),
                        outputs=[sign_img_display, sign_md_display],
                    )

            # ============================================
            # TAB 4 — Corregir y aprender (active learning)
            # ============================================
            with gr.Tab("🎓 Corregir y aprender"):
                gr.Markdown(
                    "### Active learning\n\n"
                    "Si el modelo se equivocó en el Tab 1, ayúdale a aprender corrigiéndolo. "
                    "Tus correcciones se guardan en `datos/feedback/` y cuando acumules **≥ 50**, "
                    "puedes correr `python retrain_with_feedback.py` para mejorar el modelo "
                    "(fine-tuning incremental sin olvidar lo que ya sabe).\n\n"
                    "**Importante:** primero identifica una imagen en el Tab 1; aquí se evalúa esa última predicción."
                )

                # Estados que recuerdan la última predicción del Tab 1
                last_image_state = gr.State(None)
                last_pred_species = gr.State("")
                last_pred_code = gr.State("")
                last_pred_prob = gr.State(0.0)

                with gr.Row():
                    fb_image_preview = gr.Image(label="Última imagen identificada",
                                                  height=300, interactive=False)
                    fb_notes = gr.Textbox(label="Notas (opcional)",
                                          placeholder="Comentarios, ubicación, condiciones de luz, etc.",
                                          lines=5)

                with gr.Row():
                    btn_confirm = gr.Button("✅ La identificación es correcta",
                                              variant="primary")

                gr.Markdown("**O corrige diciendo cuál es la especie real:**")
                with gr.Row():
                    correct_code = gr.Dropdown(
                        choices=[f"{SPECIES_DATA[s].code} — {SPECIES_DATA[s].common_name_en}"
                                 for s in SPECIES_ORDER],
                        label="Especie correcta",
                        info="Selecciona la especie que realmente aparece en la foto",
                    )
                    btn_correct = gr.Button("📝 Esta es la especie correcta",
                                              variant="secondary")

                fb_result_md = gr.Markdown()

                # Guardar observación científica (con GPS opcional)
                gr.Markdown("---")
                gr.Markdown("### 📍 Guardar como observación científica")
                gr.Markdown(
                    "Registra esta identificación como un avistamiento formal "
                    "(compatible con Darwin Core, exportable a iNaturalist/eBird)."
                )
                with gr.Row():
                    obs_lat = gr.Number(label="Latitud (opcional)", precision=6)
                    obs_lon = gr.Number(label="Longitud (opcional)", precision=6)
                with gr.Row():
                    obs_loc = gr.Textbox(label="Lugar (opcional)",
                                          placeholder="Ej. Cardel, Veracruz")
                btn_save_obs = gr.Button("💾 Guardar observación", variant="primary")
                obs_result_md = gr.Markdown()

                # Wiring de los handlers
                btn_confirm.click(
                    handle_feedback_confirm,
                    inputs=[last_image_state, last_pred_species, last_pred_code,
                            last_pred_prob, fb_notes],
                    outputs=[fb_result_md],
                )

                def _correct_with_code_extraction(image, pred_sp, pred_code, pred_prob, dropdown_value, notes):
                    code = (dropdown_value or "").split(" ")[0] if dropdown_value else ""
                    return handle_feedback_correct(image, pred_sp, pred_code, pred_prob, code, notes)

                btn_correct.click(
                    _correct_with_code_extraction,
                    inputs=[last_image_state, last_pred_species, last_pred_code,
                            last_pred_prob, correct_code, fb_notes],
                    outputs=[fb_result_md],
                )

                btn_save_obs.click(
                    handle_save_observation,
                    inputs=[last_image_state, last_pred_species, last_pred_code,
                            last_pred_prob, obs_lat, obs_lon, obs_loc, fb_notes],
                    outputs=[obs_result_md],
                )

            # --- conectar el click del Tab 1 AHORA que existen los estados del Tab 4 ---
            img_btn.click(
                handle_image,
                inputs=[img_input],
                outputs=[
                    img_gradcam, img_summary, img_sign, img_sign_md, img_probs_table,
                    last_image_state, last_pred_species, last_pred_code, last_pred_prob,
                    fb_image_preview,
                ],
            )

            # ============================================
            # TAB 5 — Estadísticas
            # ============================================
            with gr.Tab("📊 Estadísticas"):
                gr.Markdown("Resumen del uso de la app y datos acumulados para retraining.")
                stats_md = gr.Markdown(refresh_stats())
                btn_refresh = gr.Button("🔄 Actualizar")
                btn_refresh.click(lambda: refresh_stats(), outputs=[stats_md])

            # ============================================
            # TAB 6 — Acerca de
            # ============================================
            with gr.Tab("ℹ️ Acerca de"):
                gr.Markdown(f"""
## Acerca del proyecto

**raptors-cnn** — Sistema integrado de identificación automatizada de aves rapaces migratorias
del corredor de Veracruz, integrado con un catálogo de señas en International Sign para inclusión
de la comunidad sorda.

### Características técnicas

- **Arquitectura ML:** CNN ResNet-50 con transfer learning desde ImageNet, fine-tuned sobre
  imágenes de rapaces en vuelo (14 especies objetivo).
- **Interpretabilidad:** Grad-CAM (Selvaraju et al., 2017) como verificación visual de que
  el modelo atiende a caracteres morfológicos diagnósticos.
- **Inclusión:** catálogo de 14 señas en International Sign co-creado con la comunidad sorda,
  validado con escala Likert sobre claridad, naturalidad y memorabilidad.

### Estado actual

⚠️ **Esta demo usa el modelo del smoke-test entrenado con dataset sintético.** Las predicciones
NO son científicamente válidas todavía — solo verifican que el pipeline funciona end-to-end.
Cuando se entrene con dataset real (≥200 imgs por especie), las predicciones serán confiables.

### Autoría y contacto

**Brian Fernández Báez** · brianferbaez@gmail.com · Tesis de Maestría · 2026
Repositorio: [github.com/ZOMBIECRAFTIAN/raptors-cnn](https://github.com/ZOMBIECRAFTIAN/raptors-cnn)

### Licencias

- **Código:** MIT
- **Modelo:** Creative Commons CC-BY 4.0
- **Catálogo de señas:** CC-BY-SA 4.0 (co-creación con comunidad sorda)
- **Tesis:** CC-BY-NC 4.0
                """)

    return demo


def main():
    demo = build_interface()
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True, share=False)


if __name__ == "__main__":
    main()
