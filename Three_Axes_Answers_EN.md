# The professor's three questions, answered for each project

Your friend gave you the three things the US professor said he will ask:

1. **Justification** - why the project, what problem it solves, application.
2. **Construction process** - how the model was built, how to improve it.
3. **Bioacoustic readiness** - whether you can work in audio.

This document gives you the **exact answer in English** for each of the three questions, for each of the three projects. Memorise the bold sentences.

---

## PROJECT 1 - Australian Raptor CNN

### Q1.1 - Why this project? What problem does it solve?

> **"Australia experienced its largest documented ecological disaster during the 2019-2020 Black Summer bushfires. Three billion vertebrates were affected, eighteen-point-six million hectares burnt. Recovery monitoring of apex predators like raptors became a national research priority for the Australian Department of Agriculture.**
>
> **My project closes three gaps simultaneously: automation - a CNN identifies eight key raptor species so monitoring can scale; inclusion - an AUSLAN sign vocabulary brings the three-point-six million Australians with hearing loss into citizen science; and interoperability - every observation exports in Darwin Core JSON format, ready for upload to the Atlas of Living Australia or any GBIF data publisher.**
>
> **The application is post-fire ecological recovery monitoring at the scale rangers and ecologists cannot reach manually."**

### Q1.2 - How did you build the model and how can it be improved?

> **"Standard transfer-learning recipe. EfficientNet-B4 backbone pre-trained on ImageNet. Dataset of about 2400 images from iNaturalist research-grade plus the Atlas of Living Australia, automatically downloaded with a Python scraper. Two-stage training: stage one freezes the backbone and trains only the classifier head; stage two unfreezes and fine-tunes the whole network with cosine annealing and label smoothing. The result is F1-macro point-eight-five and accuracy eighty-five percent on the 206-image test set.**
>
> **Three things would improve it: first, adding a behaviour module - 3D-CNN on short video would capture flight cadence the same way an expert ornithologist does. Second, adding an audio modality - many raptors are heard before seen. Third, federated learning across ranger stations so each one trains locally and only model weights are shared, which preserves location privacy of sensitive species."**

### Q1.3 - How does this project prepare me for bioacoustics?

> **"It taught me the transfer-learning template I reused in both other projects, the GUI architecture I migrated to Mexico, and the Darwin Core export pattern. But for bioacoustics specifically, this project did not touch audio - that comes from project three."**

---

## PROJECT 2 - Raptors CNN Mexico (master's thesis)

### Q2.1 - Why this project? What problem does it solve?

> **"Mexico hosts the largest raptor migration corridor in the Americas. More than five million birds pass through Veracruz each autumn. Existing tools like Merlin Bird ID train on perched birds with rich colour photos - they fail when a raptor is in flight against bright sky, which is most field observations.**
>
> **An expert ornithologist relies on silhouette and flight cadence, not colour. My project builds a CNN that imitates this expert reasoning: it trains explicitly on the silhouette in flight, with augmentations that strip colour information. On top of that, I add a Bayesian behaviour module that fuses static visual classification with flight-mode analysis from short video.**
>
> **The application is field identification of all 53 diurnal raptor species of Mexico, with International Sign accessibility for Deaf naturalists. To my knowledge, no published raptor identifier fuses silhouette-targeted CNN with flight-behaviour priors, and no other biodiversity catalogue covers 53 species in any signed language."**

### Q2.2 - How did you build it and how can it be improved?

> **"Five pipelines. One, dataset construction: scrape iNaturalist plus Macaulay Library plus eBird plus CONABIO, restricted to Creative Commons licences. Two, automatic curation in curate dot pie: score each image zero to one hundred on resolution, sharpness measured by variance of Laplacian, brightness, and perceptual hash for deduplication. Three, double annotation on borderline images with Cohen's kappa floor at point-eight-five. Four, training: same two-stage recipe as Australia, scaled. Mixed precision and gradient accumulation let me train on a four-gigabyte RTX 3050. Five, behaviour module: Faster R-CNN bird detection, CNN-LSTM on sixteen frames classifies five flight modes, Bayesian combination with the visual likelihood.**
>
> **I benchmarked four architectures head to head: MobileNetV3, EfficientNet-B3, ResNet-50 as baseline, and ConvNeXt-Tiny. Same split, same augmentations, same protocol. The Pareto plot of accuracy versus latency tells me which to deploy in which scenario.**
>
> **How to improve it - this is the doctorate. Five components. Replace the 1-fps prior with a 3D-CNN at 8-16 fps that captures the falcon stoop. Add DeepSORT for per-individual tracking across frames. Build a dedicated flight-mode classifier with quantitative descriptors - flap frequency in Hertz, altitude gain in metres per second, thermal radius. Move to full multimodal Bayesian fusion combining vision, behaviour, phenology, and geography at the posterior level. And expand to Strigiformes - the owls - which requires night-vision plus audio modalities, and that's where this project connects to my bioacoustics work."**

