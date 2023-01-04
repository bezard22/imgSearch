# imgSearch engine Module
import json
import numpy as np
import cv2
from os import listdir
from os.path import join
from tqdm import tqdm
import sys

# sys.tracebacklimit = 0

class Engine:
    """Search engine backend, performs relevant image scanning and searching.

    :raises Exception: _description_
    :return: _description_
    :rtype: _type_
    """    
    
    def __init__(self) -> None:
        """Engine Constructor

        :raises Exception: _description_
        """        
        configPath = r"imgSearch\config.json"
        with open(configPath) as configFile:
            self.config = json.load(configFile)
        with open(join(self.config["dataDir"], "data.json")) as dataFile:
            self.data = json.load(dataFile)
        
        self.detectors = []
        if self.config["detectors"]["ORB"]:
            self.detectors.append(cv2.ORB_create())
        if self.config["detectors"]["SIFT"]:
            self.detectors.append(cv2.SIFT_create())
        
        if self.config["distanceMetric"] == "NORM_HAMMING":
            self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=self.config["crossCheck"])
        else:
            raise Exception(f'invalid distanceMetric in config: {self.config["distanceMetric"]}')

    def update(self) -> None:
        """Update persistant data.
        """        
        with open(join(self.config["dataDir"], "data.json"), "w") as dataFile:
            json.dump(self.data, dataFile)

    def add(self, directory: str) -> None:
        """Add an image directory to the system and scan corresponding image files. Updates data accordingly.

        :param directory: path to directory to be added to system
        :type directory: str
        """        

        # check if direcyory already loaded
        if directory in self.data["directories"]:
            print(f'Directory: {directory} alredy loaded.')
        else:
            print(f"Adding directory: {directory}")
            self.data["directories"].append(directory)
            
            # scan directory for images
            filenames, features = self.scan(directory)

            # update data
            self.data["filenames"][directory] = filenames
            featureFileName = str(self.data["directories"].index(directory))
            np.save(join(self.config["dataDir"], featureFileName), features)
            self.data["featureFiles"][directory] = featureFileName + ".npy"
            self.update()

    def describe(self, img) -> list:
        """Extract relevant features from image.

        :param img: image to be described
        :type img: _type_
        :return: list of features describing image
        :rtype: list
        """        
        description = []
        for detector in self.detectors:
            _, des = detector.detectAndCompute(img, None)
            description.append(des)
        return description

    def scan(self, directory: str):
        """Scan given directoy and extract features from image files.

        :param directory: path to directory containing images to scan
        :type directory: str
        :return: tuple containing filenames and features corresponding to images
        :rtype: tuple
        """        

        filenames = []
        features = []
        print(f"Scanning Images from {directory}")
        for filename in tqdm(listdir(directory), ascii=' >='):
            filenames.append(filename)
            img = cv2.imread(join(directory, filename))
            features.append(self.describe(img))
        
        return filenames, np.array(features, dtype=object)

    def search(self, imgPath: str, directory: str) -> list:
        """Extract features from the given image and search against images in provided directory
        to find similar images.

        :param imgPath: path to image to search against
        :type imgPath: str
        :param directory: path to directory to search against
        :type directory: str
        :return: list of images from directed, sorted in order of similarity to given image
        :rtype: list
        """        
        # img = cv2.imread(imgPath)
        # des = self.describe(img)
        # comp = []
        # print("Searching for Similar Images")
        # for path, feature in tqdm(zip(self.paths, self.features), ascii=' >='):
        #     c = []
        #     for d, f in zip(des, feature):
        #         if d is None or f is None or len(d) == 0 or len(f) == 0:
        #             c.append(0)
        #         else:
        #             matches = eng.bf.match(np.uint8(d), np.uint8(f))
        #             c.append(sum([match.distance for match in matches]))
        #     comp.append([np.average(c), path])
        # return sorted(comp, key=lambda x: x[0], reverse=True)

    def info(self) -> None:
        """Print relevent info
        """        
        for directory in self.data["directories"]:
            print(directory)