import os

dirname = os.path.dirname(__file__)

for i, file in enumerate(os.listdir(os.path.join(dirname, "captchas"))):
    os.rename(os.path.join(dirname, "captchas", file), os.path.join(dirname, "captchas", str(i)))

for i, file in enumerate(os.listdir(os.path.join(dirname, "captchas"))):
    os.rename(os.path.join(dirname, "captchas", file), os.path.join(dirname, "captchas", f"captcha{i}.png"))