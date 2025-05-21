import nibabel as nib
import numpy as np

def load_nifti(path):
    img = nib.load(path)
    data = img.get_fdata()
    return data, img.affine, img.header

def save_nifti(data, affine, header, path):
    out = nib.Nifti1Image(data.astype(np.uint8), affine, header)
    nib.save(out, path)

def voxel_to_mm(spacing, voxels):
    return voxels * np.array(spacing)

def mm_to_voxel(spacing, mm):
    return (np.array(mm) / np.array(spacing)).astype(int)

def get_spacing(header):
    return header.get_zooms()[:3]