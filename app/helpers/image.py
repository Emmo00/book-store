from uuid import uuid4
import os
from os import path

from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image as PillowImage

from app.models import Image, LocationImage


def save_file(file, imageClass=Image):
    image = PillowImage.open(file)
    # Crop the center of the image
    crop_size = image.width if image.width < image.height else image.height
    left = (image.width - crop_size) // 2
    top = (image.height - crop_size) // 2
    right = (image.width + crop_size) // 2
    bottom = (image.height + crop_size) // 2
    # crop and resize
    cropped_img = image.crop((left, top, right, bottom)).resize((390, 390))
    webp_name = f"{str(uuid4())}.webp"
    cropped_img.save(
        f"{current_app.config['UPLOADS_FOLDER']}/{webp_name}", optimize=True
    )
    return imageClass(name=path.split(webp_name)[1])
