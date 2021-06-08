# Load segments from audio and annotaion files

from Code.test_utils.training_individual_chord_model import NewModel, SimUidAndAudioPathExtractor, load_file_list

import os
import numpy as np
import json
from random import seed
from random import randrange
import time

from pychord_tools.low_level_features import  AnnotatedBeatChromaEstimator, AnnotatedChromaSegments
from pychord_tools.third_party import NNLSChromaEstimator
from pychord_tools.low_level_features import AudioPathExtractor, UidExtractor

from simmusic.feature_extraction import AdaptiveChromaEstimator, GuitarLabelTranslator
from simmusic.latency import remove_latency

from sklearn.model_selection import KFold

from joblib import Memory
location = '../Cached_Segments/'
memory = Memory(location, verbose=0)

ex_2_id={0:'../test_data/Lily Was Here/Lily Was Here.json',
         1:'../test_data/Mountain At My Gates/Mountain At My Gates.json',
         2:'../test_data/20th Century Boy/20th Century Boy.json',
         3:'../test_data/Where Did You Sleep Last Night/Where Did You Sleep Last Night.json',
         4:'../test_data/Hole In My Shoe/Hole In My Shoe.json',
         5:'../test_data/Runaway Train/Runaway Train.json'}
song_2_anno={'Lily':'../test_data/Lily Was Here/Lily Was Here.json',
         'Mountain':'../test_data/Mountain At My Gates/Mountain At My Gates.json',
         'Century':'../test_data/20th Century Boy/20th Century Boy.json',
         'Where':'../test_data/Where Did You Sleep Last Night/Where Did You Sleep Last Night.json',
         'Hole':'../test_data/Hole In My Shoe/Hole In My Shoe.json',
         'Train':'../test_data/Runaway Train/Runaway Train.json'}

def describe_data (recordings):
    sources = {}
    properties = {}
    songs = {}
    for t in recordings:

        try : 
            source = t['name'].split('_')[3].replace('.wav','')

        except : 
            source = t['name'].split('_')[2].replace('.wav','')

        if source not in sources.keys():
            sources[source] = 0
        else:
            sources[source] += 1

        try : 
            prop = t['name'].split('_')[4].replace('.wav','')

            if prop not in properties.keys():
                properties[prop] = 0
            else:
                properties [prop] += 1
        except : 
            pass
        
        try : 
            song = t['name'].split('_')[0].replace('.wav','')

            if song  not in songs.keys():
                songs[song] = 0
            else:
                songs[song] += 1
        except : 
            pass
        
    print('Recordings by source: {}'.format(sources))
    print('Recordings by property: {}'.format(properties))
    print('Recordings by song: {}'.format(songs))

   
class ExerciseAudioPathExtractor(AudioPathExtractor, UidExtractor):
    def set(self, audio_path, uid_value):
        self.audio_path = audio_path
        self.uid_value = uid_value

    def audio_path_name(self, uid):
        return self.audio_path

    def uid(self, annotation_file_name):
        return self.uid_value
    
def create_segments_variable():
        segments = AnnotatedChromaSegments(
            labels=np.array([], dtype='object'),
            pitches=np.array([], dtype='int'),
            kinds=np.array([], dtype='object'),
            chromas=np.zeros((0, 12), dtype='float32'),
            uids=np.array([], dtype='object'),
            start_times=np.array([], dtype='float32'),
            durations=np.array([], dtype='float32'))
        return segments
    
def load_submissions(chromaEstimator, path_extractor, exercise_id2annotations, submissions, base_path, segments = None):
    if segments == None:
        segments = create_segments_variable()
    for s in submissions:
        print('Loading: ',s['path'])
        audio_file = os.path.join(base_path, s['path'])
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
    
def create_AnnotatedBeatChromaEstimator(roll_to_c = True):
    path_extractor = ExerciseAudioPathExtractor()
    chromaEstimator = AnnotatedBeatChromaEstimator(
            chroma_estimator=NNLSChromaEstimator(audio_path_extractor=path_extractor),
            segment_chroma_estimator=AdaptiveChromaEstimator(),
            label_translator=GuitarLabelTranslator(),
            uid_extractor=path_extractor,
            roll_to_c_root= roll_to_c )
    return chromaEstimator, path_extractor