### Q2.3 - How does this project prepare me for bioacoustics?

> **"This project taught me that the same person who builds a visual classifier can also build the behaviour module, the GUI, the Bayesian fusion, the reproducibility infrastructure - it taught me to build end-to-end systems. For bioacoustics specifically, the Bayesian fusion idea is exactly what extends naturally to audio: instead of fusing image and behaviour, the multimodal V2 fuses image and audio. The mathematical framework is already in place."**

---

## PROJECT 3 - BioAcoustics Fauna Identification

### Q3.1 - Why this project? What problem does it solve?

> **"Many species are heard before they are seen - bats, frogs, crickets, nocturnal mammals, owls. Visual-only systems miss them entirely. Passive acoustic monitoring with low-cost recorders like AudioMoth is the standard for ecological monitoring at scale, but it produces terabytes of audio nobody can listen to manually. AI is mandatory at this scale.**
>
> **Existing solutions are taxon-specific - BirdNET for birds, BatDetect for bats. There is no unified open-source toolkit that handles chiroptera, anura, vocal mammalia, reptilia, and insecta in one system, each with its own per-taxon presets for sample rate and preprocessing. My project is that unified toolkit.**
>
> **The application is large-scale passive acoustic monitoring in protected areas, with automatic species detection, geographic indexing, and a REST API biologists can call from R or Python."**

### Q3.2 - How did you build it and how can it be improved?

> **"Six layers. Acquisition: AudioMoth or SM4BAT to wave files. Preprocessing in source slash audio-processing: bandpass filter to the taxon's frequency range, noise reduction with the noisereduce library, voice activity detection, segmentation. Feature extraction: Mel spectrogram, MFCC with first and second derivatives, zero-crossing rate, spectral centroid, chroma. Classification: three architectures - a custom BioAcousticCNN with residual blocks as baseline, EfficientNet B0 and B4 with transfer learning, and PANNs-CNN14 which is pre-trained on AudioSet. Storage: PostgreSQL 15 with PostGIS for spatial indexing, full taxonomic schema. API: FastAPI async with async-pg, endpoints for classify, detections, species.**
>
> **Production stack: Docker compose orchestrates the API plus PostgreSQL plus pgAdmin plus MLflow. GitHub Actions runs the CI with thirty-five unit tests on preprocessing and fifty tests on the models. Models export to ONNX and TorchScript for edge deployment on Raspberry Pi or AudioMoth.**
>
> **How to improve it: first, multi-species detection in overlapping audio segments - currently I assume one species per segment, but real soundscapes overlap. Second, few-shot site adaptation - each recording site has its own soundscape, and a small fine-tuning pass per site improves accuracy substantially. Third, an active-listening loop where the system samples more around uncertain detections. Fourth, federated learning across recorder networks. And fifth, fusion with camera-traps - when an audio detection matches a visual identity at the same site within seconds, confidence is much higher."**

### Q3.3 - Are you comfortable with bioacoustics?

> **"Yes. I already have a working passive acoustic monitoring system. Version 0.3 is running with three classifier architectures including PANNs-CNN14 pre-trained on AudioSet, a FastAPI REST service, PostgreSQL with PostGIS, Docker compose for orchestration, and CI/CD on GitHub Actions. The natural next step is the multi-modal fusion with my visual raptor work. That fusion is exactly what I want to do for the doctorate."**

---

## The synthesis - if the professor asks "what next?"

> **"My doctorate would be the multi-modal fusion of these three pipelines. A single system where the visual classifier and the audio classifier vote together through a Bayesian fusion at the posterior level; where the sign-language layer guarantees accessibility for the Deaf community; and where the output feeds biodiversity infrastructure like the Atlas of Living Australia, GBIF, and iNaturalist through Darwin Core. Working title: multi-modal artificial intelligence for biodiversity identification at scale, accessible to the Deaf community.**
>
> **The first year I would deliver a clean benchmark of the silhouette-first work for Methods in Ecology and Evolution; prototype the multimodal fusion on one site with both camera-trap photos and audio; and release a reproducibility report and open licences for the three current projects.**
>
> **That's what I'm here to discuss with you."**

---

## Quick reference card - just the bold sentences

If you can keep these eight sentences clear in your head, you have the meeting.

1. *"My research program is multi-modal AI for biodiversity identification with accessibility built in."*
2. *"Project one is the Australian Raptor CNN. F1 point-eight-five on eight species."*
3. *"Project two is my master's thesis: 53 raptors of Mexico, four architectures benchmarked, silhouette plus behaviour plus International Sign."*
4. *"Project three is a bioacoustics system for passive acoustic monitoring of five taxa."*
5. *"They are not three accidents. They define a research program."*
6. *"Yes, I am comfortable with bioacoustics. I already have a working PAM system."*
7. *"The doctorate is the multi-modal fusion: vision plus audio plus sign language."*
8. *"That's why I asked for this conversation."*

You have this.
