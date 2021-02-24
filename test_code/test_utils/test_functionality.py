# Example, how an exercise could be assessed off-line (without music critic)
# More examples are in pysimmusic project:
# pysimmusic/demo/demo_guitar.py

import matplotlib.pyplot as plt
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
from simmusic.feature_extraction import AdaptiveChromaEstimator, ConstUIDExtractor
from simmusic.chroma_labels import GuitarLabelTranslator

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
            s = int(float(beats[i]) *
                    self.sample_rate / self.hop_size)
            d = int(float(durations[i]) *
                    self.sample_rate / self.hop_size)
            d = min(d, len(chroma) - s)
            w = eval('np.hanning(2*d)')
            shift = int(d - 0.15 * self.sample_rate / self.hop_size)
            d = int(d - 0.15 * self.sample_rate / self.hop_size)
            w = w[shift:shift + d] / np.sum(w[shift:shift + d])
            w = np.reshape(w, (1, d))
            c = chroma[s:s+d]
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

def plot_chroma_scores(real_segments,predicted):
    type_of_notes_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # ------Plotting predictions obtained NNLS Chromas-------------------#
    fig = plt.figure(figsize=(15,1))
    ax = fig.add_subplot(111)
    img = ax.imshow(real_segments.chromas.T,cmap='inferno',aspect='auto',interpolation='nearest')
    cbar = fig.colorbar(img, ax=ax, shrink=0.3, orientation="horizontal")
    cbar.set_label('Probability')
    ax.set_xticks(range(len(predicted)))
    ax.set_yticks(range(12))

    x_label_list = []
    for n, c in zip(predicted, real_segments.labels):
        stri = n.__repr__()[0] .replace(':','') + ' '+ c.replace(':','').replace('(','').replace(')','')
        x_label_list.append(stri)
    plt.xticks(rotation=-90)
    #ax.tick_params(axis='x', which='both', length=0)
    #x_label_list = [n.__repr__()[0]  for n,c in zip(predicted,real_segments.chromas)]
    y_label_list = [n for n in type_of_notes_list]

    ax.set_xticklabels(x_label_list)
    ax.set_yticklabels(y_label_list)
    ax.set_xlabel("Predicted note\nGT note")
    ax.set_ylabel('Predicted probabilities')

    plt.grid()
    plt.title('Pysimmusic Predictions')
    plt.show()

def all_chroma_scores(anno_file, audio_file):
    m = load_model('/home/eduard/Escritorio/TFG_EduardVergesFranch/test_code/test_utils/models/new_model.pkl')
    lu, nlu, real_segments = estimate_segment_scores(anno_file, audio_file, m)
    predicted, plu = m.predict(real_segments.chromas)
    plot_chroma_scores(real_segments,predicted)
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
                 onset_series_delta=0.22):
        super().__init__(
            tuning_estimator,
            rhythm_estimator,
            chroma_estimator,
            overall_estimator,
            tuning_feature_names,
            timing_feature_names,
            chroma_feature_names,
            onset_series_delta=onset_series_delta)

    def chroma_scores(self, anno_file, audio_file):
        return all_chroma_scores(anno_file, audio_file)