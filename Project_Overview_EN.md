# Project portfolio overview - master's candidate Brian Fernandez Baez

**Reading time: 45 minutes. This is the single document you study before Friday.**

---

## How to use this file

The professor will likely ask three things about each project:

1. **Justification** - why does it exist? What problem does it solve?
2. **Construction process** - how did you build it? How can it be improved?
3. **Comfort with bioacoustics** - could you extend to audio?

This document answers all three for all three projects, then proposes the unifying doctoral program. Read it twice. Then move to `Self_Quiz_EN.md` to test yourself.

---

## The 30-second pitch

> "My research program is **multi-modal AI for biodiversity identification with accessibility built in**. I have three projects that together form a coherent doctoral path: a visual raptor identifier for Australia with AUSLAN signs, a scaled visual raptor identifier for Mexico with International Sign and behaviour analysis, and a passive acoustic monitoring system for mammals, amphibians, reptiles and insects. The natural doctorate is the multi-modal fusion of all three: vision + acoustics + sign language for continent-scale wildlife monitoring that is accessible to the Deaf community."

Memorise this verbatim. Practice it three times. If the professor asks "tell me about your work" in the hallway, this is the answer.

---

## Project 1 - Australian Raptor CNN + AUSLAN

### What it is

Deep-learning identifier for **8 raptor species of southeast Australia**, coupled with a proposed AUSLAN (Australian Sign Language) vocabulary for Deaf citizen scientists. Built as the foundation for an MPhil research proposal at the **University of Queensland**.

### Justification - why it exists

- The **2019-2020 Black Summer bushfires** affected 3 billion vertebrates and burnt 18.6 million hectares (Ward et al., *Nature Ecology & Evolution*, 2020).
- Recovery monitoring of apex predators like raptors is a **national research priority** of the Australian Department of Agriculture, Water and Environment.
- Current methods are slow, manual, and exclude **3.6 million Australians with hearing loss** from citizen-science participation.
- This project closes three gaps simultaneously: **automation** (a CNN does the ID), **inclusion** (AUSLAN vocabulary), **interoperability** (Darwin Core export to Atlas of Living Australia).

### The 8 target species

| Common name | Scientific | F1 (test) | Conservation status |
|---|---|---|---|
| Wedge-tailed Eagle | *Aquila audax* | 0.94 | Subspecies endangered |
| Spotted Harrier | *Circus assimilis* | 0.85 | Vulnerable (NSW) |
| Peregrine Falcon | *Falco peregrinus macropus* | 0.86 | Not listed |
| Brown Goshawk | *Tachyspiza fasciata* | n/a | Not listed |
| Nankeen Kestrel | *Falco cenchroides* | 0.74 | Not listed |
| Black-shouldered Kite | *Elanus axillaris* | 0.81 | Not listed |
| Square-tailed Kite | *Lophoictinia isura* | 0.75 | **Vulnerable (EPBC)** |
| Little Eagle | *Hieraaetus morphnoides* | 0.84 | Not listed |

### Construction process

1. **Dataset.** ~2400 images from iNaturalist (research-grade) plus Atlas of Living Australia (no API key required).
2. **Architecture.** EfficientNet-B4 with transfer learning from ImageNet.
3. **Training.** Two-stage: feature extraction first, then fine-tuning. Adam optimiser, mixed precision.
4. **Metrics achieved.** Accuracy **0.8495**, F1-macro **0.8478** on the test set of 206 images.
5. **Interpretability.** Grad-CAM mosaic for sanity-check that attention falls on bird, not background.
6. **GUI.** Flask web app with drag-drop, top-3 prediction, species fact sheet, AUSLAN sign video, citizen-science form.
7. **Export.** Every observation is exportable in Darwin Core JSON for Atlas of Living Australia / GBIF.

### What I learned that fed the other projects

- **Transfer learning recipe** that became the V1 template for Mexico.
- **GUI patterns** (drag-drop, Merlin-style fact sheet) that I migrated 1:1 to raptors-cnn.
- **Sign-language methodology** I refined for IS in the Mexico project.
- **Darwin Core integration** for biodiversity data sharing.

### How it can be improved (the answer to "what's next?")

- **Add a behaviour module.** Same as raptors-cnn V2: 3D-CNN on short video.
- **Add audio modality.** Many raptors are heard before seen; bioacoustics complements vision.
- **Federated learning.** Each ranger station trains locally, aggregates centrally - privacy-preserving.
- **EPBC-listed species priority sampling.** Rare-species detection is the conservation impact axis.

