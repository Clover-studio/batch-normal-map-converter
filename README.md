🌀 Batch Normal Map Converter (OpenGL ↔ DirectX)

This Python script automatically converts normal maps between OpenGL and DirectX formats by flipping the green (Y) channel — the only difference between the two systems.

Unlike manual converters, this script can process entire folders recursively. Simply give it one main folder, and it will:

    Search all subfolders inside it

    Convert only files whose names contain both “normal” and “map”

    Save the converted version next to the original file

    Keep the same file format as the original (e.g., .tga to .tga, .exr to .exr) [ADDED]

    Add a suffix (for example _DX or _GL) to the new converted file

    Keep your original normal maps untouched

You don’t need to convert one by one — it does all of them automatically.

📦 What It Does

    ✅ Batch converts OpenGL ↔ DirectX normal maps

    ✅ Recursively scans subfolders inside a given folder

    ✅ Converts only relevant files (normal + map in filename)

    ✅ Preserves the original file format/extension (e.g., PNG remains PNG, EXR remains EXR) [UPDATED]

    ✅ Keeps the original files safe

    ✅ Adds a suffix (_DX or _GL) to converted versions

    ✅ Supports .png, .jpg, .tga, .tif, .bmp, .webp, .exr, etc. [UPDATED]

🧰 Requirements

You need Python 3 installed on your computer.

🔹 Step 1 — Check if Python is installed

Open Command Prompt (Windows) or Terminal (macOS/Linux) and type:

     python --version

If you get a version like Python 3.10 or higher, you’re good to go.

If not, download and install Python from the official website: https://www.python.org/downloads/

🔹 Step 2 — Install the required libraries

Once Python is installed, open a Command Prompt and run this command. Note that the opencv-python library is mandatory for handling .exr files. 

     python -m pip install pillow numpy opencv-python

🔹 Step 3 — (Optional) For EXR Support

If you plan to convert .exr files and encounter installation errors, you may need to install the Visual C++ Build Tools (on Windows) to successfully compile dependencies like NumPy and OpenCV. This is usually done by installing the "Desktop development with C++" workload in the Visual Studio Installer. 

🚀 How to Use the Script

- Download the file: convert_normals_inplace.py

- Place it anywhere convenient e.g.: C:\Tools\convert_normals_inplace.py

- Open Command Prompt in that same folder, or navigate to it:

- Run one of the following commands:

➤ To Convert from OpenGL → DirectX

     python convert_normals_inplace.py "D:\Your\Top\Folder" --mode ogl2dx --suffix _DX

➤ To Convert from DirectX → OpenGL

     python convert_normals_inplace.py "D:\Your\Top\Folder" --mode dx2ogl --suffix _GL

Flag	Description
--suffix _DX	Text added to converted file name

--Example :

D:\3D_Assets\
 ├─ rocks\
 │   ├─ rock_normal_map.png
 │   └─ rock_albedo.png
 ├─ walls\
 │   ├─ wall_normal_map.tga
 │   └─ wall_diffuse.jpg

Run: python convert_normals_inplace.py "D:\3D_Assets" --mode ogl2dx --suffix _DX

Result:

D:\3D_Assets\
 ├─ rocks\
 │   ├─ rock_normal_map.png
 │   ├─ rock_normal_map_DX.png   ← converted version (.png kept)
 ├─ walls\
 │   ├─ wall_normal_map.tga
 │   ├─ wall_normal_map_DX.tga   ← converted version (.tga kept)

🧠 Notes

The conversion only flips the Y (green) channel — that’s the only difference between OpenGL and DirectX normal maps. The script is non-destructive — your originals are safe. Works with high-res textures (tested up to 8K).

🧑‍💻 Author

Zakarya CHIOUA 3D Game Artist CLOVER

https://www.linkedin.com/company/clover-studio-ma

https://x.com/clover_morocco

https://www.instagram.com/clover.studio.ma/

MIT License — free to use, modify, and share.
