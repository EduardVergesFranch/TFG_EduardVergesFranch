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

store = '/home/eduard/Escritorio/TFG_EduardVergesFranch/test_code/test_utils/models/'
model_name = 'Baseline_Thirds' + '.pkl'

if __name__ == "__main__":
    pysim_chords_test_data_dir = '/home/eduard/Escritorio/pysimmusic-experiments/guitar_for_beginners/data'
    chromaEstimator = AnnotatedBeatChromaEstimator(
        chroma_estimator=NNLSChromaEstimator(),
        segment_chroma_estimator=AdaptiveChromaEstimator(),
        label_translator=GuitarLabelTranslator(),
        uid_extractor=SimUidAndAudioPathExtractor(pysim_chords_test_data_dir))

    ####################### RECORDINGS
    seva_rec = load_file_list(
        os.path.join(pysim_chords_test_data_dir, 'annotations/correct.txt'),
        pysim_chords_test_data_dir)

    ####################### TCL
    tcl_Rec = load_file_list('/home/eduard/Escritorio/TFG_EduardVergesFranch/test_data/TCL_annotation_paths.txt','')

    segments = chromaEstimator.load_chromas_for_annotation_file_list(seva_rec + tcl_Rec)
    print('Loaded TCL Stems and SEVA data')



    ######################## SUBMISSIONS
    exercise_id2annotations = {
        26: '/home/eduard/Escritorio/pysimmusic-experiments/guitar_for_beginners/data/exercises/Leah17Dec2018/Lesson01Ex1/l1ex1.json',
        20: '/home/eduard/Escritorio/pysimmusic-experiments/guitar_for_beginners/data/exercises/Leah17Dec2018/Lesson02Ex1/l2ex1.json',
        17: '/home/eduard/Escritorio/pysimmusic-experiments/guitar_for_beginners/data/exercises/Leah17Dec2018/Lesson02Ex2/l2ex2.json',
        16: '/home/eduard/Escritorio/pysimmusic-experiments/guitar_for_beginners/data/exercises/Leah17Dec2018/Lesson03Ex1/l3ex1.json',
        27: '/home/eduard/Escritorio/pysimmusic-experiments/guitar_for_beginners/data/exercises/Leah17Dec2018/Lesson04Ex1/l4ex1.json',
        25: '/home/eduard/Escritorio/pysimmusic-experiments/guitar_for_beginners/data/exercises/Leah17Dec2018/Lesson05Ex1/l5ex1.json'
    }

    with open("/home/eduard/Escritorio/pysimmusic-experiments/guitar_for_beginners/one_time_scripts/guitar_samples_annotation/chroma_pattern_dataset.json") as af:
        submissions = json.load(af)

    class ExerciseAudioPathExtractor(AudioPathExtractor, UidExtractor):
        def set(self, audio_path, uid_value):
            self.audio_path = audio_path
            self.uid_value = uid_value

        def audio_path_name(self, uid):
            return self.audio_path

        def uid(self, annotation_file_name):
            return self.uid_value

    path_extractor = ExerciseAudioPathExtractor()

    chromaEstimator = AnnotatedBeatChromaEstimator(
        chroma_estimator=NNLSChromaEstimator(audio_path_extractor=path_extractor),
        segment_chroma_estimator=AdaptiveChromaEstimator(),
        label_translator=GuitarLabelTranslator(),
        uid_extractor=path_extractor)

    base_path = "/home/eduard/Escritorio/pysimmusic-experiments/guitar_for_beginners/one_time_scripts/guitar_samples_annotation/"
    segments = load_submissions(chromaEstimator, path_extractor, exercise_id2annotations , submissions, segments, base_path)
    print('Loaded submissions')

    m = NewModel(
        {'maj': ['I', 'III', 'V'], 'min': ['I', 'IIIb', 'V'], '5': ['I', 'V'], '1': ['I', 'V', 'III'],
         '+3': ['I', 'III'], '-3': ['I','IIIb']},

        {'maj': {'n_components': 1, 'covariance_type': 'full', 'max_iter': 200},
         'min': {'n_components': 1, 'covariance_type': 'full', 'max_iter': 200},
         '5': {'n_components': 1, 'covariance_type': 'full', 'max_iter': 200},
         '1': {'n_components': 1, 'covariance_type': 'full', 'max_iter': 200},
         '+3': {'n_components': 1, 'covariance_type': 'full', 'max_iter': 200},
         '-3': {'n_components': 1, 'covariance_type': 'full', 'max_iter': 200}})

    m.fit(segments)
    m.save_model(store + model_name)
