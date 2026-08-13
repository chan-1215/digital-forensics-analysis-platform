from pathlib import Path
from uuid import uuid4

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from utils.hash_utils import calculate_hashes
from utils.gps_utils import extract_gps
from utils.signature_utils import detect_file_signature
from utils.email_utils import analyze_eml
from utils.metadata_utils import analyze_image_metadata
from utils.carving_utils import find_embedded_signatures

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)


def save_uploaded_file(file_storage):
    """Save an uploaded file with a collision-resistant name."""
    original = secure_filename(file_storage.filename or "uploaded.bin")
    path = UPLOAD_FOLDER / f"{uuid4().hex}_{original}"
    file_storage.save(path)
    return path, original


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/hash", methods=["GET", "POST"])
def hash_analysis():
    result = None
    filename = None
    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            path, filename = save_uploaded_file(uploaded)
            result = calculate_hashes(path)
    return render_template("hash.html", result=result, filename=filename)


@app.route("/gps", methods=["GET", "POST"])
def gps_analysis():
    result = None
    filename = None
    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            path, filename = save_uploaded_file(uploaded)
            result = extract_gps(path)
    return render_template("gps.html", result=result, filename=filename)


@app.route("/signature", methods=["GET", "POST"])
def signature_analysis():
    result = None
    filename = None
    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            path, filename = save_uploaded_file(uploaded)
            result = detect_file_signature(path)
    return render_template("signature.html", result=result, filename=filename)


@app.route("/email", methods=["GET", "POST"])
def email_analysis():
    result = None
    filename = None
    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            path, filename = save_uploaded_file(uploaded)
            result = analyze_eml(path)
    return render_template("email.html", result=result, filename=filename)


@app.route("/metadata", methods=["GET", "POST"])
def metadata_analysis():
    result = None
    filename = None
    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            path, filename = save_uploaded_file(uploaded)
            result = analyze_image_metadata(path)
    return render_template("metadata.html", result=result, filename=filename)


@app.route("/carving", methods=["GET", "POST"])
def carving_analysis():
    result = None
    filename = None
    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            path, filename = save_uploaded_file(uploaded)
            result = find_embedded_signatures(path)
    return render_template("carving.html", result=result, filename=filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
