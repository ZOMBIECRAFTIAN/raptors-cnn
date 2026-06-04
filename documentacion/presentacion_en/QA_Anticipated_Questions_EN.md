# Q&A - anticipated questions with ready answers

The 30 questions a US-based professor of AI / ecology / signal processing will most likely ask after seeing your three projects, plus the answer in English. Print this. Read it twice. Cover the question column with your hand and try to answer; check yourself.

The answers are tuned to the **three axes** the professor told you to prepare:
1. **Justification** (why this project, what problem it solves)
2. **Construction process** (how you built it, how to improve it)
3. **Bioacoustics readiness** (whether you can extend to audio)

---

## Section A - Justification questions

**Q1. Why three projects instead of one focused thesis?**
A. *"Each project answered a different question and taught me something the next one needed. Australia proved transfer learning + signed-language accessibility could work. Mexico proved I could scale the same recipe by 6x and add behaviour fusion. Bioacoustics proved I can work in a completely different modality at production grade. Together they define the research program, which is multi-modal biodiversity ID. A single project would not let me prove range, depth, and direction at once."*

**Q2. What problem does the Mexico project solve that BirdNET or Merlin Bird ID does not?**
A. *"Merlin and iNaturalist train on perched birds with rich colour photographs - useless when a raptor is in flight against bright sky, which is most field observations. My silhouette-targeted augmentations and the flight-behaviour module imitate the way an expert decides: by shape and cadence, not colour. To my knowledge, no published raptor identifier fuses silhouette CNN with quantitative flight-behaviour priors."*

**Q3. Why did you choose International Sign instead of ASL or LSM?**
A. *"International Sign is the cross-national lingua franca documented by the World Federation of the Deaf. It maximises reach. I document equivalents in Mexican Sign Language and ASL where possible as a reference column, but the main catalogue is IS so that a deaf scientist anywhere can use it. ASL or LSM would limit the audience geographically."*

**Q4. Why bioacoustics for fauna identification? Is it not solved by BirdNET?**
A. *"BirdNET is audio-only and bird-only. My system covers five taxonomic groups - chiroptera, anura, orthoptera, vocal mammalia, and reptilia - each with very different signal characteristics. Bats need 192 kHz sample rate for echolocation, anurans need 22 kHz for mating calls. A unified system that handles all of them, with PostgreSQL spatial indexing and a FastAPI service, does not exist as open-source in one toolkit."*

**Q5. Why Mexico-specific? Does this generalise?**
A. *"The 53 species cover all diurnal raptors documented in Mexico under the AOS 2024 checklist. Most also occur in the southern US, Central America, and northern South America. The model is trained on Mexico data but the species set is regionally complete, so it generalises to the entire neotropical migratory corridor."*

**Q6. Is this a master's project or a doctoral project?**
A. *"The master's thesis is project 2: Mexico raptors V1.1, with the silhouette focus and the IS catalogue and the V1 Bayesian prior. The doctorate is the multi-modal V2: 3D-CNN behaviour, full multimodal Bayes, and the fusion with the bioacoustics work. The portfolio shows the path from one to the other."*

**Q7. What is the strongest contribution of all three projects?**
A. *"The combination. Each project has merit alone: Australia is a clean reproducible benchmark, Mexico is a scale-up with novel silhouette focus, bioacoustics is a production-grade multi-taxa system. The doctoral synthesis - vision + audio + sign language for accessible biodiversity ID - is what I have not seen published anywhere."*

---

## Section B - Construction process questions

**Q8. Walk me through the Mexico pipeline from a fresh user.**
A. *"They run scripts/windows/descargar_v1_1.bat which downloads images from iNaturalist. Then scripts/windows/pipeline_completo_v1_1.bat curates with curate.py, splits 70/15/15, runs a smoke test, then trains ResNet-50 in two stages. Finally they run python app.py from app_flask and drag a photo in the browser. End-to-end on a fresh machine: about ten hours including download."*

**Q9. Why ResNet-50 as baseline and not something newer?**
A. *"ResNet-50 is the most reported model in the ornithological AI literature since 2018. Choosing it as baseline lets me compare against published numbers directly. ConvNeXt-Tiny is my SOTA challenger in the same benchmark. The full comparison is in codigo/comparacion/comparar_arquitecturas.py."*

