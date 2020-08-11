# Builtins
from os import environ
import json

# Externs
from canvasapi import Canvas, exceptions
from dotenv import load_dotenv
from 

load_dotenv("./config/.env")

API_KEY = environ.get("API_KEY")
API_URL = environ.get("API_URL")


class Client:
    def __init__(self):
        """
        Wrapper for Canvas client object
        """
        self.client = Canvas(API_URL, API_KEY)

    def generateManifest(self, jsonDump: str = None) -> dict:
        """
        Serialize a dictionary manifest of courses and files contained
        in the course

        Args:
            jsonDump: filename to output manifest to

        Return:
            manifest of courses and files within the course

        """
        courses = self.client.get_courses()
        manifest = dict()
        for course in courses:
            try:
                files = list()
                for filePacket in course.get_files():
                    file = {
                        "fileId": filePacket.id,
                        "fileName": filePacket.filename,
                        "timestamp": filePacket.modified_at
                    }
                    files.append(file)

                manifest[course.name] = {
                    "courseId": course.id,
                    "files": files
                }

            except exceptions.Unauthorized:
                continue

        if jsonDump is not None:
            with open(jsonDump, 'w') as manifestFile:
                json.dump(manifest, manifestFile, indent=2)

        return manifest

    def loadManifest(self, manifestFile: str) -> dict:
        return json.load(manifestFile)

    def diffManifest(self):
        pass
