from dotenv import load_dotenv
from google.cloud import storage
from pdf2image import convert_from_bytes
import io
import os
from dotenv import load_dotenv

# ------------------- Importing credentials --------------------#

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./file_name.json"

# ------------------- Function to convert pdf to images ----------------#


def pdf2images_cloudstorage(bucketName):
    storageClient = storage.Client()
    bucket = storageClient.get_bucket(bucketName)

    blobs = bucket.list_blobs(prefix='{Add path to folder containing files}')
    for blob in blobs:
        name = blob.name.split('/')
        if len(name) > 2 and blob.content_type == '{ mime_type_of_files }':
            fileName = name[-1]
            imageName = fileName[:-4]
            blobByte = blob.download_as_bytes()
            pages = convert_from_bytes(blobByte, 300)
            for num, page in enumerate(pages, start=1):

                # To store the images locally:
                page.save(f'./imgs/{imageName}-page{num}.jpg', 'JPEG')

                # To store the images in another bucket on cloud storage:
                resultBucket = storageClient.get_bucket(
                    '{bucket in which images to be stored}')
                resultBlob = resultBucket.blob(
                    f"path_to_specific_folder/{imageName}/{imageName}-page{num}.jpg")

                image_bytes = io.BytesIO()
                page.save(image_bytes, format='JPEG')
                resultBlob.upload_from_file(
                    image_bytes, content_type='image/jpeg')

    """
        Variables:
            prefix: path to the folder containing files.
            if complete path: bucketName/folder1/folder2, 
            then, prefix would be: folder1/folder2

            mime_type_of_files:
            for pdf: application/pdf
            for text: text/plain
    """


pdf2images_cloudstorage(bucketName="")
