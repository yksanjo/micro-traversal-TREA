import os
import cv2
import numpy as np
from micro_traversal.vision import find_element_on_screen

def test_match_center():
    screen = np.zeros((100, 100), dtype=np.uint8)
    screen[40:60, 40:60] = 255
    template = np.zeros((20, 20), dtype=np.uint8)
    template[:, :] = 255
    cv2.imwrite("screen.png", screen)
    cv2.imwrite("template.png", template)
    pt = find_element_on_screen("screen.png", "template.png", 0.8)
    assert pt is not None
    os.remove("screen.png")
    os.remove("template.png")