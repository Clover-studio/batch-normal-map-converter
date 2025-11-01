# batch-normal-map-converter
A Python tool to batch convert OpenGL normal maps to DirectX or viceversa, by flipping the green channel.
# 🌀 Batch Normal Map Converter (OpenGL ↔ DirectX)

This Python script automatically converts **normal maps** between **OpenGL** and **DirectX** formats by flipping the **green (Y)** channel — the only difference between the two systems.

Unlike manual converters, this script can process **entire folders recursively**.  
Simply give it **one main folder**, and it will:

- Search all **subfolders** inside it  
- Convert only files whose names contain both **“normal”** and **“map”**  
- Save the **converted version next to the original** file  
- Add a **suffix** (for example `_DX` or `_GL`) to the new converted file  
- Keep your **original normal maps untouched**

You don’t need to convert one by one — it does all of them automatically.  

---

## 📦 What It Does

- ✅ Batch converts OpenGL ↔ DirectX normal maps  
- ✅ Recursively scans subfolders inside a given folder  
- ✅ Converts only relevant files (`normal` + `map` in filename)  
- ✅ Keeps the original files safe  
- ✅ Adds a suffix (`_DX` or `_GL`) to converted versions  
- ✅ Supports `.png`, `.jpg`, `.tga`, `.tif`, `.bmp`, `.webp`, etc.  

---

## 🧰 Requirements

You need **Python 3** installed on your computer.

### 🔹 Step 1 — Check if Python is installed

Open **Command Prompt** (Windows) or **Terminal** (macOS/Linux) and type:

python --version

If you get a version like Python 3.10 or higher, you’re good to go.

If not, download and install Python from the official website:
https://www.python.org/downloads/

Step 2 — Install the required libraries

Once Python is installed, open a Command Prompt and run this command:

python -m pip install pillow numpy

🚀 How to Use the Script
1. Download the file : convert_normals_inplace
2. Place it anywhere convenient eg : C:\Tools\convert_normals_inplace.py
3. Open Command Prompt in that same folder, or navigate to it:
4. Run one of the following commands:
   ➤ To Convert from OpenGL → DirectX
      python convert_normals_inplace.py "D:\Your\Top\Folder" --mode ogl2dx --suffix _DX
   ➤ To Convert from DirectX → OpenGL
   python convert_normals_inplace.py "D:\Your\Top\Folder" --mode dx2ogl --suffix _GL
   

   | Flag           | Description                                           |
| -------------- | ----------------------------------------------------- |
| `--suffix _DX` | Text added to converted file name                     |
| `--keep-ext`   | Keep original file extension instead of saving as PNG |


- Examples :
  
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
 │   ├─ rock_normal_map_DX.png   ← converted version
 ├─ walls\
 │   ├─ wall_normal_map.tga
 │   ├─ wall_normal_map_DX.png   ← converted version

🧠 Notes

The conversion only flips the Y (green) channel — that’s the only difference between OpenGL and DirectX normal maps.

The script is non-destructive — your originals are safe.

Works with high-res textures (tested up to 8K).

🧑‍💻 Author

Zakarya CHIOUA
3D Game Artist & Photogrammetry Specialist
CLOVER 

MIT License — free to use, modify, and share.