**Q10. Why two-stage training? Why not just end-to-end fine-tuning?**
A. *"Fine-tuning a full backbone with a randomly initialised head can destroy pre-trained features in the first few epochs - the gradient from the random head is too large. Stage one stabilises the head with the backbone frozen, then stage two unfreezes everything safely. This is the ULMFiT recipe from Howard and Ruder 2018."*

**Q11. How do you measure sharpness in curate.py?**
A. *"Variance of the Laplacian on the image. Low variance signals blur. I set the threshold empirically by labelling a calibration set of 200 images by hand. The function is curate.py, _sharpness()."*

**Q12. How do you handle the class imbalance?**
A. *"Three layers. First, weighted cross-entropy with weights inversely proportional to class frequency. Second, Mixup with alpha 0.2 and CutMix with alpha 1.0 - both implicitly oversample rare classes. Third, in V2, synthetic minority oversampling with diffusion-generative augmentation."*

**Q13. Why Cohen's kappa 0.85 as the floor and not 0.80?**
A. *"Landis and Koch 1977 calls 0.81-1.00 'almost perfect agreement.' 0.61-0.80 is only 'substantial.' For fine-grained species ID where confusing species are taxonomically close, anything below 'almost perfect' lets too much noise into the training set."*

**Q14. How does the bioacoustics preprocessing pipeline work?**
A. *"Bandpass filter to the taxon's frequency range, noise reduction with the noisereduce library which uses spectral gating, normalisation, voice activity detection to find audible segments, and finally segmentation into fixed-length windows. Each taxon has its own preset because the frequencies are completely different - 200 kHz for bats, 8 kHz for frogs."*

**Q15. What does PANNs-CNN14 give you that EfficientNet does not?**
A. *"PANNs is pre-trained on AudioSet, which is the audio equivalent of ImageNet but ten times larger. EfficientNet pre-trained on images cannot exploit acoustic structure as well, even when you turn the spectrogram into a 3-channel image. PANNs has already learned what bird calls, mammal vocalisations, and environmental sounds look like in the spectral domain."*

**Q16. How do you keep the three projects consistent in terms of code quality?**
A. *"Each repo has the same skeleton: README, LICENSE, CITATION.cff, environment files, configs centralised in one config.py, requirements.txt for pip and environment.yml for conda. Mexico uses .bat scripts for Windows users; bioacoustics uses Docker compose. All three are MIT licensed."*

**Q17. How reproducible are these projects?**
A. *"All three fix seeds at 42. Mexico has three environment files - CUDA, MPS for Apple Silicon, and CPU - that all give the same results. Bioacoustics ships a Dockerfile and docker-compose so the entire stack reproduces with a single command. SHA-256 of every image is logged for Mexico and Australia."*

**Q18. How long would it take to train Mexico from scratch on a new GPU?**
A. *"Four to eight hours for ResNet-50 on an RTX 3050 with 4 GB VRAM using mixed precision and gradient accumulation. About two hours on a 3060. The smoke test - one epoch to verify everything is wired - takes five minutes."*

**Q19. What does the Flask GUI actually call?**
A. *"app.py loads the best checkpoint into memory on startup. When a user uploads, it runs the inference pipeline, generates a Grad-CAM via the gradcam.py module, pulls species facts from species_data.py, and returns JSON to the JavaScript front end which renders the top-3, the heatmap overlay, the fact sheet, and the sign-language video. All in vanilla JS - no React. Less than 500 lines of JS total."*

**Q20. Why FastAPI and not Flask for the bioacoustics project?**
A. *"FastAPI is async-native, which matters because audio classification is I/O bound when you stream from a recorder. Flask is sync-default and would block. FastAPI also gives me an OpenAPI schema for free, which is important for an API that biologists will call from R or Python."*

---

## Section C - Improvement and doctorate questions

**Q21. If you joined my program, what would you do in your first three months?**
A. *"First, deliver a clean comparative report of the four architectures on the Mexico dataset - that closes the V1.1 thesis. Second, prototype the multimodal fusion: a small site with both camera-trap photos and audio, predicted by both pipelines, fused at the posterior. Third, draft the silhouette-first paper for Methods in Ecology and Evolution. After that, depending on your guidance, I would either deepen the behaviour module or expand the bioacoustic taxa."*

