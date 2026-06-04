# Speaker notes + code study guide

This file complements `Presentation_Script_EN.md`. For each slide you get:

- **Speaker cue** — the 3-5 bullet talking points if you forget the script.
- **Likely question** — what the US professor will probably ask.
- **Code/file to study** — the real file in your repo you should read before Friday so you can answer with confidence.
- **English phrase** — the exact wording to use in the answer.

Print this and the script together. Read both at least three times before the meeting.

---

## SLIDE 1 - Title

- **Speaker cue:** name, master's candidate, project title, 53 raptors of Mexico, integrated with IS.
- **Likely question:** "Why this topic?"
- **Code/file to study:** `README.md` (top section + abstract EN).
- **English phrase:** *"I have been fascinated by raptors since I was a child, and I wanted to combine that passion with the accessibility work I am doing with the Deaf community in Mexico."*

---

## SLIDE 2 - Agenda

- **Speaker cue:** 7 sections, 25 minutes total.
- **Likely question:** none usually.
- **Code/file:** none.
- **English phrase:** *"Please interrupt me at any point if you want me to go deeper."*

---

## SLIDE 3 - The problem

- **Speaker cue:** in flight, far, backlit; silhouette is all you have; 5M raptors in Veracruz corridor.
- **Likely question:** "Is this dataset noisy?"
- **Code/file:** `codigo/pytorch/curate.py` (lines around `def score_image`).
- **English phrase:** *"Yes, raw iNaturalist data is noisy. We address it with curate.py, which scores every image on five criteria and routes borderline cases to a double-annotation step with a Cohen's kappa floor of zero point eight five."*

---

## SLIDE 4 - The two gaps

- **Speaker cue:** epistemic gap (expert knowledge not codified) + accessibility gap (no IS catalogue).
- **Likely question:** "Why International Sign and not American Sign Language?"
- **Code/file:** `lengua_de_senas/README.md` + `documentacion/contribucion_novedosa.md`.
- **English phrase:** *"International Sign is the cross-national signed lingua franca documented by the World Federation of the Deaf. It maximises reach. We document equivalents in Mexican Sign Language and ASL where possible, as a reference column."*

---

## SLIDE 5 - Research question

- **Speaker cue:** one long sentence; each clause = one objective.
- **Likely question:** "What does *expert-level accuracy* mean operationally?"
- **Code/file:** `codigo/pytorch/evaluate.py` (where metrics are computed).
- **English phrase:** *"Operationally we benchmark against the inter-expert agreement reported in the ornithological literature - typically eighty to eighty-five percent. So a target of F1-macro zero point eight is conservative but defensible."*

---

## SLIDE 6 - Three hypotheses

- **Speaker cue:** H1 technical, H2 novelty, H3 inclusion.
- **Likely question:** "How will you test H2 specifically?"
- **Code/file:** `documentacion/preregistration.md`.
- **English phrase:** *"We pre-register pairs of confused species before training. After training we compute the per-pair confusion delta between the image-only model and the image-plus-behaviour model. The fifteen percent target is on that delta, not on global accuracy."*

---

## SLIDE 7 - Objectives

- **Speaker cue:** 1 general + 5 specific, each mapped to a chapter.
- **Likely question:** "Is the sign work supervised by a linguist?"
- **Code/file:** `lengua_de_senas/instrumentos_validacion/cuestionario_likert.md`.
- **English phrase:** *"Yes, the protocol is reviewed by the Confederacion Nacional de Personas Sordas de Mexico and we follow the World Federation of the Deaf manifesto."*

---

## SLIDE 8 - 53 species

- **Speaker cue:** 38 + 10 + 4 + 1; AOS 2024 splits.
- **Likely question:** "Why not include Strigiformes from the start?"
- **Code/file:** `documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md`.
- **English phrase:** *"Diurnal raptors share a visual modality. Owls require night-vision imagery and audio modalities. They belong to V2 as a separate research thread."*

---

## SLIDE 9 - Why silhouette + flight

- **Speaker cue:** Merlin uses plumage; we use shape; augmentations strip colour; second module is behaviour.
- **Likely question:** "What happens with a perched bird upload?"
- **Code/file:** `codigo/pytorch/app_flask/app.py` (`/predict` route).
- **English phrase:** *"The pipeline accepts it but flags lower confidence because the model was trained on flight-silhouette distribution. That is a documented limitation and one of the V2 priorities."*

---

## SLIDE 10 - Dataset pipeline

- **Speaker cue:** 5 stages, 53 classes, 200 target per species, kappa floor 0.85.
- **Likely question:** "Are the iNaturalist images copyright-clean?"
- **Code/file:** `codigo/pytorch/download_inaturalist.py` (lines with `LICENSE` filter).
- **English phrase:** *"Yes. The downloader filters on Creative Commons CC0, CC-BY, CC-BY-SA. The licence and attribution metadata are stored alongside each image and reproduced in any output we publish."*

---

## SLIDE 11 - Curate.py

