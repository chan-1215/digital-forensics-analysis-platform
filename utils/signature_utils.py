FILE_SIGNATURES = [
    ("JPEG", b"\xff\xd8\xff"),
    ("PNG", b"\x89PNG\r\n\x1a\n"),
    ("GIF87a", b"GIF87a"),
    ("GIF89a", b"GIF89a"),
    ("ZIP", b"PK\x03\x04"),
    ("PDF", b"%PDF"),
    ("Windows Executable (MZ)", b"MZ"),
]


def detect_file_signature(path):
    """Identify common file types from their header signature."""
    with open(path, "rb") as f:
        header = f.read(32)

    matches = [name for name, sig in FILE_SIGNATURES if header.startswith(sig)]
    return {
        "header_hex": header.hex(" "),
        "matches": matches or ["Unknown"],
    }
