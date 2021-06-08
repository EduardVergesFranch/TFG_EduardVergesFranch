# Example, how an exercise could be assessed off-line (without music critic)
# More examples are in pysimmusic project:
# pysimmusic/demo/demo_guitar.py

import matplotlib.pyplot as plt
import numpy as np

from pychord_tools.models import load_model

import simmusic.extractors.guitar as guitar

from pychord_tools.third_party import NNLSChromaEstimator, nnls_chroma_from_audio
from pychord_tools.low_level_features import AnnotatedBeatChromaEstimator, AnnotatedChromaSegments, ChromaEstimator, AudioPathExtractor
from simmusic.feature_extraction import AdaptiveChromaEstimator, ConstUIDExtractor
from simmusic.chroma_labels import GuitarLabelTranslator

import sys
sys.path.append('./')
sys.path.append('./test_code/test_utils/')
sys.path.append('./test_code/test_utils/models/')

from test_utils.training_individual_chord_model import *

class MyNNLSChromaEstimator(ChromaEstimator):
    def __init__(self, audio_path_extractor=AudioPathExtractor(), hop_size=2048, sample_rate=44100):
        super().__init__(8192, hop_size, sample_rate, audio_path_extractor=audio_path_extractor)

    def estimate_chroma(self, uid):
        return nnls_chroma_from_audio(uid, self.audio_path_extractor, self.sample_rate, self.hop_size)

class MyAdaptiveChromaEstimator(AdaptiveChromaEstimator):
    def __init__(self, frame_size=16384, hop_size=2048, sample_rate=44100, smoothing_time=0.6):
        super().__init__(frame_size, hop_size, sample_rate, smoothing_time = smoothing_time)

    def fill(self, beats, durations, chroma, smoothed_chromas):
        for i in range(len(beats)):

            """s = int(float(beats[i]) *
                    self.sample_rate / self.hop_size)
            d = int(float(durations[i]) *
                    self.sample_rate / self.hop_size)
            d = min(d, len(chroma) - s)
            w = eval('np.hanning(2*d)') #Use a non-symetric window?
            shift = int(d - 0.15 * self.sample_rate / self.hop_size) #<---------------- 0 -> Provar un altre 0.15
            d = int(d - 0.15 * self.sample_rate / self.hop_size) # <----------------0
            w = w[shift:shift + d] / np.sum(w[shift:shift + d]) # <----------------0
            w = np.reshape(w, (1, d))
            c = chroma[s:s+d]
            smoothed_chromas[i] = np.dot(w,c)"""


            s = int(float(beats[i]) * self.sample_rate / self.hop_size)  # Set start
            d = int(float(durations[i]) * self.sample_rate / self.hop_size)  # Set duration
            if len(chroma) - s < d:
                d = int(len(chroma) - s)
            
            w = eval('np.hanning(2*d)')  # Construct window
            if (len(w) == 1) or (len(w) == 2):  # Force window being one for very short notes
                w = np.ones(len(w))
            w = w[d:]/ np.sum(w[d:])
            w = np.reshape(w, (1, d))
            
            c = chroma[s:s + d]
            
            smoothed_chromas[i] = np.dot(w, c)


def estimate_segment_scores(
        annotation_filename,
        student_filename,
        chroma_pattern_model,
        chroma_estimator=NNLSChromaEstimator()):
    """
    Estimates averaged segments chroma scores accoriding to given annotation.

    :param annotation_filename: annotation file
    :param student_filename: Name of the performance audio file of a student
    :param chroma_pattern_model: ChromaPatternModel
        model for estimating chords quality
    :param chroma_estimator: chorma estimator
    :return:
    """
    chromaEstimator = AnnotatedBeatChromaEstimator(
        chroma_estimator=chroma_estimator,
        segment_chroma_estimator=MyAdaptiveChromaEstimator(),
        label_translator=GuitarLabelTranslator(),
        uid_extractor=ConstUIDExtractor(student_filename),
        roll_to_c_root=False)

    realSegments = chromaEstimator.load_chromas_for_annotation_file(annotation_filename)
    # filter out unclassified:
    is_defined = [x != 'unclassified' for x in realSegments.kinds]
    realSegments = AnnotatedChromaSegments(
        realSegments.labels[is_defined],
        realSegments.pitches[is_defined],
        realSegments.kinds[is_defined],
        realSegments.chromas[is_defined],
        realSegments.uids[is_defined],
        realSegments.start_times[is_defined],
        realSegments.durations[is_defined])

    #predicted, plu = chromaPatternModel.predict(realSegments.chromas)
    nlu = chroma_pattern_model.log_utilities_given_sequence(
        chromas=realSegments.chromas, pitched_patterns=realSegments.pitched_patterns(), normalize=True)
    lu = chroma_pattern_model.log_utilities_given_sequence(
        chromas=realSegments.chromas, pitched_patterns=realSegments.pitched_patterns(), normalize=False)

    return lu, nlu, realSegments

def plot_chroma_scores(real_segments,predicted,save_path = None):
    plt.rcParams.update({'font.size': 10})
    type_of_notes_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # ------Plotting predictions obtained NNLS Chromas-------------------#
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)

    img = ax.imshow(real_segments.chromas.T,cmap='inferno',aspect='auto',interpolation='nearest')
    not_found_chromas = [ind for ind, chroma in enumerate(real_segments.chromas) if all(chroma == 0)] #Localize not found chromas
    for f in not_found_chromas:
        ax.axvline(x=f, color='r', linestyle='-', linewidth=2)

    cbar = fig.colorbar(img, ax=ax, shrink=0.1, orientation="vertical")
    cbar.set_label('Intensity')

    ax.set_xticks(range(len(predicted)))
    ax.set_yticks(range(12))

    x_label_list = []
    for i, (n, c) in enumerate(zip(predicted, real_segments.labels)):
        x_label_list.append(n.__repr__().replace(':','')+ '<--' + c.replace(':','').replace('(','').replace(')',''))

    ax.set_xticklabels(x_label_list)
    ax.set_yticklabels(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
    ax.set_xlabel("Predicted <-- GT note")
    ax.set_ylabel('Predicted probabilities')

    plt.xticks(rotation=-90)
    plt.grid(color='w', alpha=0.3, linestyle='-', linewidth=1)
    plt.title('Pysimmusic Predictions')
    if save_path:
        plt.savefig(save_path)
    #plt.show()

def all_chroma_scores(anno_file, audio_file, save_path):
    m = load_model( './MODELS/cross-validation/Baseline_Case/Baseline_Case.pkl')
    lu, nlu, real_segments = estimate_segment_scores(anno_file, audio_file, m)
    predicted, plu = m.predict(real_segments.chromas)
    plot_chroma_scores(real_segments,predicted, save_path)

    ##METRICS

    #print(predicted)
    return nlu

class GenericWorkflow(guitar.AssessmentWorkflow):
    def __init__(self,
                 tuning_estimator,
                 rhythm_estimator,
                 chroma_estimator,
                 overall_estimator,
                 tuning_feature_names,
                 timing_feature_names,
                 chroma_feature_names,
                 onset_series_delta=0.22,
                 path_chroma = None):
        super().__init__(
            tuning_estimator,
            rhythm_estimator,
            chroma_estimator,
            overall_estimator,
            tuning_feature_names,
            timing_feature_names,
            chroma_feature_names,
            onset_series_delta=onset_series_delta)
        self.save_chroma_path = path_chroma

    def chroma_scores(self, anno_file, audio_file):
        return all_chroma_scores(anno_file, audio_file, self.save_chroma_path)