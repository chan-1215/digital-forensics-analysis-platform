import hashlib


def calculate_hashes(path):
    """Calculate MD5, SHA-1 and SHA-256 for a file."""
    algorithms = {
        "MD5": hashlib.md5(),
        "SHA1": hashlib.sha1(),
        "SHA256": hashlib.sha256(),
    }

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            for hasher in algorithms.values():
                hasher.update(chunk)

    return {name: hasher.hexdigest() for name, hasher in algorithms.items()}
