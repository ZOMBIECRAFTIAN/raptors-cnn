# Cheat sheet - 1 page, print this

Print on **landscape A4** with **font size 10**. Carry it in your hand or pocket during Q&A.

---

## The three projects in 30 seconds

| | Project 1 | Project 2 (master's) | Project 3 |
|---|---|---|---|
| **Name** | Aus Raptor CNN | Raptors-CNN Mexico | BioAcoustics Fauna ID |
| **Subject** | 8 raptors of SE Australia | 53 raptors of Mexico | 5 taxa (bats, frogs, insects, mammals, reptiles) |
| **Models** | EfficientNet-B4 | 4 CNNs: MobileV3, B3, ResNet50, ConvNeXt-T | BioCNN + EffNet + PANNs-CNN14 |
| **Sign lang** | AUSLAN | International Sign | n/a |
| **Status** | F1 0.85 / Acc 85% | training in progress | v0.3 production stack |
| **Stack** | PyTorch + Flask + ALA | PyTorch + Flask + Darwin Core | PyTorch + FastAPI + PostgreSQL + Docker |
| **Test n** | 206 images | 53 classes, 70/15/15 | 35+50 unit tests |

## Key numbers I must know cold

- **53** species, Mexico, AOS 2024 - 38 Accipitridae + 10 Falconidae + 4 Cathartidae + 1 Pandionidae
- **8** species Australia, 2400 images, 206 test
- **5** taxa bioacoustics, sample rates 22-192 kHz
- **0.85** F1-macro Australia; target 0.80 Mexico; bioacoustics pending
- **42** the seed everywhere
- **70 / 15 / 15** Mexico split, stratified by species
- **>= 0.85** Cohen's kappa floor for annotation
- **16** batch, **2** grad accum steps, effective batch 32
- **80** epochs stage 2 max, **15** early-stopping patience
- **3** AOS 2023 reclassifications: Accipiter cooperii -> Astur cooperii, A. gentilis -> A. atricapillus, Buteo nitidus -> B. plagiatus

## Hyperparameters Mexico

- Stage 1: Adam, lr **1e-3**, backbone frozen, **10** epochs
- Stage 2: AdamW, lr **1e-4**, weight decay **5e-4**, cosine annealing, **3** warm-up epochs
- Augmentations: ColorJitter, Mixup α=**0.2**, CutMix α=**1.0**, label smoothing **0.1**
- Silhouette augs: sat jitter 0.4, grayscale p=0.2, plumage erasing
- Loss: weighted cross-entropy

## Five-layer architecture bioacoustics

1. Acquisition: AudioMoth / SM4BAT, .wav
2. Preprocess: bandpass -> noisereduce -> VAD -> segment
3. Features: Mel + MFCC+ΔΔ + ZCR + spectral centroid + chroma
4. Classify: BioCNN / EffNet / PANNs
5. Storage + API: PostgreSQL 15 + PostGIS + FastAPI

## "Are you comfortable with bioacoustics?" - answer

> "Yes - **I already have a working passive acoustic monitoring system**. v0.3 with three classifier architectures including PANNs-CNN14 pre-trained on AudioSet, FastAPI REST, PostgreSQL with PostGIS, Docker compose, CI/CD. The multimodal fusion with my visual raptor work is the doctorate."

## Five recovery phrases

1. "That is a great question. I haven't measured that, but my intuition is X."
2. "You are right - that is a documented limitation."
3. "Honestly, I don't know yet - that experiment is in the roadmap."
4. "Let me think about that for a moment." [pause 3 sec]
5. "Could you help me make sure I understood the question?"

## Closing line

> "Multi-modal AI for biodiversity ID, with accessibility built in. Three projects, one program. That's why I'm here."

## Hard-to-pronounce names (steal these phonetics)

- Astur cooperii = "AS-tur KU-per-ee-ai"
- Harpia harpyja = "AR-pi-a ar-PI-ya"
- Buteogallus = "BU-te-o GA-yus"
- Spizaetus = "spi-ZA-e-tus"
- Cathartes aura = "ka-TAR-tes A-u-ra"
- Cohen's kappa = "KO-henz KA-pa"
- Laplacian = "la-PLAY-shi-an"
- Bayesian = "BAY-zhi-an"
- silhouette = "si-loo-ET"
- Grad-CAM = "grad-KAM"

## Filler phrases - avoid Spanglish

- "Bueno..." → say **"So..."** or **"Right..."**
- "Entonces" → say **"So"** / **"Therefore"**
- "Como ven" → say **"As you can see"**
- "Es decir" → say **"That is"** / **"In other words"**
- "O sea" → say **"That is to say"** (or skip)
