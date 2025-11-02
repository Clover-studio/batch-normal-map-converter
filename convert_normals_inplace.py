#!/usr/bin/env python3
"""
convert_normals_inplace.py  (OpenCV EXR edition w/ auto-enable)
---------------------------------------------------------------
Batch-convert normal maps between OpenGL and DirectX by flipping the GREEN (Y) channel.

- Recursively scans subfolders starting from a given folder (or accepts a single file).
- Converts ONLY files whose names contain BOTH "normal" AND "map" (case-insensitive).
- Saves the converted file NEXT TO the original with a suffix (default: _DX).
- Keeps the SAME file format/extension as the original (PNG->PNG, TGA->TGA, EXR->EXR).
- EXR handled via OpenCV (cv2). This script auto-enables EXR by setting OPENCV_IO_ENABLE_OPENEXR=1.
"""

import argparse
import os
from pathlib import Path

# Auto-enable EXR reader in OpenCV builds that gate it behind an env var
os.environ.setdefault('OPENCV_IO_ENABLE_OPENEXR', '1')

from PIL import Image
import numpy as np

# Optional EXR via OpenCV
try:
    import cv2
    _HAS_CV2 = True
except Exception:
    _HAS_CV2 = False

VALID_EXTS = {'.png', '.jpg', '.jpeg', '.tga', '.tif', '.tiff', '.bmp', '.webp', '.exr'}

def looks_like_normal_map(filename: str) -> bool:
    n = filename.lower()
    return ("normal" in n) and ("map" in n)

def _has_alpha_mode(mode: str) -> bool:
    return mode in ('RGBA', 'LA', 'PA')

def _save_with_params(img: Image.Image, path: Path, orig_mode: str):
    ext = path.suffix.lower()
    params = {}
    if ext in ('.jpg', '.jpeg'):
        if img.mode != 'RGB':
            img = img.convert('RGB')
        params.update(dict(quality=95, subsampling=1, optimize=True))
    elif ext == '.tga':
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGBA' if _has_alpha_mode(orig_mode) else 'RGB')
    elif ext in ('.tif', '.tiff'):
        params['compression'] = 'tiff_lzw'
    img.save(path, **params)

def _process_exr_cv2(path_in: Path, path_out: Path, exr_negpos: bool):
    if not _HAS_CV2:
        print(f"  ! Skipping (needs opencv-python): {path_in}")
        return None

    arr = cv2.imread(str(path_in), cv2.IMREAD_UNCHANGED)
    if arr is None:
        print(f"  ! OpenCV failed to read (check OPENCV_IO_ENABLE_OPENEXR=1): {path_in}")
        return None

    if arr.ndim != 3 or arr.shape[2] < 3:
        print(f"  ! Unexpected EXR shape: {path_in} -> {arr.shape}")
        return None

    # OpenCV returns BGR(A): channel 1 is G
    G = arr[:, :, 1].astype(np.float32)

    if exr_negpos:
        G = -((G * 2.0) - 1.0)
        G = (G * 0.5) + 0.5
    else:
        G = 1.0 - G

    G = np.clip(G, 0.0, 1.0)
    arr[:, :, 1] = G

    ok = cv2.imwrite(str(path_out), arr)
    if not ok:
        print(f"  ! OpenCV failed to write: {path_out}")
        return None
    return path_out

def convert_image_inplace(path_in: Path, suffix: str = '_DX', exr_negpos: bool = False) -> Path:
    ext = path_in.suffix.lower()
    stem = path_in.stem + suffix
    out_path = path_in.with_name(stem + path_in.suffix)

    if ext == '.exr':
        return _process_exr_cv2(path_in, out_path, exr_negpos)

    # Non-EXR path: use Pillow
    src = Image.open(path_in)
    orig_mode = src.mode
    img = src.convert('RGBA')
    arr = np.array(img, dtype=np.uint8)
    arr[..., 1] = 255 - arr[..., 1]  # flip G

    if _has_alpha_mode(orig_mode) or ('transparency' in src.info):
        out_img = Image.fromarray(arr, mode='RGBA')
    else:
        out_img = Image.fromarray(arr[..., :3], mode='RGB')

    _save_with_params(out_img, out_path, orig_mode)
    return out_path

def main():
    parser = argparse.ArgumentParser(description="Flip Y channel of normal maps (OpenGL <-> DirectX), save next to originals with SAME format. EXR via OpenCV (auto-enabled).")
    parser.add_argument('input', type=str, help='Input file or top-level folder to search recursively')
    parser.add_argument('--mode', choices=['ogl2dx', 'dx2ogl'], default='ogl2dx')
    parser.add_argument('--suffix', type=str, default='_DX')
    parser.add_argument('--exr_negpos', action='store_true', help='Use if your EXR normals are encoded in -1..1.')
    args = parser.parse_args()

    in_path = Path(args.input)

    files = []
    if in_path.is_file():
        if in_path.suffix.lower() in VALID_EXTS and looks_like_normal_map(in_path.name):
            files = [in_path]
    else:
        for root, _, fnames in os.walk(in_path):
            for f in fnames:
                p = Path(root) / f
                if p.suffix.lower() in VALID_EXTS and looks_like_normal_map(f):
                    files.append(p)

    if not files:
        print("No matching normal map files found (must contain both 'normal' and 'map' in the filename).")
        return

    print(f"Converting {len(files)} file(s) (mode={args.mode}) ...")
    for f in files:
        out_path = convert_image_inplace(f, suffix=args.suffix, exr_negpos=args.exr_negpos)
        if out_path is None:
            continue
        print(f"  - {f} -> {out_path}")
    print("Done.")

if __name__ == '__main__':
    main()
