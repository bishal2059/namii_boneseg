# Pipeline Explanation: 3D Bone Segmentation & Landmark Detection

## 1. Overview of Workflow


* **Input**: 3D CT volume of knee region in NIfTI format (data/knee\_ct.nii).
* **Step 1**: Bone Segmentation (src/segmentation.py)
* **Step 2**: Mask Expansion (src/expansion.py)
* **Step 3**: Contour Randomization (src/randomization.py)
* **Step 4**: Landmark Detection (src/landmarks.py)
* **Step 5**: Visualization (src/visualize.py & src/overlay\_visualize.py)
* **Output**: Binary masks (.nii.gz), landmark coordinates (.txt), and PNG figures (.png)

---

## 2. Packages and Dependencies


* **nibabel**: Read/write NIfTI volumes (load and save operations)
* **numpy**: Numerical operations, array manipulations
* **scipy.ndimage**: Distance transforms, voxel-based dilation
* **scikit-image**: Morphological clean-up, labeling, region properties
* **SimpleITK**: Physical-space distance maps, contour-based operations (in some versions)
* **matplotlib**: Plotting and saving visualization figures

---

## 3. Detailed Function Descriptions


### 3.1 src/utils.py

* `load_nifti(path)`:

  * Loads a NIfTI file using nibabel.
  * Returns: 3D numpy array, affine matrix, header.
* `save_nifti(data, affine, header, path)`:

  * Saves a binary mask (uint8) to NIfTI.
* `get_spacing(header)`:

  * Extracts voxel spacing (x, y, z) from header metadata.
* `mm_to_voxel(spacing, mm)`:

  * Converts physical mm into integer voxel distances per axis.

### 3.2 src/segmentation.py

* `segment_bone(volume, threshold_hu)`:

  1. Apply global threshold: `mask = volume >= threshold_hu`.
  2. Remove small objects (<1000 voxels) and holes (<1000 voxels).
  3. Label connected components; compute areas via `regionprops`.
  4. Retain two largest components (femur and tibia). Output binary combined mask.

**Expected Result**: `combined_mask.nii.gz` containing femur + tibia segmentation.

### 3.3 src/expansion.py

* `expand_mask(mask, spacing, radius_mm)`:

  * Compute Euclidean distance transform on background voxels (scipy or SimpleITK).
  * Threshold distances at `radius_mm` to create expanded mask.
  * Using SciPy: transform(mm->voxels) -> spherical structuring element -> binary\_dilation.

**Expected Results**:

* `expanded_2mm.nii.gz` (2 mm dilation)
* `expanded_4mm.nii.gz` (4 mm dilation)

### 3.4 src/randomization.py

* `randomize_mask(original, expanded, spacing, max_radius_mm)`:

  1. Compute distance map from original mask (in mm).
  2. Clamp distances at max\_radius\_mm.
  3. Sample random threshold per voxel: `rnd[i] in [0, max_mm]`.
  4. Create mask where `dist >= rnd` and within expanded region.
  5. Merge with original mask to ensure no shrinkage.

**Expected Results**:

* `random1.nii.gz` (random within 2 mm)
* `random2.nii.gz` (random within 4 mm)

### 3.5 src/landmarks.py

* `find_lowest_medial_lateral(mask, affine)`:

  1. Extract voxel coordinates of mask (z,y,x).
  2. Transform to physical coordinates via affine.
  3. Split points by median X-plane (medial vs lateral).
  4. Identify point with minimal Z in each group.
  5. Return two 3D coordinates in mm.

**Output**: `results/landmarks.txt` with lines:

```
combined_mask, medial: (x,y,z), lateral: (x,y,z)
expanded_2mm, medial: ..., lateral: ...
...
```

### 3.6 src/visualize.py

* `visualize_slices(mask_paths, output_dir, slice_index)`:

  * Loads each mask, plots central axial slice side-by-side.
  * Saves figure as `compare_slice_<slice>.png`.

### 3.7 src/overlay\_visualize.py

* `save_original_slice`:

  * Plots CT slice alone.
* `overlay_each_mask`:

  * Overlays each mask contour in red on CT slice, with titles and indices.
* `overlay_comparison`:

  * Generates side-by-side panels of Combined, 2mm, 4mm overlays.

**Output**: PNG images in `results/visualize/`.

---

## 4. Data Flow Overview


```plaintext
[data/knee_ct.nii]
        |
        v
[segment_bone] --(combined_mask)--> results/masks/combined_mask.nii.gz
        |
        +---> [expand_mask] --expanded masks--> results/masks/expanded_*.nii.gz
        |
        +---> [randomize_mask] --randomized masks--> results/masks/random*.nii.gz
        |
        +---> [find_lowest_medial_lateral] --> results/landmarks.txt
        |
        +---> [visualize_slices] & [overlay_visualize]
                       |
                       v
          results/visualize/*.png
```

---

## 5. Expected Artifacts


* **NIfTI Masks**: Binary volumes of segmentation and variants.
* **Landmarks**: Text file with mm-precision coordinates.
* **Figures**: Publication-quality PNG overlays for QA and demonstration.

---

## 6. Best Practices & Extensibility


* **Modularity**: Each task isolated in its own module.
* **Parameterization**: Thresholds and radii configurable via CLI.
* **Reproducibility**: Random seeds can be set if needed for consistency.
* **Logging**: Comprehensive console prints trace pipeline state.
* **Extension Points**: Swap segmentation method, add multi-slice visualization, integrate GUI.
