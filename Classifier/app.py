import os
import shutil

from flask import Flask, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from classifier import delete_folder_contents, fix_documents

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/upload", methods=["POST"])
def upload_folder():
    input = request.files["file"]
    input.save(os.path.join("./input", secure_filename(input.filename)))  # Save zip
    shutil.unpack_archive("./input/folder.zip", "./input", "zip")
    os.remove("./input/folder.zip")  # Extract and delete it
    print("Received zip and extracted")

    fix_documents("./input")
    delete_folder_contents("./input")

    return send_file("./output/Fixed Documents.zip", as_attachment=True), 200


if __name__ == "__main__":
    app.run(port=5005)