- **Speaker cue:** 5 criteria, score 0-100, KEEP/REVIEW/DISCARD.
- **Likely question:** "How do you measure sharpness?"
- **Code/file:** `codigo/pytorch/curate.py` (`def _sharpness`).
- **English phrase:** *"We compute the variance of the Laplacian on the image. Low variance signals blur. We set the threshold empirically by labelling a calibration set."*

---

## SLIDE 12 - Augmentations

- **Speaker cue:** standard set + silhouette-targeted set; cannot win with colour.
- **Likely question:** "Did you ablate the silhouette augmentations?"
- **Code/file:** `codigo/pytorch/train.py` (look for `--no-silhouette-augs` if present, otherwise plan).
- **English phrase:** *"We plan an ablation table in Chapter 4, comparing standard-only versus standard-plus-silhouette across all four architectures, with three random seeds each."*

---

## SLIDE 13 - Four architectures

- **Speaker cue:** MobileNet (edge), B3 (ratio), ResNet50 (baseline), ConvNeXt-Tiny (SOTA).
- **Likely question:** "Why not include a Vision Transformer like ViT-B/16?"
- **Code/file:** `codigo/comparacion/README.md`.
- **English phrase:** *"Excellent question. ViT requires more data than we have per class for fine-grained classification. ConvNeXt-Tiny closes most of the ViT gap with CNN-friendly compute. ViT is on the V2 list once we have the synthetic-minority augmentation."*

---

## SLIDE 14 - Two-stage training

- **Speaker cue:** Stage 1 head only; Stage 2 fine-tune everything; cosine annealing; weighted CE.
- **Likely question:** "Why two stages? Why not just end-to-end fine-tuning?"
- **Code/file:** `codigo/pytorch/train.py` (`run_stage` function).
- **English phrase:** *"Fine-tuning the full backbone with a randomly initialised head can destroy pre-trained features in the first few epochs. Stage one stabilises the head first. It is a standard recipe from Howard and Ruder twenty eighteen, ULMFiT."*

---

## SLIDE 15 - config.py code

- **Speaker cue:** SPECIES list, BATCH_SIZE, USE_AMP, device autodetect.
- **Likely question:** "Does this run on Apple Silicon?"
- **Code/file:** `codigo/pytorch/config.py` (function `_detect_device`) + `codigo/pytorch/environment-mps.yml`.
- **English phrase:** *"Yes. The device function detects MPS on M-series Macs. I ship an environment-mps.yml file alongside the CUDA and CPU environments. Same code, three platforms."*

---

## SLIDE 16 - Flight behaviour

- **Speaker cue:** 6 steps, Faster R-CNN bird-class, CNN-LSTM 5 modes, Bayes posterior.
- **Likely question:** "How do you handle the assumption of conditional independence in the Bayes step?"
- **Code/file:** `documentacion/ROADMAP_V2.md` (multimodal Bayesian section).
- **English phrase:** *"V1 uses a naive Bayes approximation, which assumes conditional independence given the species. V2 will model the joint with a small graphical model and learn the dependence empirically. The naive version is a calibrated starting point."*

---

## SLIDE 17 - Grad-CAM

- **Speaker cue:** 95% accuracy not enough; activation peaks on wingtip + tail; 20 maps per class audit.
- **Likely question:** "What if Grad-CAM lies to you?"
- **Code/file:** `codigo/pytorch/gradcam.py`.
- **English phrase:** *"Grad-CAM is a known proxy. We complement it with the augmentation ablation - if removing the silhouette augmentations drops accuracy by more than ten points, that is independent evidence the model learned shape. We mention this in Chapter 4."*

---

## SLIDE 18 - International Sign

- **Speaker cue:** 3 iterations, Likert >= 4.0, 10-min retention test, 14 random clips.
- **Likely question:** "Have the signs been published?"
- **Code/file:** `lengua_de_senas/catalogo_senas/Catalogo_de_Senas_Propuesta_Brian.md`.
- **English phrase:** *"The proposal is published in the repository under CC-BY. The validated final versions follow after the focus-group sessions, on the same licence."*

---

## SLIDE 19 - Flask GUI

- **Speaker cue:** drag-drop, top-3, Grad-CAM, fact sheet, sign video, Darwin Core export.
- **Likely question:** "Can I see a demo?"
- **Code/file:** `codigo/pytorch/app_flask/app.py` + `templates/index.html`.
- **English phrase:** *"Absolutely. I can run it on my laptop right now. The model loads in ten seconds and inference is sub-second per image."*

---

## SLIDE 20 - Active learning

- **Speaker cue:** loop with audit step, 50 confirmed corrections before retraining.
- **Likely question:** "How do you prevent feedback poisoning?"
- **Code/file:** `codigo/pytorch/retrain_with_feedback.py`.
- **English phrase:** *"Every correction is logged with user, timestamp and original prediction. An expert annotator must sign off before the correction enters the retrain pool. The minimum batch of fifty plus the audit step makes a coordinated attack practically infeasible."*

---

## SLIDE 21 - Reproducibility

- **Speaker cue:** seeds, three environments, SHA-256, Git tags, MIT + CC-BY, weights published.
- **Likely question:** "What about deterministic GPU operations?"
- **Code/file:** `codigo/pytorch/train.py` (`torch.backends.cudnn.deterministic = True`).
- **English phrase:** *"We set cuDNN deterministic to True and accept the small throughput cost. Reproducibility outranks training speed in our priorities."*

