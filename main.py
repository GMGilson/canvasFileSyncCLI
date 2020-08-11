from canvasapi import Canvas, exceptions
from os import environ
from dotenv import load_dotenv
from src.manifest import Client
# load_dotenv("./config/.env")

# API_KEY = environ.get("API_KEY")
# API_URL = environ.get("API_URL")

# client = Canvas(API_URL, API_KEY)
# courses = client.get_courses()

# for i in courses:
#     try:
#         print(f"{i.name}")
#         for file in i.get_files():
#             print(f"Downloading: {file} Last Modified: {file.modified_at}")
#             file.download(f'./temp/{file.filename}')
#     except exceptions.Unauthorized:
#         continue
#     except AttributeError:
#         continue

if __name__ == "__main__":
    client = Client()
    client.generateManifest()