### Honest weaknesses

- Only 8 species.
- F1-macro just below the 0.85 target.
- No behaviour analysis yet.
- AUSLAN vocabulary is a *proposal*, not yet validated with focus groups.

---

## Project 2 - Raptors CNN Mexico (raptors-cnn V1.1)

### What it is

The master's-thesis project. Extends Australia from 8 to **53 diurnal raptor species of Mexico** (AOS 2024), replaces AUSLAN with **International Sign** (broader reach), and **adds a behaviour module** that combines silhouette classification with flight-mode analysis through a Bayesian prior.

### Justification - why it exists

- Mexico hosts the largest raptor migration corridor in the Americas: more than **5 million birds** through Veracruz each autumn.
- Existing tools (Merlin Bird ID, iNaturalist) train on **perched birds with rich colour photos** - useless for raptors in flight against bright sky.
- An expert ornithologist relies on **silhouette + flight cadence**, not colour. We build a model that imitates this.
- The Deaf community in Mexico has no signed vocabulary for raptors. The IS catalogue is the first of its kind in any biodiversity domain.

### Why 53 species (and not 23)

The project started in V1 with only the 23 species of the Veracruz River of Raptors corridor. In V1.1 it expanded to the full 53 diurnal raptors of Mexico (AOS 2024) to be **nationally representative**, not corridor-specific. The 23 V1 species are preserved within the 53; nothing was discarded.

### Construction process

1. **Dataset.** Same pipeline as Australia, scaled: iNaturalist + Macaulay + eBird + CONABIO. ~10 600 images target, ~3 GB.
2. **Curation.** `curate.py` scores each image 0-100 (resolution, Laplacian sharpness, brightness, perceptual hash). KEEP / REVIEW / DISCARD outcomes.
3. **Annotation.** Double-annotation on borderline images with **Cohen's kappa >= 0.85** required.
4. **Split.** 70/15/15 stratified by species, seed 42.
5. **Architectures.** **Four CNNs benchmarked head-to-head**: MobileNetV3-Large, EfficientNet-B3, ResNet-50 (baseline), ConvNeXt-Tiny.
6. **Training.** Same two-stage recipe as Australia. Mixed precision and gradient accumulation let me train on a 4 GB RTX 3050.
7. **Augmentations.** Standard set **plus silhouette-targeted layer**: saturation jitter, random grayscale, plumage erasing. The model literally cannot win with colour.
8. **Interpretability.** Grad-CAM on every architecture; manual audit of >= 20 maps per class.
9. **GUI.** Flask web app (same look as Australia, scaled). Multilingual ES/EN.
10. **Behaviour module.** Faster R-CNN bird detection -> CNN-LSTM classifier on 5 flight modes -> Bayesian fusion with the visual prediction. V1.1 is the prior-based prototype; V2 is full multi-modal Bayesian.
11. **International Sign catalogue.** 53 signs in 3 iterations: proposal -> focus-group refinement -> Likert validation (>= 4.0).
12. **Active learning.** User feedback loop with expert audit gate; retrain only after 50 confirmed corrections.
13. **Reproducibility.** Three environment files (CUDA / CPU / Apple Silicon MPS), SHA-256 logs, Git tags, MIT + CC-BY.

### What it adds beyond Australia

- 6.6x more species (8 -> 53).
- 4 architectures compared, not 1.
- **Behaviour module is novel.** No published raptor identifier fuses static silhouette with flight-mode behaviour.
- **International Sign** (broader than AUSLAN).
- Multi-platform device detection (CUDA / MPS / CPU).
- Active learning with audit safeguards.
- Bayesian fusion as the path toward a multi-modal V2.

### How it can be improved (the doctorate roadmap)

The V2 roadmap, formalised in `documentacion/ROADMAP_V2.md`:

1. **3D-CNN** (SlowFast or ResNet3D-18) trained end-to-end on short clips at 8-16 fps - captures the *Falco peregrinus* stoop, which V1 cannot see at 1 fps.
2. **DeepSORT tracker** for per-individual tracking across frames.
3. **Flight-mode classifier** with quantitative descriptors: flap frequency in Hertz, altitude gain in m/s, thermal radius.
4. **Multimodal Bayesian fusion** - vision + behaviour + phenology + geography at posterior level.
5. **Strigiformes expansion** to add ~30 owl species, which introduces **night-vision + audio modalities**. This is where it connects to Project 3.

### Honest weaknesses

