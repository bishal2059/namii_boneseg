# 3D Bone Segmentation & Landmark Detection Pipeline

## Overview
This pipeline segments femur and tibia from a knee CT, expands and randomizes the contour, and extracts medial/lateral lowest points on each mask.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python -m src.main --input data/knee_ct.nii --output_dir results --threshold 300 --expand1 2 --expand2 4
```

This will generate masks under `results/masks/` and write coordinates to `results/landmarks.txt`.