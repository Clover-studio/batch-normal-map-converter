#!/usr/bin/env python3
"""
convert_normals_inplace.py
--------------------------
Batch-convert normal maps between OpenGL and DirectX (flip GREEN/Y channel).

Behavior:
- Give ONE folder that may contain many subfolders.
- The script scans recursively and converts ONLY files whose names contain BOTH words
  "normal" AND "map" (case-insensitive).
- The converted file is saved NEXT TO the original, with a suffix (default: _DX).
- The converted file keeps the SAME FORMAT/EXTENSION as the original.  (e.g., JPG -> JPG, TGA -> TGA)

Usage examples:
  python convert_normals_inplace.py "D:/Assets" --mode ogl2dx --suffix _DX
  python convert_normals_inplace.py "D:/Assets" --mode dx2ogl --suffix _GL
  python convert_normals_inplace.py "D:/Assets/rocks/rock_normal_map.png"

Notes:
- "ogl2dx" (default) flips Y for OpenGL -> DirectX; "dx2ogl" does the same flip (inverse is identical).
- Preserves alpha channel if the original had alpha; if not, saves RGB.
- Supports .png, .jpg, .jpeg, .tga, .tif, .tiff, .bmp, .webp.
"""

import argparse
import os
from pathlib import Path

from PIL import Image
import numpy as np

VALID_EXTS = {'.png', '.jpg', '.jpeg', '.tga', '.tif', '.tiff', '.bmp', '.webp'}

def looks_like_normal_map(filename: str) -> bool:
    n = filename.lower()
    return ("normal" in n) and ("map" in n)

def _has_alpha_mode(mode: str) -> bool:
    # Common alpha-carrying modes
    return mode in ('RGBA', 'LA', 'PA')

def convert_image_inplace(path_in: Path, suffix: str = '_DX') -> Path:
    # Load original and remember attributes
    src = Image.open(path_in)
    orig_mode = src.mode
    orig_suffix = path_in.suffix  # includes dot, e.g. ".png"
    # Convert to RGBA for uniform per-channel manipulation
    img = src.convert('RGBA')
    arr = np.array(img, dtype=np.uint8)

    # Flip GREEN (Y) channel
    arr[..., 1] = 255 - arr[..., 1]

    # Convert back to appropriate mode:
    # - If the source had alpha (or was paletted with alpha), keep RGBA
    # - Otherwise, drop alpha and save as RGB
    if _has_alpha_mode(orig_mode) or ('transparency' in src.info):
        out_img = Image.fromarray(arr, mode='RGBA')
        target_mode = 'RGBA'
    else:
        out_img = Image.fromarray(arr[..., :3], mode='RGB')
        target_mode = 'RGB'

    # Build output path next to original, same extension
    stem = path_in.stem + suffix
    out_path = path_in.with_name(stem + orig_suffix)

    # Save with sane defaults per format
    ext = orig_suffix.lower()
    save_params = {}
    if ext in ('.jpg', '.jpeg'):
        # JPEG has no alpha; ensure RGB
        if target_mode != 'RGB':
            out_img = out_img.convert('RGB')
        save_params['quality'] = 95
        save_params['subsampling'] = 1
        save_params['optimize'] = True
    elif ext in ('.tga',):
        # Ensure correct TGA mode
        if target_mode not in ('RGB', 'RGBA'):
            out_img = out_img.convert('RGBA' if _has_alpha_mode(orig_mode) else 'RGB')
    elif ext in ('.tif', '.tiff'):
        save_params['compression'] = 'tiff_lzw'

    # Save (preserve metadata if possible)
    try:
        out_img.save(out_path, **save_params)
    except OSError:
        out_img.save(out_path)

    return out_path

def main():
    parser = argparse.ArgumentParser(description="Flip Y channel of normal maps (OpenGL <-> DirectX), save next to originals with SAME format.")
    parser.add_argument('input', type=str, help='Input file or top-level folder to search recursively')
    parser.add_argument('--mode', choices=['ogl2dx', 'dx2ogl'], default='ogl2dx',
                        help='Conversion direction label (both flip Y; for your reference).')
    parser.add_argument('--suffix', type=str, default='_DX',
                        help='Suffix appended to output filename (e.g., _DX or _GL).')
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
        out_path = convert_image_inplace(f, suffix=args.suffix)
        print(f"  - {f} -> {out_path}")
    print("Done.")

if __name__ == '__main__':
    main()
