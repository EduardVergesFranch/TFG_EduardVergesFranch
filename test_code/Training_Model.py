import sys
sys.path.append('../')
sys.path.append('./test_utils/')
sys.path.append('./test_utils/models/')

from pychord_tools.low_level_features import  AnnotatedBeatChromaEstimator
from pychord_tools.third_party import NNLSChromaEstimator
from simmusic.feature_extraction import AdaptiveChromaEstimator, GuitarLabelTranslator

from training_individual_chord_model import NewModel,SimUidAndAudioPathExtractor
import joblib
import numpy as np

def append_to_segments(segments, chunk):
    segments.chromas = np.concatenate((segments.chromas, chunk.chromas))
    segments.labels = np.concatenate((segments.labels, chunk.labels))
    segments.pitches = np.concatenate((segments.pitches, chunk.pitches))
    segments.kinds = np.concatenate((segments.kinds, chunk.kinds))
    segments.uids = np.concatenate((segments.uids, chunk.uids))
    segments.start_times = np.concatenate((segments.start_times, chunk.start_times))
    segments.durations = np.concatenate((segments.durations, chunk.durations))
    return segments

def load_segments_for_trainning(annotations):
    chromaEstimator = AnnotatedBeatChromaEstimator(
        chroma_estimator=NNLSChromaEstimator(),
        segment_chroma_estimator=AdaptiveChromaEstimator(),
        #    segment_chroma_estimator=SmoothedStartingBeatChromaEstimator(0.6),
        label_translator=GuitarLabelTranslator(),
        uid_extractor=SimUidAndAudioPathExtractor('/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/'))

    for i, ann in enumerate(annotations):
        if i == 0:
            segments = chromaEstimator.load_chromas_for_annotation_file(ann)
        else:
            chunk = chromaEstimator.load_chromas_for_annotation_file(ann)
            segments = append_to_segments(segments, chunk)
    return segments

#model = '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_code/test_utils/models/Baseline.pkl'
#m = joblib.load(open(model, 'rb'))

store = '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_code/test_utils/models/'
annotations = ['/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/Lily Was Here/Lily Was Here.json',
              '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/Hole In My Shoe/Hole In My Shoe.json',
              '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/20th Century Boy/20th Century Boy.json',
              '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/Where Did You Sleep Last Night/Where Did You Sleep Last Night.json',
              '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/Runaway Train/Runaway Train.json']


segments = load_segments_for_trainning(annotations)

m = NewModel(
        {'maj':['I', 'III', 'V'], 'min':['I', 'IIIb', 'V'], '5':['I', 'V'], '1':['I', 'V', 'III']},
        {'maj':{'n_components':1, 'covariance_type':'full', 'max_iter':200},
         'min':{'n_components':1, 'covariance_type':'full', 'max_iter':200},
         '5':{'n_components':1, 'covariance_type':'full', 'max_iter':200},
         '1':{'n_components':1, 'covariance_type':'full', 'max_iter':200}})

m.fit(segments)
#m.save_model(store + 'OverfitedModel.pkl')