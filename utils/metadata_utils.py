from PIL import Image, ExifTags


def analyze_image_metadata(path):
    """Return common image properties and readable EXIF metadata."""
    with Image.open(path) as image:
        exif = image.getexif()
        decoded_exif = {}
        for key, value in exif.items():
            name = ExifTags.TAGS.get(key, str(key))
            try:
                decoded_exif[name] = str(value)
            except Exception:
                decoded_exif[name] = repr(value)

        return {
            "format": image.format,
            "mode": image.mode,
            "width": image.width,
            "height": image.height,
            "exif": decoded_exif,
        }
