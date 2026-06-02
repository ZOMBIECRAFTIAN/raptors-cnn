# Self-quiz - 30 questions, answer key at the end

Take the quiz on **Wednesday or Thursday morning** with your laptop closed. Aim for 25/30 or better. If you score below that, the answer key tells you which document to reread.

Time yourself: 30 minutes total. Do not look anything up.

---

## Section A - The portfolio (10 questions)

**A1.** How many projects does my research portfolio contain, and what is the unifying theme?

**A2.** Which is the master's thesis project of the three?

**A3.** Which project uses the production stack with FastAPI + PostgreSQL + Docker?

**A4.** What signed language does the Australia project use, and what does the Mexico project use? Why are they different?

**A5.** What is the natural doctoral thesis that unifies the three projects?

**A6.** Give one number that summarises each project's current status.

**A7.** What is the 30-second elevator pitch (key phrases)?

**A8.** Why was the Mexico project expanded from 23 species (V1) to 53 species (V1.1)?

**A9.** Name the four CNN architectures benchmarked in the Mexico project, in order from fewest to most parameters.

**A10.** What are the five taxonomic groups covered by the bioacoustics project?

---

## Section B - Technical questions on Mexico (10 questions)

**B1.** What does `BATCH_SIZE = 16` and `GRADIENT_ACCUM_STEPS = 2` give you in terms of effective batch?

**B2.** What does the function `_detect_device()` do in `config.py`?

**B3.** Name three augmentations from the "silhouette-targeted" list (not the standard list).

**B4.** What is the Cohen's kappa threshold and why that number?

**B5.** What is the test split ratio and what is the seed?

**B6.** What three outcomes does `curate.py` assign to each image?

**B7.** In what order are the six steps of the flight-behaviour module?

**B8.** What does Grad-CAM tell you, and what would make a sample fail your audit?

**B9.** Why two-stage training instead of end-to-end fine-tuning?

**B10.** What is the active-learning safeguard that prevents one user from poisoning the model?

---

## Section C - Bioacoustics and synthesis (10 questions)

**C1.** What is PANNs-CNN14 pre-trained on?

**C2.** Why does Chiroptera need 192 kHz sample rate?

**C3.** Name three signal features extracted from audio in the bioacoustics project.

**C4.** What does PostGIS add to PostgreSQL and why does this project need it?

**C5.** What is "voice activity detection" (VAD) in the context of this project?

**C6.** How does the bioacoustics project handle different taxa with completely different acoustic signatures?

**C7.** How do you answer "are you comfortable with bioacoustics?" without saying just "yes"?

**C8.** What is the doctoral synthesis of the three projects in one sentence?

**C9.** Name three deliverables you commit to in the first year of the doctorate.

**C10.** What is the biggest honest weakness across the three projects?

---

## Answer key

### Section A

- **A1.** Three projects: Australian Raptor CNN, Raptors-CNN Mexico, Bioacoustics fauna ID. Theme: **multi-modal AI for biodiversity identification with accessibility built in**.
- **A2.** Mexico (raptors-cnn V1.1).
- **A3.** Bioacoustics (project 3).
- **A4.** Australia = AUSLAN (Australian Sign Language). Mexico = International Sign. Different because IS reaches a wider Deaf audience globally; AUSLAN was the natural choice when the proposal was for the University of Queensland.
- **A5.** Multi-modal AI for biodiversity ID combining vision + audio + sign language, for continent-scale monitoring accessible to the Deaf community.
- **A6.** Australia: F1-macro 0.85 / accuracy 85%. Mexico: 53 species. Bioacoustics: v0.3, 5 taxonomic groups, 85 unit tests.
- **A7.** Key phrases: "multi-modal AI for biodiversity", "accessibility built in", "three projects, one program", "vision + acoustics + sign language".
- **A8.** V1 only covered the 23 species of the Veracruz River of Raptors corridor. V1.1 expanded to all 53 diurnal raptors of Mexico for **national representativeness**.
- **A9.** MobileNetV3-Large (5.5M), EfficientNet-B3 (12.2M), ResNet-50 (25.6M), ConvNeXt-Tiny (28.6M).
- **A10.** Chiroptera (bats), Amphibia (anurans), Insecta (Orthoptera, Cicadidae), Mammalia (vocal), Reptilia.