**Q22. What is the main risk in your doctoral plan?**
A. *"Data acquisition for rare species. Harpy Eagle, Crested Eagle, Orange-breasted Falcon all have fewer than 100 photos public. I have outreach to The Peregrine Fund's Mesoamerican programme and to CONABIO's archives, but partnerships take time. The bioacoustics side has the opposite problem - too much audio, not enough labelled."*

**Q23. How would you fund the field work?**
A. *"For the visual side, AudioMoth recorders and camera-traps cost about 100 USD each; 20 stations is 2000 USD. For the audio annotation, I can apply to the Cornell Lab of Ornithology citizen-science programmes or the Smithsonian Tropical Research Institute. There are also Mexican national grants - CONACYT - and the Mohamed bin Zayed Species Conservation Fund."*

**Q24. Why should we accept you over candidates with published papers?**
A. *"Because I have shipped three working systems with code, tests, documentation and reproducibility infrastructure, while many candidates have one paper and one notebook. I am at the stage where the first paper is the next deliverable, not the entry ticket. My GitHub profile is the equivalent of a 30-page CV - it shows exactly what I can do."*

**Q25. What do you want from a supervisor?**
A. *"Honest feedback on methodology, especially on the Bayesian fusion. Help finding the right venue for each contribution. Access to your institutional network for partnerships with deaf communities and conservation NGOs. And the freedom to keep the open-source ethos of the three current projects."*

**Q26. Would you be comfortable teaching a class?**
A. *"Yes. I co-wrote the documentation of all three projects in bilingual Spanish-English, including installation manuals for users with no AI background. The Mexico manual covers Windows / Linux / Mac with and without GPU. I would be happy to teach an intro deep-learning course or an applied AI for ecology course."*

**Q27. Are you comfortable with bioacoustics?**
A. *"Yes - I already have a working passive acoustic monitoring system. Version 0.3 is running with three classifier architectures including PANNs-CNN14 pre-trained on AudioSet, FastAPI, PostgreSQL with PostGIS, Docker compose, and CI/CD. The natural next step is the multi-modal fusion with my visual raptor work, which is exactly what I want to do for the doctorate."*

**Q28. Where do you see your work in five years?**
A. *"A multi-modal biodiversity ID API that anyone can call - federated, Darwin Core compliant, deployable on edge devices, accessible to the Deaf community via signed-language video output. Used by protected-area managers across the Americas and Australasia. That is the thesis target."*

**Q29. What if the multimodal fusion does not give a clear improvement over single-modality models?**
A. *"That is a publishable negative result, and it is interesting in itself. It would tell us when audio and vision are redundant vs complementary. I have a fallback chapter that discusses ablation outcomes. My doctorate is defensible whether the fusion gain is 30 percent or only 5 percent - the contribution is the framework, not the specific delta."*

**Q30. What do you do if I tell you your silhouette-first approach is wrong?**
A. *"I would ask why, listen carefully, and consider it seriously. If I disagree after thinking, I would explain my reasoning with the evidence I have - the augmentation ablation, the Grad-CAM audit, the operational match with expert ornithologists' descriptions. But I would not dismiss the criticism just because I built it. The point of coming to talk to you is to find out where I am wrong."*

---

## Five recovery phrases for genuine "I don't know"

1. *"That is a great question. I have not measured that directly, but my intuition is X - I will verify and follow up."*
2. *"You are right that this is a limitation. I document it in chapter 5, section 3."*
3. *"The honest answer is I don't know yet - that experiment is in the roadmap."*
4. *"Let me think about that for a moment."* (3 seconds is fine - it shows you are thinking)
5. *"Could you help me make sure I understood the question correctly?"*

Any of these is better than guessing wrong.

---

## Three Spanish-to-English traps

- *"Es decir"* → say "**that is**" or "**in other words**", not "it says"
- *"En este sentido"* → say "**in this regard**" or skip it, not "in this sense"
- *"O sea"* → say "**that is to say**" or skip it; *never* say "or be" in English
