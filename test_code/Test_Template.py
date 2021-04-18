import numpy as np
import os
from pychord_tools.models import load_model
import simmusic
import simmusic.feature_extraction as feature_extraction
import simmusic.extractors.guitar as guitar
from PIL import Image
import io
from pychord_tools.third_party import NNLSChromaEstimator, nnls_chroma_from_audio
from pychord_tools.low_level_features import AnnotatedBeatChromaEstimator, AnnotatedChromaSegments, ChromaEstimator, AudioPathExtractor
import sys
sys.path.append('../')
sys.path.append('./test_utils/')
sys.path.append('./test_utils/models/')
from test_utils.training_individual_chord_model import *

from test_utils.test_functionality import GenericWorkflow

from simmusic.feature_extraction import AdaptiveChromaEstimator, ConstUIDExtractor
from simmusic.chroma_labels import GuitarLabelTranslator
import sys

if __name__ == "__main__":
    sys.path.append('/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data')

    assessment_workflow = load_model(os.path.join(simmusic.__path__[0], 'extractors/guitar_models/picking_workflow.pkl'))
    hacked_workflow = GenericWorkflow(
        assessment_workflow.tuning_estimator,
        assessment_workflow.rhythm_estimator,
        assessment_workflow.chroma_estimator,
        assessment_workflow.overall_estimator,
        assessment_workflow.tuning_feature_names,
        assessment_workflow.timing_feature_names,
        assessment_workflow.chroma_feature_names,
        onset_series_delta=0.22)


    json = '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/Hole In My Shoe/Hole In My Shoe.json'
    lily = '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/Hole In My Shoe/Hole In My Shoe.ly'
    target_audio = '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/Hole In My Shoe/3_gtrX_Hole In My Shoe_Traffic_Gtr Gr0.wav'

    results = guitar.assess_guitar_exercise(json, lily, 0.0, target_audio, assessment_workflow= hacked_workflow,image_format='pdf')


    with open("/home/eduard/Escritorio/TFG_EduardVergesFranch/test_code/test_utils/Results_Training/Hole In My Shoe1.pdf", "wb") as out_file:
        out_file.write(results["ImageBytes"])
    print('Overall:', results['Overall'])
    print('Rhythm:', results['Rhythm'])
    print('Tuning:', results['Tuning'])
    print('Pitch:', results['Pitch'])
    os.system('open -a "Adobe Acrobat Reader DC.app" //home/eduard/Escritorio/TFG_EduardVergesFranch/test_code/test_utils/Results_Training/Hole In My Shoe1.pdf')