class SEGMENTS_LOADER():
    def __init__(self, base_path):
        self.base_path = base_path
        
    def load_annotation_list(self, list):

        return load_file_list(list, self.base_path)

    def load_chromas_annotation_list(self, list):

        list = self.load_annotation_list(os.path.join(self.base_path,list))
        print('Loaded {} files.'.format(len(list)))
        chromaEstimator = AnnotatedBeatChromaEstimator(
            chroma_estimator=NNLSChromaEstimator(),
            segment_chroma_estimator=AdaptiveChromaEstimator(),
            label_translator=GuitarLabelTranslator(),
            uid_extractor=SimUidAndAudioPathExtractor(self.base_path))
        return chromaEstimator.load_chromas_for_annotation_file_list(list)

    def load_chromas_for_dataset(self, exercise_annotaion_mapping, recordings, roll_to_c = False, segments = None):
        with open(self.base_path + recordings) as af:
            recordings = json.load(af)
            print('Loaded {} files.'.format(len(recordings)))
            
        chromaEstimator,path_extractor = create_AnnotatedBeatChromaEstimator(roll_to_c = roll_to_c)
        
        _load = memory.cache(load_submissions)
        
        start = time.time()
        segments = _load(chromaEstimator,
                        path_extractor,
                        exercise_annotaion_mapping,
                        recordings,
                        self.base_path,
                        segments)
        end = time.time()
        print('\n--->>>The train segments  loading took {:.2f} s to compute.'.format(end - start))
        
        return segments
    def train_test_split_filtered_field(self,ex_id_map,recordings,filter_field = None,segments = None):
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

        if filter_field:
            chromaEstimator_Train, path_extractor_train =  create_AnnotatedBeatChromaEstimator(roll_to_c = True)

        chromaEstimator_Test, path_extractor_test=  create_AnnotatedBeatChromaEstimator(roll_to_c = False)

        train_segments = segments
        
        print(memory)
        _load = memory.cache(load_submissions)
        
        if filter_field:
            print('Building Train set...')
            start = time.time()
            train_segments = _load(chromaEstimator_Train,
                                              path_extractor_train,
                                              ex_id_map,
                                              train,
                                              self.base_path,
                                              segments)
            end = time.time()
            print('\n--->>>The train segments  loading took {:.2f} s to compute.'.format(end - start))

        print('Building test set ...')
        start = time.time()
        test_segments = _load(chromaEstimator_Test,
                                         path_extractor_test,
                                         ex_id_map, 
                                         test,
                                         self.base_path,
                                         segments = None)
        end = time.time()
        print('\n--->>>The test segments  loading took {:.2f} s to compute.'.format(end - start))

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

    def K_fold_generation(self,database_indices,events, splits = 5):
        database_indices = np.array(database_indices)
        kf = KFold(n_splits=splits)
        folds = {}
        count = 0
        for train_index, test_index in kf.split(database_indices):
            train_rec = []
            test_rec = []
            for e in events:
                if e['id'] in database_indices[train_index]:
                    train_rec.append(e)
                else:
                    test_rec.append(e)

            folds[count] = (train_rec,test_rec)
            count += 1
        return folds

    def train_test_split_indexes(self,num_of_rec, split=0.60):
        dataset = np.arange(num_of_rec + 1)

        train = list()
        train_size = split * num_of_rec
        test = list(dataset)
        while len(train) < train_size:
            index = randrange(len(test))
            train.append(test.pop(index))
        return train, test

    def load_folds_database(self, database, folds_num = 5, split = 0.60):

        with open(self.base_path + database) as f:
            events = json.load(f)
            event = max(events, key=lambda ev: ev['id'])

            num_of_rec = event['id'] + 1
            return self.K_fold_generation(np.arange(num_of_rec), events, folds_num)

    def load_train_test_segments(self,train_rec, test_rec, ex_id_map, segments=None):
        rng = np.random.RandomState(42)
        
        
        chromaEstimator_Train, path_extractor_Train =  create_AnnotatedBeatChromaEstimator(roll_to_c = True)
        chromaEstimator_Test,path_extractor_Test =  create_AnnotatedBeatChromaEstimator(roll_to_c = False)

        train_segments = segments
        
        
        print(memory)
        print('Building train set ...')
        _load = memory.cache(load_submissions)
        
        start = time.time()
        train_segments = _load(chromaEstimator_Train,
                                          path_extractor_Train,
                                          ex_id_map,
                                          train_rec,
                                          self.base_path,
                                          segments)
        end = time.time()
        print('\n--->>>The train segments  loading took {:.2f} s to compute.'.format(end - start))
        
        print('Building test set ...')
        start = time.time()
        
        test_segments = _load(chromaEstimator_Test,
                              path_extractor_Test, 
                              ex_id_map, 
                              test_rec,     
                              self.base_path, 
                              segments=None)
        end = time.time()
        print('\n--->>>The test segments  loading took {:.2f} s to compute.'.format(end - start))
        
        is_defined = [x != 'unclassified' for x in test_segments.kinds]
        test_segments = AnnotatedChromaSegments(
            test_segments.labels[is_defined],
            test_segments.pitches[is_defined],
            test_segments.kinds[is_defined],
            test_segments.chromas[is_defined],
            test_segments.uids[is_defined],
            test_segments.start_times[is_defined],
            test_segments.durations[is_defined])

        return train_rec, test_rec, train_segments, test_segments
        
       
        return train_rec, test_rec, train_segments, test_segments

    def train_test_split_json(self, database,ex_id_map, seed_num  =1, split=0.70, segments=None):
        seed(seed_num)
        with open(self.base_path + database) as f:
            events = json.load(f)

            event = max(events, key=lambda ev: ev['id'])
            num_of_rec = event['id']
            train_indx, test_indx = self.train_test_split_indexes(num_of_rec, split=split)

            train_rec = []
            test_rec = []
            for e in events:
                if e['id'] in train_indx:
                    train_rec.append(e)
                else:
                    test_rec.append(e)

        return self.load_train_test_segments(train_rec,test_rec,ex_id_map,segments = segments)