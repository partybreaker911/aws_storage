from apps.storage.utils.generate_thumbnail import generate_thumbnail

from PyPDF2 import PdfFileReader
from PIL import Image


class ThumbnailGenerator:
    @staticmethod
    def generate_thumbnail(file_path, thumbnail_path):
        # Default method for generating thumbnails
        # You can customize this method to handle generic cases

        generate_thumbnail(file_path, thumbnail_path)

    @classmethod
    def generate(cls, file_path, thumbnail_path):
        file_extension = file_path.split(".")[-1].lower()

        if hasattr(cls, file_extension):
            getattr(cls, file_extension)(file_path, thumbnail_path)
        else:
            cls.generate_thumbnail(file_path, thumbnail_path)


class PNGThumbnailGenerator(ThumbnailGenerator):
    @staticmethod
    def png(file_path, thumbnail_path):
        # Generate thumbnail for PNG file
        with Image.open(file_path) as image:
            image.thumbnail((100, 100))
            image.save(thumbnail_path)


class PDFThumbnailGenerator(ThumbnailGenerator):
    @staticmethod
    def pdf(file_path, thumbnail_path):
        # Generate thumbnail for PDF file
        with open(file_path, "rb") as file:
            pdf = PdfFileReader(file)
            first_page = pdf.getPage(0)
            scale_factor = 0.5
            page_width = int(first_page.mediaBox.getWidth() * scale_factor)
            page_height = int(first_page.mediaBox.getHeight() * scale_factor)
            image = first_page.get_thumbnail((page_width, page_height))
            image.save(thumbnail_path)