- Class imbalance: *Cathartes aura* > 1000 images vs *Harpia harpyja* ~60.
- iNaturalist bias toward clear-sky soaring birds.
- 1 fps temporal resolution insufficient for fast events.
- Geographic prior risks confirmation bias.
- Behaviour module is **planned**, full implementation is V2.

---

## Project 3 - BioAcoustics Fauna Identification System

### What it is

A complete **Passive Acoustic Monitoring (PAM)** pipeline that detects and identifies **mammals, amphibians, reptiles and insects** from field audio recordings. Production-grade architecture: PyTorch models, FastAPI REST, PostgreSQL with PostGIS, Docker compose, CI/CD.

### Justification - why it exists

- Many species are **heard before seen** - bats, frogs, crickets, monkeys, owls, nocturnal mammals.
- Visual-only systems (Projects 1 and 2) miss them entirely.
- PAM is the standard for ecological monitoring at scale: low-cost recorders (AudioMoth) deployed for weeks, terabytes of audio.
- Manual analysis is infeasible. AI is mandatory at this scale.
- A unified system that covers chiroptera + amphibians + insects + vocal mammals + reptiles has, to my knowledge, no equivalent in any single open-source toolkit.

### Taxonomic groups and signal characteristics

| Group | Frequency | Sample rate | What we detect |
|---|---|---|---|
| Chiroptera (bats) | 20-200 kHz | 192 kHz | Echolocation pulses |
| Amphibia (anurans) | 100-8 000 Hz | 22 050 Hz | Mating calls |
| Insecta (Orthoptera, Cicadidae) | 200-100 kHz | 44 100 Hz | Stridulation |
| Mammalia (vocal) | 20-20 000 Hz | 22 050 Hz | Vocalisations |
| Reptilia | 100-5 000 Hz | 22 050 Hz | Crocodilians, geckos |

### Construction process

1. **Acquisition layer.** AudioMoth / SM4BAT / Zoom H5 -> .wav / .flac.
2. **Preprocessing pipeline.** Bandpass filter -> noise reduction (`noisereduce`) -> normalise -> Voice Activity Detection -> segment. Presets per taxonomic group.
3. **Feature extraction.** Mel spectrogram, MFCC + delta + delta-delta, Zero-Crossing Rate, Spectral Centroid, Chroma.
4. **Three classifier architectures.**
   - **BioAcousticCNN** - custom with residual blocks (baseline).
   - **EfficientNet** - B0/B4, transfer learning from ImageNet on spectrograms-as-images.
   - **PANNs-CNN14** - pre-trained on **AudioSet** (the audio equivalent of ImageNet). Strongest performer.
5. **Storage.** PostgreSQL 15 with PostGIS, full taxonomic schema (kingdom -> species), spatial indexing for site coordinates.
6. **API.** FastAPI REST with async PostgreSQL driver (`asyncpg`). Endpoints: `/classify`, `/detections`, `/species`.
7. **Real-time monitor.** `acoustic_monitor.py` - continuous capture + VAD + inference, runs on edge devices.
8. **Augmentation.** Bioacoustic-specific: SpecAugment, time stretch, pitch shift, mix with field noise, channel dropout.
9. **Edge deployment.** Export to ONNX and TorchScript via `scripts/export_model.py`.
10. **Testing.** 35 unit tests on preprocessing, 50 on models. Pytest + coverage in CI.
11. **DevOps.** Docker multi-stage build, docker-compose orchestrating API + Postgres + pgAdmin + MLflow. GitHub Actions CI.

### How it can be improved

- **Active-listening loop.** Sample more around uncertain detections.
- **Site adaptation.** Few-shot fine-tuning per recording site (each location has its own soundscape).
- **Federated learning** across recorder networks.
- **Multi-target detection.** Multiple species overlapping in one clip (currently one species per segment).
- **Visual fusion.** Pair with a camera-trap to confirm visual identity when audio matches.

### Why this matters for the doctorate

This is where the answer to "are you comfortable with bioacoustics?" becomes:

> "Yes. I have a working PAM system, version 0.3, with three classifier architectures including PANNs-CNN14 pre-trained on AudioSet, a FastAPI service, PostgreSQL storage, Docker deployment and CI. The natural next step is the fusion with Projects 1 and 2 into a multi-modal raptor + general fauna system."

That is a much stronger answer than "I could learn it."

### Honest weaknesses

- Currently single-species per audio segment.
- Dataset is still being assembled (Xeno-canto, iNaturalist audio, GBIF).
- No human-in-the-loop GUI yet (it is a backend system).
- Performance numbers are preliminary; full benchmark pending.