### Section B

- **B1.** Effective batch = `BATCH_SIZE × GRADIENT_ACCUM_STEPS = 16 × 2 = 32`. Lets you simulate batch 32 on a 4 GB GPU that can only fit batch 16 in memory.
- **B2.** Auto-detects the hardware: returns `cuda` if NVIDIA GPU available, otherwise `mps` if Apple Silicon, otherwise `cpu`. Lets the same code run on three platforms.
- **B3.** Saturation jitter up to 0.4 / random conversion to grayscale with p=0.2 / RandomErasing on plumage regions.
- **B4.** Cohen's kappa floor = 0.85. Landis & Koch 1977 call 0.81-1.00 "almost perfect agreement". Below that is not good enough for fine-grained taxonomy.
- **B5.** 70 / 15 / 15 train/val/test, stratified by species, seed = 42.
- **B6.** KEEP (>= 70) / REVIEW (40-69, needs double annotation) / DISCARD (< 40, moved to `_review/` folder, never deleted).
- **B7.** Sample frames at 1 fps -> Faster R-CNN bird detection -> crop and classify -> extract behavioural descriptors -> CNN-LSTM classifies 5 flight modes -> Bayesian combination with the visual prediction.
- **B8.** Grad-CAM shows which pixels the model relied on to make its decision. A sample fails the audit if the activation peaks on background (sky, trees) instead of the bird.
- **B9.** End-to-end fine-tuning with a randomly initialised head destroys pre-trained backbone features in the first epochs. Stage 1 stabilises the head with backbone frozen; stage 2 unfreezes everything once the head is sensible. Recipe from Howard & Ruder 2018 (ULMFiT).
- **B10.** Every correction is logged with user, timestamp, and original prediction. An expert annotator must sign off on each correction. Retraining triggers only after 50 confirmed corrections accumulate.

### Section C

- **C1.** AudioSet (the audio equivalent of ImageNet, but about 10x larger).
- **C2.** Bat echolocation pulses range from 20 to 200 kHz. By Nyquist theorem, you need at least 2x the highest frequency to capture it, so 192 kHz (or 256 kHz) sample rate is required.
- **C3.** Mel spectrogram / MFCC + delta + delta-delta / Zero-Crossing Rate / Spectral Centroid / Chroma (any three).
- **C4.** PostGIS adds spatial indexing and geographic queries to PostgreSQL. The project needs it because every detection has a site coordinate, and biologists need queries like "all detections of Tyto alba within 10 km of this location".
- **C5.** Voice Activity Detection identifies segments where there is actually sound of interest (a call, a vocalisation) versus silence or background noise. Used to crop the audio before classification.
- **C6.** With **per-taxon presets**: each taxonomic group has its own sample rate, bandpass filter range, noise reduction parameters, and segment length. Bats: 192 kHz, 20-200 kHz bandpass, short segments. Frogs: 22 kHz, 100-8000 Hz bandpass, longer segments.
- **C7.** Lead with "yes - I already have a working PAM system" then list the concrete pieces: three classifier architectures including PANNs-CNN14 on AudioSet, FastAPI, PostgreSQL + PostGIS, Docker, CI/CD. Close with "the multimodal fusion with my visual work is exactly what I want for the doctorate."
- **C8.** Multi-modal AI for biodiversity identification combining vision and audio classifiers via Bayesian fusion, with signed-language accessibility, for continent-scale monitoring published as an open API.
- **C9.** Examples (pick any 3): silhouette-first paper for *Methods in Ecology and Evolution*; multi-modal demo on one site with both modalities; clean reproducibility report; Atlas of Living Australia or GBIF data publication; engagement with Deaf community on sign-vocabulary validation.
- **C10.** No peer-reviewed publication yet across the three projects. That is the natural next step in the doctoral program.

---

## Scoring

- **27-30 correct:** Ready. Sleep well. Re-read the elevator pitch on Friday morning.
- **22-26 correct:** Almost ready. Reread Project_Overview_EN.md and the slides you scored worst on. Do the quiz again Thursday evening.
- **15-21 correct:** Need to reread Project_Overview_EN.md and Presentation_Script_EN.md tonight, then redo Tuesday.
- **Below 15:** Do not panic. Read the overview slowly twice on Sunday. Print everything. The material is yours - you just need it organised in your head.
