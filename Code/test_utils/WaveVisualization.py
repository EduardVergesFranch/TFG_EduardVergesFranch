
import matplotlib.pyplot as plt
import numpy as np
from tmp_file_manager import TmpFileManager
from matplotlib.transforms import Bbox
import math
from common_utils import Stopwatch
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle, BoxStyle

class FeatureVisualizer:
    def __init__(self,
                 caption="",
                 right_hand_specific=False,
                 left_hand_specific=False):
        # height in staff_space units
        self.height_in_ss = 3
        self.caption = caption
        self.right_hand_specific = right_hand_specific
        self.left_hand_specific = left_hand_specific

    def draw(self, ax):
        pass

class DemoNoiseVisualiser(FeatureVisualizer):
    def __init__(self):
        super(DemoNoiseVisualiser, self).__init__()
        self.height_in_ss = 5

    def draw(self, ax):
        x = np.linspace(0, 1, 10000)
        y = np.random.rand(*(x.shape))
        ax.set_xlim(0,1)
        ax.plot(x,y)