---

## How the three projects fit together

```
                Australian Raptor CNN  (Project 1)
                +  AUSLAN sign vocabulary
                +  Atlas of Living Australia
                          |
                          |  scale up + behaviour + IS
                          v
                Raptors-CNN Mexico  (Project 2)
                +  53 species + International Sign
                +  Bayesian behaviour fusion
                          |
                          |  add audio modality
                          v
                BioAcoustics PAM  (Project 3)
                +  mammals + anurans + bats + insects
                +  PostgreSQL + FastAPI + PANNs

                          |
                          v

                  DOCTORAL THESIS
            Multi-modal AI for biodiversity ID:
            vision + audio + sign language
            for continent-scale monitoring
            accessible to the Deaf community
```

### The unifying argument

These are not three unrelated projects. They are a **research program**:

1. **Project 1 proved the baseline:** transfer learning works for raptor visual ID, with sign-language accessibility integrated from day one.
2. **Project 2 proved scale and rigor:** the same method scales 6x with multi-architecture comparison, behaviour fusion, and reproducibility infrastructure.
3. **Project 3 proves modality breadth:** the same person who does vision can also do production-grade audio AI.
4. **The doctoral synthesis is the missing piece:** a single system where vision and audio classifiers vote together through a Bayesian fusion, where the sign-language layer guarantees accessibility, and where the output feeds biodiversity data infrastructure (Atlas of Living Australia, GBIF, iNaturalist via Darwin Core).

This is the answer to "what is the contribution that justifies a PhD?"

---

## The three questions, answered for each project

| Project | Justification | Construction | How to improve |
|---|---|---|---|
| **1. Australia** | Black Summer bushfires, EPBC monitoring, AUSLAN inclusion | EfficientNet-B4 + transfer learning + Flask GUI + Darwin Core | Behaviour module, audio fusion, federated learning |
| **2. Mexico** | Veracruz corridor, silhouette-not-plumage, IS catalogue | 4 CNNs + curation + Bayesian behaviour + IS validation | 3D-CNN, DeepSORT, multimodal Bayes, owls |
| **3. Bioacoustics** | PAM at scale, taxa heard-not-seen, no unified open toolkit | librosa + 3 architectures + FastAPI + PostgreSQL + Docker | Multi-species detection, site adaptation, visual fusion |

---

## Frequently asked questions across projects

**Q: How is this different from BirdNET?**
A: BirdNET is audio-only and bird-only. My bioacoustic project covers five taxonomic groups including non-birds. My visual projects add silhouette-and-flight focus instead of plumage. The doctoral synthesis combines both modalities.

**Q: Why not use Vision Transformers?**
A: ViTs need more data than I have per species for fine-grained classification. ConvNeXt-Tiny in Project 2 closes most of the gap with CNN-friendly compute. ViT is in the V2 list once synthetic-minority augmentation is in place.

**Q: How do you avoid model bias for under-represented species?**
A: Weighted cross-entropy, Mixup, CutMix, and active oversampling. In Project 2 specifically, we partner with The Peregrine Fund for rare-species data and use synthetic minority oversampling with diffusion-generative augmentation in V2.

**Q: How accessible is your system to Deaf scientists?**
A: Each species has a video of its sign in the relevant signed language (AUSLAN in Project 1, International Sign in Project 2), the GUI is keyboard-navigable, and the methodology follows the World Federation of the Deaf manifesto on signed languages and the CAST framework on Universal Design for Learning.

**Q: What is your most novel contribution?**
A: The combination. Each project has merit. The doctoral synthesis - vision + audio + sign language for biodiversity ID, with reproducibility and accessibility as first-class design constraints - is what I have not seen published anywhere.

**Q: Where would you publish?**
A: Vision work: *Methods in Ecology and Evolution*. Behaviour fusion: *Ecological Informatics*. Bioacoustic system paper: *Journal of Open Source Software*. Sign-language catalogue: *Journal of Deaf Studies and Deaf Education*, co-authored with a Deaf community member.

---

## What to study tonight

1. This document. Twice.
2. `Presentation_Script_EN.md` slide by slide.
3. The 5 priority code files listed in `Presentation_Speaker_Notes_EN.md`.
4. The `reporte_final.json` of the Australian project, so you know the numbers cold.
5. The README of `Identificacion de mamiferos` - the architecture diagram and the 5 layers.

Tomorrow morning, do the self-quiz in `Self_Quiz_EN.md`. If you score 25/30 or better, you are ready.

Good luck.
