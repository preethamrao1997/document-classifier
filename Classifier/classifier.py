import os
import pickle
import shutil

from pdf2image import convert_from_path
from PIL import Image
from transformers import pipeline


def classify(image):  # Classify the image and return folder names
    pipe = pipeline("image-classification", model="./model")
    output = pipe(image)[0]["label"]

    with open("./model/remap.pickle", "rb") as handle:
        remap = pickle.load(handle)

    # Fixing folder names
    result = remap[output]
    result = result.title()

    return result


def delete_folder_contents(path):
    for root, dirs, files in os.walk(path):  # Delete tempdir contents
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def fix_documents(path):
    for root, directories, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            """for filename in os.listdir(path):  # Iterate over all files in the folder
            file_path = os.path.join(path, filename)"""

            if os.path.isfile(file_path):
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    image = Image.open(file_path).convert("RGB")
                    new_folder = os.path.join("./tempdir", classify(image))

                    if not os.path.exists(new_folder):  # If output folder doesn't exist
                        os.makedirs(new_folder)

                    dest_file = os.path.join(new_folder, filename)
                    shutil.copy2(file_path, dest_file)  # Copy file to new folder

                elif filename.lower().endswith(".pdf"):
                    pdf = convert_from_path(file_path)[0]
                    new_folder = os.path.join("./tempdir", classify(pdf))

                    if not os.path.exists(new_folder):  # If output folder doesn't exist
                        os.makedirs(new_folder)

                    dest_file = os.path.join(new_folder, filename)
                    shutil.copy2(file_path, dest_file)  # Copy file to new folder

    shutil.make_archive("./output/Fixed Documents", "zip", "./tempdir")

    delete_folder_contents("./tempdir")

    print("Files sorted and zipped up")


# fix_documents("./images")
