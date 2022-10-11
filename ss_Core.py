import sys
import os
import imagehash
import numpy
from PIL import Image, ImageGrab
from PIL.Image import Image as ImageClass
from enum import Enum, auto as enumAuto
import winsound
from common.ss_Logging import logSS
from common.ss_PathClasses import PathType, SSPath, PathElement
from common.ss_ColorClasses import *
from common.ss_PixelScanners import *
from typing import Any
import tomli
import time

def getDVal(d : dict, listPath : list) -> Any:
    for key in listPath:
        d = d[key]
    return d

def testColors():

    c = [
        ColorScanInstance(color=(237, 28, 36),tolerance=0,pure=ColorPure.required), # Red
        ColorScanInstance(color=(34, 177, 76),tolerance=0,pure=ColorPure.required), # Green
        ColorScanInstance(color=(0, 162, 232),tolerance=0,pure=ColorPure.required) # Green
    ]

    for i in range(1, 8):
        with Image.open('./tests/testColors_' + str(i) + '.png', mode='r') as im:
            px = getPixelRow_Pixel(im=im, row=im.height/2)
            # print(px)
            print("\n\n\n")

            logSS.info(f"Tests for image {i}, total width: {len(px)}")

            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 0, 0
            c[0].pure, c[1].pure, c[2].pure = ColorPure.required, ColorPure.required, ColorPure.required
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Zero tolerance test... Success: {result}")
            for color in colors:
                logSS.info(color)


            c[0].tolerance, c[1].tolerance, c[2].tolerance = 3, 120, 3
            c[0].pure, c[1].pure, c[2].pure = ColorPure.required, ColorPure.required, ColorPure.required
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Adequate tolerance test... Success: {result}")
            for color in colors:
                logSS.info(color)


            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 0, 0
            c[0].pure, c[1].pure, c[2].pure = ColorPure.notRequired, ColorPure.notRequired, ColorPure.notRequired
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Non-required test... Success: {result}")
            for color in colors:
                logSS.info(color)

            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 150, 0
            c[0].pure, c[1].pure, c[2].pure = ColorPure.required, ColorPure.notRequired, ColorPure.required
            result, colors = pixelSequenceScan(pixels=px, colors=c)
            logSS.info(f"Required Red/Blue, Toleranced/NonRequired Green... Success: {result}")
            for color in colors:
                logSS.info(color)

class SSProfileInstance:
    def __init__(self : str, n, v : str, p : str) -> None:
        self.name = n
        self.version = v
        self.path = p
    
    def __str__(self) -> str:
        return f"{self.name}, v{self.version}"

def findAllProfiles() -> list[SSProfileInstance]:
    """
    Scan for all available profiles
    """
    allProfilePaths = [ f.path for f in os.scandir(SSPath.profiles.path) if f.is_dir()]

    validProfilePaths = []
    for profilePath in allProfilePaths:
        try:
            runPath = os.path.join(profilePath,'run.toml')
            with open(runPath, 'rb') as f:
                a = tomli.load(f)
                profileName = a["name"]
                profileVersion = a["version"]
        except KeyError as e:
            logSS.warning(f"Invalid profile detected: {profilePath}, missing attribute {e}")
            continue
        except FileNotFoundError as e:
            logSS.warning(f"Invalid profile detected: {profilePath}, missing run file {e}")
            continue
        except tomli.TOMLDecodeError as e:
            logSS.warning(f"Invalid profile detected: {profilePath}, cannot decode run.tomli... corrupted file: {e}")
            continue
        except Exception as e:
            raise e
        
        audioPath = PathElement(PathType.directory, os.path.join(profilePath, "Audio Packs"))
        if not audioPath.detect():
            logSS.warning(f"Invalid profile detected: {profilePath}, does not have Audio Packs folder")
            continue

        validProfilePaths.append(SSProfileInstance(profileName, profileVersion,profilePath))

    return validProfilePaths

class AudioPackData:
    def __init__(self, title : str, authors : list[str] , hashPath, packPath : str) -> None:
        self.title = title
        self.authors = authors
        self.path = packPath
    
    def __str__(self):
        msg = f"AudioPack: {self.title}, Authors: "
        for i, a in enumerate(self.authors):
            msg += f"{a}"
            if i < len(self.authors) - 1:
                msg += ", "
        msg += "\n"
        return msg

def findAllAudioPacks(prof : SSProfileInstance) -> list[AudioPackData]:
    allValidAudioPacks : AudioPackData = []



    # Scan the AudioPack directory for all installed packs
    allAudioPacks = [ a.path for a in os.scandir(prof.path) if a.is_dir()]

    # Compile only those directories with an Audio Pack Description file that contains a title and hash table
    for packDir in allAudioPacks:

        print(f"AudioPack Directory: {packDir}")

        # Audio Pack Description
        file = Path(os.path.join(packDir,'AudioPackDescription.toml'))

        print(f"AudioPack Description file: {file}")

        if not file.is_file():
            print("Description does not exist")
            continue

        names = []
        with open(file, mode='r') as file_csv:
            # Create csv reader object of hashtable csv
            reader_obj = csv.reader(file_csv)

            
            names.append(n)
            print(f"Appended name: {n}")

        file = os.path.join(packDir,'hashTable.csv')

        if not pathFunction(file).is_file():
            print("hashTable.csv is not a file")
            break
        if not checkHashTable(file):
            print("hashTable.csv check failure")
            break

        allValidAudioPacks.append(AudioPackData(title, names, file, packDir))



# Returns valid selection
def chooseFromList(prompt : str, l : list) -> int:
    choosing = True
    selectionMenu = prompt + "\n\n"

    while choosing:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        for i, p in enumerate(l):
            selectionMenu += f"[{i}] : {str(p)}\n"

        selectionMenu += "\nPlease enter the selection number: "

        try:
            selection = int(input(selectionMenu))
        except KeyboardInterrupt:
            exit()
        except:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("That is not a number.")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            if selection < 0 or selection >= len(l):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("That is not a valid selection")
                time.sleep(2)
            else:
                choosing = False

if __name__ == "__main__":

    allProfiles = findAllProfiles()
    exit()
    selectedProfileIndex = chooseFromList("Please choose from the following profiles:", allProfiles)

    while True:
        # Screenshot is a PIL Image class PNG of (r,g,b,alpha)
        screenShot_Whole_Image = ImageGrab.grab()
        screenShot_Whole_npArray = numpy.array(screenShot_Whole_Image).tolist()
    
        # for _seq in run["sequence"]:
        # seq = run["sequence"][_seq]

        # print(f"\nRunning sequence {seq['name']}\n\n")

        # for step in range(1,len(seq)+1):
        #     stepStr = str(step)

        #     if seq[stepStr]["function"] == "getNumbers":
        #         seq[stepStr]["result"] = getNumbers()

