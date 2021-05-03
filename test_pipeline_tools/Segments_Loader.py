# Load segments from audio and annotaion files

from test_code.test_utils.training_individual_chord_model import NewModel, SimUidAndAudioPathExtractor, load_file_list

import os
import numpy as np
import json

from pychord_tools.low_level_features import  AnnotatedBeatChromaEstimator, AnnotatedChromaSegments
from pychord_tools.third_party import NNLSChromaEstimator
from pychord_tools.low_level_features import AudioPathExtractor, UidExtractor

from simmusic.feature_extraction import AdaptiveChromaEstimator, GuitarLabelTranslator
from simmusic.latency import remove_latency


class ExerciseAudioPathExtractor(AudioPathExtractor, UidExtractor):
    def set(self, audio_path, uid_value):
        self.audio_path = audio_path
        self.uid_value = uid_value

    def audio_path_name(self, uid):
        return self.audio_path

    def uid(self, annotation_file_name):
        return self.uid_value

class SEGMENTS_LOADER():
    def __init__(self, base_path):
        self.base_path = base_path
    def load_annotation_list(self, list):

        return load_file_list(list, self.base_path)

    def load_chromas_annotation_list(self, list):

        list = self.load_annotation_list(os.path.join(self.base_path,list))
        chromaEstimator = AnnotatedBeatChromaEstimator(
            chroma_estimator=NNLSChromaEstimator(),
            segment_chroma_estimator=AdaptiveChromaEstimator(),
            label_translator=GuitarLabelTranslator(),
            uid_extractor=SimUidAndAudioPathExtractor(self.base_path))
        return chromaEstimator.load_chromas_for_annotation_file_list(list)

    def create_segments_variable(self):
        segments = AnnotatedChromaSegments(
            labels=np.array([], dtype='object'),
            pitches=np.array([], dtype='int'),
            kinds=np.array([], dtype='object'),
            chromas=np.zeros((0, 12), dtype='float32'),
            uids=np.array([], dtype='object'),
            start_times=np.array([], dtype='float32'),
            durations=np.array([], dtype='float32'))
        return segments

    def load_submissions(self,chromaEstimator, path_extractor, exercise_id2annotations, submissions, segments = None):
        if segments == None:
            segments = self.create_segments_variable()
        for s in submissions:
            print('Loading: ',s['path'])
            audio_file = os.path.join(self.base_path, s['path'])
            latency = s['latency']
            anno_file = exercise_id2annotations[s['exercise_id']]
            temp_audio = "q.wav"
            remove_latency(audio_file, temp_audio, latency)
            path_extractor.set(temp_audio, s['id'])

            chunk = chromaEstimator.load_chromas_for_annotation_file(anno_file)
            segments.chromas = np.concatenate((segments.chromas, chunk.chromas))
            segments.labels = np.concatenate((segments.labels, chunk.labels))
            segments.pitches = np.concatenate((segments.pitches, chunk.pitches))
            segments.kinds = np.concatenate((segments.kinds, chunk.kinds))
            segments.uids = np.concatenate((segments.uids, chunk.uids))
            segments.start_times = np.concatenate((segments.start_times, chunk.start_times))
            segments.durations = np.concatenate((segments.durations, chunk.durations))

        return segments

    def load_chromas_for_dataset(self, exercise_annotaion_mapping, recordings, segments = None):
        with open(self.base_path + recordings) as af:
            recordings = json.load(af)

        path_extractor = ExerciseAudioPathExtractor()
        chromaEstimator = AnnotatedBeatChromaEstimator(
            chroma_estimator=NNLSChromaEstimator(audio_path_extractor=path_extractor),
            segment_chroma_estimator=AdaptiveChromaEstimator(),
            label_translator=GuitarLabelTranslator(),
            uid_extractor=path_extractor)

        return self.load_submissions(chromaEstimator, path_extractor,exercise_annotaion_mapping, recordings, segments)

    def train_test_split(self,ex_id_map,recordings,filter_field = None,segments = None):
        with open(self.base_path + recordings) as af:
            recordings = json.load(af)
        train = []
        test = []

        if filter_field:
            for s in recordings:
                if any(f in s['name'] for f in filter_field):
                    train.append(s)
                else:
                    test.append(s)
        else:
            for s in recordings:
                test.append(s)

        path_extractor = ExerciseAudioPathExtractor()
        if filter_field:
            chromaEstimator_Train = AnnotatedBeatChromaEstimator(
                chroma_estimator=NNLSChromaEstimator(audio_path_extractor=path_extractor),
                segment_chroma_estimator=AdaptiveChromaEstimator(),
                label_translator=GuitarLabelTranslator(),
                uid_extractor=path_extractor,
                roll_to_c_root= True)

        chromaEstimator_Test = AnnotatedBeatChromaEstimator(
            chroma_estimator=NNLSChromaEstimator(audio_path_extractor=path_extractor),
            segment_chroma_estimator=AdaptiveChromaEstimator(),
            label_translator=GuitarLabelTranslator(),
            uid_extractor=path_extractor,
            roll_to_c_root= False)

        train_segments = segments
        if filter_field:
            print('Building Train set...')
            train_segments = self.load_submissions(chromaEstimator_Train, path_extractor,ex_id_map, train, segments)

        print('Building test set ...')
        test_segments = self.load_submissions(chromaEstimator_Test, path_extractor,ex_id_map, test, segments = None)
        is_defined = [x != 'unclassified' for x in test_segments.kinds]
        test_segments = AnnotatedChromaSegments(
            test_segments.labels[is_defined],
            test_segments.pitches[is_defined],
            test_segments.kinds[is_defined],
            test_segments.chromas[is_defined],
            test_segments.uids[is_defined],
            test_segments.start_times[is_defined],
            test_segments.durations[is_defined])

        return train, test, train_segments, test_segments