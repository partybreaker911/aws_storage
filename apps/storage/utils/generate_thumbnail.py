from PIL import Image


def generate_thumbnail(file_path, thumbnail_path):
    # Generate thumbnail from the file
    with Image.open(file_path) as image:
        image.thumbnail((100, 100))
        image.save(thumbnail_path)
