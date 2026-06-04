# Video data

This folder holds **field videos** used for the flight-behaviour module (V2).
It mirrors the structure of `datos/raw/` and `datos/processed/` for images.

```
datos/videos/
├── raw/                          original clips, as recorded
│   ├── Aquila_chrysaetos/
│   │   ├── clip_001.mp4
│   │   └── clip_002.mp4
│   ├── Buteo_jamaicensis/
│   │   └── ...
│   └── <Genus_species>/
├── processed/                    after standardisation
│   ├── Aquila_chrysaetos/
│   │   ├── clip_001_30fps_720p.mp4
│   │   └── ...
│   └── <Genus_species>/
└── annotations/                  per-clip labels (CSV)
    └── clips.csv                 columns: file, species, n_birds, flight_mode, start_s, end_s
```

## Naming convention

- Species folders use the **scientific name with underscore**, same as
  `datos/raw/` and `config.SPECIES`. For example `Buteo_platypterus`,
  NOT `Broad-winged_Hawk` and NOT `BWHA`.
- Clip files inside each species folder can be named freely.
  Recommendation: `clip_001.mp4`, `clip_002.mp4`, ... so the order
  on disk matches the order in the annotations CSV.

## Where each kind of video lives

| Purpose | Location |
|---|---|
| Behaviour-module training (V2, 3D-CNN) | here: `datos/videos/raw/<species>/` |
| Showing a behaviour clip in the Flask GUI | `codigo/pytorch/app_flask/static/behavior_videos/<species>.mp4` (one per species) |
| International Sign vocabulary | `lengua_de_senas/videos/<species>.mp4` |

If you only want the video to **appear in the GUI** for demonstration, put a
copy in `codigo/pytorch/app_flask/static/behavior_videos/` with the exact
species filename — the template auto-detects it.

## How to add new videos progressively

1. Watch the clip and identify the species.
2. Drop the file under `datos/videos/raw/<Genus_species>/`. Create the
   folder if it does not exist.
3. If you also want it visible in the GUI Species Guide, copy or symlink
   it to `codigo/pytorch/app_flask/static/behavior_videos/<species>.mp4`.
4. If you label the flight modes (soaring, flap-glide, hovering, stoop,
   active), add a row to `datos/videos/annotations/clips.csv` so the
   future training script can use it.

## Format recommendations (for V2 training)

- Container: MP4 (H.264) or MKV
- Resolution: at least 720p; 1080p preferred
- Frame rate: 30 fps (the V2 3D-CNN samples at 8-16 fps internally, but
  30 fps gives headroom for temporal jitter augmentation)
- Duration: 5-30 seconds per clip; longer clips can be split

A preprocessing script `scripts/standardise_videos.py` is on the V2
roadmap; until then videos can stay in their original recording format.
