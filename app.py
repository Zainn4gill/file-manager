import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure the upload folder exists
upload_folder = "static/uploads"
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# Set configuration for uploading
app.config["UPLOAD_FOLDER"] = upload_folder
app.config["ALLOWED_EXTENSIONS"] = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "zip"}  # Added zip

# Function to check allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# Home route that shows uploaded files
@app.route("/")
def home():
    try:
        files = os.listdir(app.config["UPLOAD_FOLDER"])
    except FileNotFoundError:
        files = []
    return render_template("index.html", files=files)

# Upload file route
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            return redirect("/")
        except Exception as e:
            app.logger.error(f"Error saving file: {e}")
            return f"An error occurred: {e}", 500
    else:
        return "File not allowed", 400

if __name__ == "__main__":
    app.run(debug=True)
