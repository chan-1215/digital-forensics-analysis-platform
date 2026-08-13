CARVING_SIGNATURES = {
    "JPEG": b"\xff\xd8\xff",
    "PNG": b"\x89PNG\r\n\x1a\n",
    "GIF87a": b"GIF87a",
    "GIF89a": b"GIF89a",
    "ZIP": b"PK\x03\x04",
}


def _find_all(data, signature):
    offsets = []
    start = 0
    while True:
        index = data.find(signature, start)
        if index == -1:
            break
        offsets.append(index)
        start = index + 1
    return offsets


def find_embedded_signatures(path):
    """Locate common embedded file signatures and return their byte offsets."""
    with open(path, "rb") as f:
        data = f.read()

    results = []
    for name, signature in CARVING_SIGNATURES.items():
        for offset in _find_all(data, signature):
            results.append({"type": name, "offset": offset})

    return sorted(results, key=lambda item: item["offset"])
