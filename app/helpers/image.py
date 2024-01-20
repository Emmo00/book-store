from uuid import uuid4
import os
from os import path

from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image as PillowImage

from app.models import Image, LocationImage


def save_file(file, imageClass=Image):
    file_name = f"{str(uuid4())}{path.splitext(secure_filename(file.filename))[1]}"
    file_save_path = f"{current_app.config['UPLOADS_FOLDER']}/{file_name}"
    file.save(file_save_path)
    image = PillowImage.open(file_save_path)
    # Crop the center of the image
    crop_size = image.width if image.width < image.height else image.height
    left = (image.width - crop_size) // 2
    top = (image.height - crop_size) // 2
    right = (image.width + crop_size) // 2
    bottom = (image.height + crop_size) // 2
    # crop and resize
    cropped_img = image.crop((left, top, right, bottom)).resize((390, 390))
    webp_name = f"{path.splitext(file_save_path)[0]}.webp"
    cropped_img.save(webp_name, optimize=True)
    try:
        os.remove(file_save_path)
    except:
        print("could not remove", file_save_path)
    return imageClass(name=path.split(webp_name)[1])
