# Setting working directory: TFG_EduardVergesFranch
import sys
sys.path.append('..')

from test_pipeline_tools.METRICS import *


import importlib 
import test_pipeline_tools.Segments_Loader as seg
importlib.reload(seg)

from test_pipeline_tools.Segments_Loader import song_2_anno, SEGMENTS_LOADER,ex_2_id
from test_pipeline_tools.Segments_Loader import SEGMENTS_LOADER, load_submissions, ExerciseAudioPathExtractor, create_AnnotatedBeatChromaEstimator
from Code.test_utils.training_individual_chord_model import NewModel

from pychord_tools.compositional_data import substitute_zeros, amalgamate, alrinv
from pychord_tools.plots import ternary_plot, plot_labels

from pychord_tools.third_party import NNLSChromaEstimator
from pychord_tools.low_level_features import  AnnotatedBeatChromaEstimator, AnnotatedChromaSegments
from simmusic.feature_extraction import AdaptiveChromaEstimator, GuitarLabelTranslator
from joblib import Memory
import time

from test_pipeline_tools.Visualization import CHORDS_NOTES_VISUALIZATION,visualize

from sklearn.metrics import confusion_matrix,accuracy_score,\
                            precision_recall_fscore_support

from test_pipeline_tools.METRICS import Overall_Metrics,Kind_Metrics,Individual_Metrics, accuracy_by_source

from test_pipeline_tools.Visualization import *

from matplotlib.pyplot import magnitude_spectrum
import essentia.standard as ess