---

## SLIDE 22 - Expected results

- **Speaker cue:** Accuracy >= 0.80, F1-macro >= 0.80, top-3 >= 0.95, behaviour +15%, Likert >= 4.0, < 1 s inference.
- **Likely question:** "What is your worst-case scenario number?"
- **Code/file:** `documentacion/preregistration.md`.
- **English phrase:** *"If accuracy lands between zero point seven and zero point eight, the contribution is still defensible because the silhouette and IS components are independent novelties. We have a fallback chapter that discusses partial-success outcomes."*

---

## SLIDE 23 - Limitations

- **Speaker cue:** 4 limitations, each with a V2 mitigation.
- **Likely question:** "How will you scale dataset acquisition for rare species?"
- **Code/file:** `documentacion/data_management_plan.md`.
- **English phrase:** *"We have an in-progress agreement with The Peregrine Fund's Mesoamerican programme to access photos from the Pechirrufo Falcon project, and CONABIO has historical archives that are not yet digitised."*

---

## SLIDE 24 - Roadmap V2

- **Speaker cue:** 3D-CNN, DeepSORT, flight-mode CNN, multimodal Bayes, Strigiformes.
- **Likely question:** "Which of the five is the doctoral thesis?"
- **Code/file:** `documentacion/ROADMAP_V2.md`.
- **English phrase:** *"The multimodal Bayesian fusion is the core. The 3D-CNN and the tracker are enabling tools. The Strigiformes expansion is the long-term scaling story for any program that values applied conservation impact."*

---

## SLIDE 25 - PhD positioning

- **Speaker cue:** 3 original contributions, any one publishable, together a research program.
- **Likely question:** "Where would you publish?"
- **Code/file:** `documentacion/contribucion_novedosa.md`.
- **English phrase:** *"The CNN work targets the Methods in Ecology and Evolution journal. The behaviour fusion fits Ecological Informatics. The International Sign catalogue fits the Journal of Deaf Studies and Deaf Education, with a co-author from the Deaf community."*

---

## SLIDE 26 - Thank you / Q&A

- **Speaker cue:** all on GitHub, MIT + CC-BY, ready for questions.
- **Closing line:** *"I am ready for your questions."*

---

## What to study before Friday — the priority list

If you only have time for five files, read them in this order. Each file maps to a slide and is the answer to its most likely question.

| Priority | File | Defends slide | Read for |
|---|---|---|---|
| 1 | `codigo/pytorch/config.py` | 15 | hyperparameters + device autodetect |
| 2 | `codigo/pytorch/train.py` | 14, 21 | two-stage training + reproducibility |
| 3 | `codigo/pytorch/curate.py` | 11 | image scoring + Laplacian sharpness |
| 4 | `codigo/pytorch/gradcam.py` | 17 | interpretability validation |
| 5 | `codigo/pytorch/app_flask/app.py` | 19 | how the Flask GUI calls the model |

If you have time for ten files, add:

| 6 | `codigo/pytorch/evaluate.py` | 22 | F1-macro, top-3 acc, confusion matrix |
| 7 | `codigo/pytorch/download_inaturalist.py` | 10 | licence filter, API pagination |
| 8 | `codigo/pytorch/data_loader.py` | 12 | augmentations and silhouette-targeted transforms |
| 9 | `codigo/comparacion/comparar_arquitecturas.py` | 13 | how the 4-architecture comparison runs |
| 10 | `codigo/pytorch/retrain_with_feedback.py` | 20 | active-learning audit flow |

---

## Five recovery phrases for when you do not know the answer

1. *"That is a great question. I have not measured that directly, but my intuition is X - I will verify and follow up."*
2. *"You are right that this is a limitation. I document it in Chapter 5, section three."*
3. *"The honest answer is I don't know yet - that experiment is in the roadmap."*
4. *"Let me think about that for a moment."* (3 seconds is fine)
5. *"Could you help me make sure I understood the question correctly?"*

Any of these is better than guessing wrong.

---

## Logistics checklist for Friday

The night before:

- [ ] Open and play the deck once end-to-end at home, timing yourself.
- [ ] Charge laptop, take charger, take HDMI adapter.
- [ ] Save the deck on a USB stick as backup.
- [ ] Push to GitHub so it is reachable from anywhere.
- [ ] Test internet and the Flask app on your local network.
- [ ] Print this script and the speaker notes (single-sided, large font).
- [ ] Bring a bottle of water.
- [ ] Sleep eight hours.

In the morning:

- [ ] Eat a real breakfast. No coffee on an empty stomach.
- [ ] Arrive twenty minutes early. Set up. Test the projector.
- [ ] Open the GitHub README on a second tab as a backup demo.
- [ ] Turn off notifications on your laptop.

During the talk:

- [ ] Look at the professor's face, not at the screen.
- [ ] Pause for two seconds at every transition between sections.
- [ ] If asked a hard question, repeat it in your own words first to gain time.

Good luck. You have done excellent work and the project speaks for itself.
