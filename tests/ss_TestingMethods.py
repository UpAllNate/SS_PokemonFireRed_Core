
from PIL import Image
from src.ss_logging.spoken_screen_logger import (
    ProjectLogger,
    standard_stream_format_string,
    DEBUG
)
from src.ss_ColorClasses import *
from src.ss_Pixel import *
from pathlib import Path

test_logger = ProjectLogger(
    stream_log_enable= True,
    stream_logger_name= "test",
    stream_log_level= DEBUG,
    stream_log_format_string= standard_stream_format_string
)

def testColors():

    c : list[PixelColor] = [
        PixelColor(color=(237, 28, 36),tolerance=0,requirement=True), # Red
        PixelColor(color=(34, 177, 76),tolerance=0,requirement=True), # Green
        PixelColor(color=(0, 162, 232),tolerance=0,requirement=True) # Green
    ]
 
    for i in range(1, 8):
        with Image.open('./tests/testColors_' + str(i) + '.png', mode='r') as im:
            px = get_pixel_row_absolute(im=im, row=im.height/2)
            # print(px)
            print("\n\n\n")

            test_logger.info(f"Tests for image {i}, total width: {len(px)}")

            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 0, 0
            c[0].requirement, c[1].requirement, c[2].requirement = True, True, True
            result, colors = pixel_sequence_scan(pixels=px, colors=c)
            test_logger.info(f"Zero tolerance test... Success: {result}")
            for color in colors:
                test_logger.info(color)


            c[0].tolerance, c[1].tolerance, c[2].tolerance = 3, 120, 3
            c[0].requirement, c[1].requirement, c[2].requirement = True, True, True
            result, colors = pixel_sequence_scan(pixels=px, colors=c)
            test_logger.info(f"Adequate tolerance test... Success: {result}")
            for color in colors:
                test_logger.info(color)

            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 0, 0
            c[0].requirement, c[1].requirement, c[2].requirement = False, False, False
            result, colors = pixel_sequence_scan(pixels=px, colors=c)
            test_logger.info(f"Non-required test... Success: {result}")
            for color in colors:
                test_logger.info(color)

            c[0].tolerance, c[1].tolerance, c[2].tolerance = 0, 150, 0
            c[0].requirement, c[1].requirement, c[2].requirement = True, False, True
            result, colors = pixel_sequence_scan(pixels=px, colors=c)
            test_logger.info(f"Required Red/Blue, Toleranced/NonRequired Green... Success: {result}")
            for color in colors:
                test_logger.info(color)