import sys
sys.path.append('/')
sys.path.append('./test_code/test_utils/')
from test_utils.training_individual_chord_model import NewModel, SimUidAndAudioPathExtractor, load_file_list

import os
import numpy as np
import json

from pychord_tools.low_level_features import  AnnotatedBeatChromaEstimator
from pychord_tools.third_party import NNLSChromaEstimator
from pychord_tools.low_level_features import AudioPathExtractor, UidExtractor

from simmusic.feature_extraction import AdaptiveChromaEstimator, GuitarLabelTranslator
from simmusic.latency import remove_latency

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

def load_submissions(chromaEstimator,path_extractor, exercise_id2annotations, submissions, segments,base_path):

    for s in submissions:
        print(s['path'])
        audio_file = os.path.join(base_path, s['path'])
        latency = s['latency']
        anno_file = exercise_id2annotations[s['exercise_id']]
        temp_audio = "q.wav"
        remove_latency(audio_file, temp_audio, latency)
        path_extractor.set(temp_audio, s['id'])
        print(audio_file)
        chunk = chromaEstimator.load_chromas_for_annotation_file(anno_file)
        segments.chromas = np.concatenate((segments.chromas, chunk.chromas))
        segments.labels = np.concatenate((segments.labels, chunk.labels))
        segments.pitches = np.concatenate((segments.pitches, chunk.pitches))
        segments.kinds = np.concatenate((segments.kinds, chunk.kinds))
        segments.uids = np.concatenate((segments.uids, chunk.uids))
        segments.start_times = np.concatenate((segments.start_times, chunk.start_times))
        segments.durations = np.concatenate((segments.durations, chunk.durations))

    return segments
