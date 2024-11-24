import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash

# Initialize the Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the folder only if it doesn't already exist
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB upload limit
app.secret_key = "your_secret_key"  # Replace with a secure key in production

# Allowed extensions for file uploads
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "zip", "mp4"}

def allowed_file(filename):
    """Check if the file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    """Render the homepage."""
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file uploads."""
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect("/")
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("File uploaded successfully")
        return redirect("/")
    else:
        flash("Invalid file type")
        return redirect("/")

@app.route("/download/<filename>")
def download_file(filename):
    """Allow file downloads."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    """Delete a file."""
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash("File deleted successfully")
    else:
        flash("File not found")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
