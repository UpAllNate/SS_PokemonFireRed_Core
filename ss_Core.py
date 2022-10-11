import sys
import os
import imagehash
import numpy
from PIL import Image, ImageGrab
from PIL.Image import Image as ImageClass
from enum import Enum, auto as enumAuto
import winsound
from common.ss_Logging import logSS
from common.ss_PathClasses import PathElement, PathType, SSPath, Path
from common.ss_ColorClasses import *
from common.ss_PixelScanners import *
from common.ss_ProfileClasses import findAllProfiles, AudioPackData, ProfileInstance
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

    set = [True, True, True]
    print(f"Require sequence: {set[0]}, color: {set[1]}, audio: {set[2]}")
    allProfiles = findAllProfiles(set[0], set[1], set[2])
    print("Found: ", end="")
    if allProfiles:
        for p in allProfiles:
            print(p, end="")
    else:
        print("None", end="")
    print()
    print()

    set = [False, True, True]
    print(f"Require sequence: {set[0]}, color: {set[1]}, audio: {set[2]}")
    allProfiles = findAllProfiles(set[0], set[1], set[2])
    print("Found: ", end="")
    if allProfiles:
        for p in allProfiles:
            print(p, end="")
    else:
        print("None", end="")
    print()
    print()
        
    set = [True, False, True]
    print(f"Require sequence: {set[0]}, color: {set[1]}, audio: {set[2]}")
    allProfiles = findAllProfiles(set[0], set[1], set[2])
    print("Found: ", end="")
    if allProfiles:
        for p in allProfiles:
            print(p, end="")
    else:
        print("None", end="")
    print()
    print()
        
    set = [True, True, False]
    print(f"Require sequence: {set[0]}, color: {set[1]}, audio: {set[2]}")
    allProfiles = findAllProfiles(set[0], set[1], set[2])
    print("Found: ", end="")
    if allProfiles:
        for p in allProfiles:
            print(p, end="")
    else:
        print("None", end="")
    print()
    print()
        
    set = [True, False, False]
    print(f"Require sequence: {set[0]}, color: {set[1]}, audio: {set[2]}")
    allProfiles = findAllProfiles(set[0], set[1], set[2])
    print("Found: ", end="")
    if allProfiles:
        for p in allProfiles:
            print(p, end="")
    else:
        print("None", end="")
    print()
    print()
        
    set = [False, False, False]
    print(f"Require sequence: {set[0]}, color: {set[1]}, audio: {set[2]}")
    allProfiles = findAllProfiles(set[0], set[1], set[2])
    print("Found: ", end="")
    if allProfiles:
        for p in allProfiles:
            print(p, end="")
    else:
        print("None", end="")
    print()
    print()
            
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

