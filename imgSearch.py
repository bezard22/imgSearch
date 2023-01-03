import numpy as np
import cv2
from os import listdir
from os.path import join
from tqdm import tqdm
import random

import seaborn_image as isns
import matplotlib.pyplot as plt


class Engine:
    def __init__(self, dir) -> None:
        print(f"Directory: {dir}")
        self.dir = dir
        self.detectors = [
            cv2.ORB_create(),
            cv2.SIFT_create(),
        ]
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.paths, self.features = self.scan()

    def describe(self, img):
        description = []
        for detector in self.detectors:
            _, des = detector.detectAndCompute(img, None)
            description.append(des)
        return description

    def scan(self):
        paths = []
        features = []
        print("Scanning Images")
        for imgFile in tqdm(listdir(self.dir)):
        # for imgFile in listdir(self.dir):
            paths.append(imgFile)
            img = cv2.imread(join(self.dir, imgFile))
            features.append(self.describe(img))
        return paths, features

    def search(self, path):
        img = cv2.imread(path)
        des = self.describe(img)
        # print(des)
        comp = []
        print("Searching for Similar Images")
        # for path, feature in zip(self.features, self.paths):
        for path, feature in tqdm(zip(self.paths, self.features)):
            c = []
            for d, f in zip(des, feature):
                if d is None or f is None or len(d) == 0 or len(f) == 0:
                    c.append(0)
                else:
                    matches = eng.bf.match(np.uint8(d), np.uint8(f))
                    c.append(sum([match.distance for match in matches]))
            comp.append([np.average(c), path])
        return sorted(comp, key=lambda x: x[0], reverse=True)
        


if __name__ == "__main__":
    # path = r"C:\Users\bwez1\Documents\Main\Data\Image\MNIST\test"
    path = r"C:\Users\bwez1\Documents\Main\Repos\imgSearch\test"
    eng = Engine(path)

    test = join(path, random.sample([p for p in listdir(path)], 1)[0])
    comp = eng.search(test)
    print(test)
    for c in comp[:10]:
        print(c)
    