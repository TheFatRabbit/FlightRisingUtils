# used only when adding new images

import os
from PIL import Image

dirname = os.path.dirname(__file__)

ANCIENT_NAMES = (
    "Aberration",
    "Aether",
    "Auraboa",
    "Banescale",
    "Gaoler",
    "Sandsurge",
    "Undertide",
    "Veilspun"
)

for folder_path in os.listdir(os.path.join(dirname, "images")):
    if ".png" in folder_path:
        continue
    for subfolder_path in os.listdir(os.path.join(dirname, "images", folder_path)):
        for file_path in os.listdir(os.path.join(dirname, "images", folder_path, subfolder_path)):
            if ".ini" in file_path:
                continue
            if " (1)" in file_path:
                if os.path.isfile(os.path.join(dirname, "images", folder_path, subfolder_path, file_path.replace(" (1)", ""))):
                    os.remove(os.path.join(dirname, "images", folder_path, subfolder_path, file_path.replace(" (1)", "")))
                os.rename(os.path.join(dirname, "images", folder_path, subfolder_path, file_path), os.path.join(dirname, "images", folder_path, subfolder_path, file_path.replace(" (1)", "")))
            for anc_name in ANCIENT_NAMES:
                if anc_name in file_path:
                    os.rename(os.path.join(dirname, "images", folder_path, subfolder_path, file_path), os.path.join(dirname, "images", folder_path, subfolder_path, file_path.replace(f" ({anc_name})", "").replace(" Gene", f" {anc_name} Gene")))

for folder_path in os.listdir(os.path.join(dirname, "images")):
    if ".png" in folder_path:
        continue
    for subfolder_path in os.listdir(os.path.join(dirname, "images", folder_path)):
        for file_path in os.listdir(os.path.join(dirname, "images", folder_path, subfolder_path)):
            if ".ini" in file_path:
                os.remove(os.path.join(dirname, "images", folder_path, subfolder_path, file_path))
                continue
            image = Image.open(os.path.join(dirname, "images", folder_path, subfolder_path, file_path))
            if image.mode == "RGBA":
                new_image = Image.new("RGB", image.size, (255, 255, 255))
                new_image.paste(image, (0, 0), image)
                new_image.save(os.path.join(dirname, "images", folder_path, subfolder_path, file_path))
                image = Image.open(os.path.join(dirname, "images", folder_path, subfolder_path, file_path))
            if image.size != (56, 56):
                new_image = image.resize((56, 56))
                new_image.save(os.path.join(dirname, "images", folder_path, subfolder_path, file_path))
                image = Image.open(os.path.join(dirname, "images", folder_path, subfolder_path, file_path))