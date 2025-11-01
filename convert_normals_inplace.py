#!/usr/bin/env python3
"""
convert_normals_inplace.py
--------------------------
Batch-convert normal maps between OpenGL and DirectX (flip GREEN/Y channel).

New behavior (per user request):
- Give ONE folder that contains many subfolders with normal maps.
- The script will walk every subfolder and convert ONLY files whose names
  contain BOTH words "normal" AND "map" (case-insensitive).
- The converted files are saved in the SAME folder as the original, with a suffix.

Also works if you pass a single file as input.

Usage examples:
  python convert_normals_inplace.py "D:/Assets" --mode ogl2dx --suffix _DX
  python convert_normals_inplace.py "D:/Assets" --mode dx2ogl --suffix _GL --keep-ext
  python convert_normals_inplace.py "D:/Assets/rocks/rock_normal_map.png"

Notes:
- "ogl2dx" (default) flips Y for OpenGL -> DirectX; "dx2ogl" does the same flip (the inverse operation is identical).
- Preserves alpha channel if present.
- Saves PNG by default to avoid artifacts; use --keep-ext to retain original extension.
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

def convert_image_inplace(path_in: Path, suffix: str = '_DX', keep_ext: bool = False) -> Path:
    # Open and ensure RGBA
    img = Image.open(path_in).convert('RGBA')
    arr = np.array(img, dtype=np.uint8)

    # Flip GREEN (Y) channel
    arr[..., 1] = 255 - arr[..., 1]

    out = Image.fromarray(arr, mode='RGBA')

    # Build output filename next to the original
    stem = path_in.stem + suffix
    out_path = path_in.with_name(stem + (path_in.suffix if keep_ext else '.png'))

    # Save result
    save_params = {}
    if out_path.suffix.lower() in ('.jpg', '.jpeg'):
        save_params['quality'] = 95
    out.save(out_path, **save_params)
    return out_path

def main():
    parser = argparse.ArgumentParser(description="Flip Y channel of normal maps (OpenGL <-> DirectX), in-place next to originals.")
    parser.add_argument('input', type=str, help='Input file or top-level folder to search recursively')
    parser.add_argument('--mode', choices=['ogl2dx', 'dx2ogl'], default='ogl2dx',
                        help='Conversion direction label (both flip Y; this is for your reference).')
    parser.add_argument('--suffix', type=str, default='_DX',
                        help='Suffix appended to output filename (e.g., _DX or _GL).')
    parser.add_argument('--keep-ext', action='store_true',
                        help='Keep original file extension; default saves PNG.')
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
        out_path = convert_image_inplace(f, suffix=args.suffix, keep_ext=args.keep_ext)
        print(f"  - {f} -> {out_path}")
    print("Done.")

if __name__ == '__main__':
    main()
