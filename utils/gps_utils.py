import exifread


def _ratio_to_float(value):
    return float(value.num) / float(value.den)


def _dms_to_decimal(values, ref):
    degrees = _ratio_to_float(values[0])
    minutes = _ratio_to_float(values[1])
    seconds = _ratio_to_float(values[2])
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ("S", "W"):
        decimal *= -1
    return decimal


def extract_gps(path):
    """Extract GPS coordinates from EXIF using exifread."""
    with open(path, "rb") as f:
        tags = exifread.process_file(f, details=False)

    lat = tags.get("GPS GPSLatitude")
    lat_ref = tags.get("GPS GPSLatitudeRef")
    lon = tags.get("GPS GPSLongitude")
    lon_ref = tags.get("GPS GPSLongitudeRef")

    if not all((lat, lat_ref, lon, lon_ref)):
        return {"found": False, "message": "GPS 정보가 없습니다."}

    latitude = _dms_to_decimal(lat.values, str(lat_ref))
    longitude = _dms_to_decimal(lon.values, str(lon_ref))

    return {
        "found": True,
        "latitude": round(latitude, 7),
        "longitude": round(longitude, 7),
    }
