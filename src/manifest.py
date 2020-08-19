# Builtins
from os import environ
from typing import Set
from pprint import pprint
import json

# Externs
from canvasapi import Canvas, exceptions
from dotenv import load_dotenv


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
                        "fileId": str(filePacket.id),
                        "fileName": filePacket.filename,
                        "timestamp": filePacket.modified_at
                    }
                    files.append(file)

                manifest[str(course.id)] = {
                    "courseName": course.name,
                    "files": files
                }

            except exceptions.Unauthorized:
                continue

        if jsonDump is not None:
            with open(jsonDump, 'w') as manifestFile:
                json.dump(manifest, manifestFile, indent=2)

        return manifest

    def loadManifest(self, manifestFile: str) -> dict:
        with open(manifestFile) as file:
            return json.load(file)

    def diffManifest(self):
        oldManifest = self.loadManifest("config/manifest.json")
        newManifest = self.generateManifest()

        # contains API path to files to be downloaded
        # {courseID: [fileIds]}
        fileUpdates = dict()

        # contains a set of filepaths marked for deletion
        fileRemovals = set()

        self.resolveCourseDifference(fileUpdates, fileRemovals, oldManifest, newManifest)
        self.resolveFileUpdates()

    def resolveCourseDifference(self,
                                fileUpdates: dict,
                                fileRemovals: Set[str],
                                oldManifest: dict,
                                newManifest: dict
                                ):

        oldManifestCourses = oldManifest.keys()
        newManifestCourses = newManifest.keys()

        # User has dropped or removed courses to be tracked
        for courseId in oldManifestCourses - newManifestCourses:
            for file in oldManifest[courseId]["files"]:
                filePath = f'{oldManifest[courseId]["courseName"]}/{file["fileName"]}'
                fileRemovals.add(filePath)

        # User has added new courses
        for courseId in newManifestCourses - oldManifestCourses:
            fileUpdates[courseId] = [file["fileId"] for file in newManifest[courseId]["files"]]

    def resolveFileUpdates(fileUpdates: dict, oldManifest: dict, newManifest: dict):
        pass
