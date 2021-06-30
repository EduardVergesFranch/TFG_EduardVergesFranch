import numpy as np
import joblib
import scipy.stats
from scipy.stats import beta
from sklearn import preprocessing
from sklearn.mixture import GaussianMixture
from scipy.special import logsumexp

from pychord_tools.low_level_features import AudioPathExtractor, UidExtractor
from pychord_tools.compositional_data import alr
from pychord_tools.compositional_data import amalgamate
from pychord_tools.compositional_data import subcomposition
from pychord_tools.compositional_data import substitute_zeros
from pychord_tools.labels import PITCH_CLASS_NAMES, PitchedPattern, degree_indices, convert_chord_labels
from pychord_tools.models import CorrectnessBalanceResidualsModel, IndependentPDFModel
from pychord_tools.low_level_features import AnnotatedChromaSegments, AnnotatedBeatChromaEstimator
from pychord_tools.third_party import NNLSChromaEstimator, ChromaEstimator,nnls_chroma_from_audio
from simmusic.feature_extraction import AdaptiveChromaEstimator, GuitarLabelTranslator, my_nnls_chroma_from_audio

from simmusic.latency import remove_latency

import json
import os

class NewModel(CorrectnessBalanceResidualsModel):
    """
    Correctness/Balance/Residuals chord model.
    Balance is modeled as Log normal.
    """
    def __init__(self, kind_to_degrees_dict, kind_to_gmm_params, kind_to_external_names=None):
        """
        :param kind_to_degrees_dict: Dictionary of chord/scale kinds
        to degree name list, e.g., {'maj':['I', 'III', 'V']}
        """
        CorrectnessBalanceResidualsModel.__init__(self, list(kind_to_degrees_dict.keys()), kind_to_external_names)
        self.kind_to_gmm_params = kind_to_gmm_params
        self.out_degree_dict = dict()
        self.in_degree_dict = dict()

        for k, v in kind_to_degrees_dict.items():
            self.in_degree_dict[k] = degree_indices(v)
            self.out_degree_dict[k] = list(set(range(12)).difference(set(self.in_degree_dict[k])))

        self.balanceGMMs = dict()
        self.betas = dict()

    def preprocess(self, chroma):
        if chroma.shape[0] >= 2: #Before chroma.shape[1] >= 2 [0,12]
            return preprocessing.normalize(substitute_zeros(chroma), norm='l1')
        else:
            return chroma

    def train_alr_gaussian(self, vectors, params_dict):
        gmm = GaussianMixture(**params_dict)
        if vectors.shape[1] > 1:
            vectors = np.apply_along_axis(alr, 1, vectors)
            gmm.fit(vectors)
            return gmm

    def fit(self, segments):
        """
        Fits the model to given chroma segments.
        :param segments: AnnotatedChromaSegment list
        """
        in_chroma_sums = dict()

        for k in self.kinds: # maj, min , 1, 5 , +3, -3
            chroma_raw = segments.chromas[segments.kinds == k]
            if chroma_raw.shape[0] >= 2:
                chroma = self.preprocess(chroma_raw)
                partition = [self.in_degree_dict[k], self.out_degree_dict[k]]
                in_chroma_sums[k] = amalgamate(partition, chroma).transpose()[0]
                in_chroma_composition = subcomposition([[e] for e in self.in_degree_dict[k]], chroma)
                print("Now training: ", k)
                self.betas[k] = beta(*beta.fit(in_chroma_sums[k], floc=0, fscale=1))
                self.balanceGMMs[k] = self.train_alr_gaussian(in_chroma_composition, self.kind_to_gmm_params[k])

    def score_balance(self, kind, pre_chromas):
        in_chroma_composition = subcomposition([[e] for e in self.in_degree_dict[kind]], pre_chromas)
        if in_chroma_composition.shape[1] > 1:
            in_chroma_composition = np.apply_along_axis(alr, 1, in_chroma_composition)
        return self.balanceGMMs[kind].score_samples(in_chroma_composition)

    def log_utilities(self, chromas, normalize=True):
        lps = np.zeros((len(chromas), len(self.externalNames)))
        chromas = chromas.astype('float64')
        for basePitch in range(len(PITCH_CLASS_NAMES)):
            pos = basePitch * self.n_kinds
            # NOTE: log-ratio preprocessing should be applied to shifted
            # chroma, so we always do it inside loop.
            pre_chromas = self.preprocess(chromas) #Normalize chroma that all intensities sum to 1
            ki = 0
            for k in self.kinds:
                partition = [self.in_degree_dict[k], self.out_degree_dict[k]]
                in_chroma_sums = amalgamate(partition, pre_chromas).transpose()[0] #SUm all in chroma intensities
                in_chroma_composition = subcomposition([[e] for e in self.in_degree_dict[k]], pre_chromas)
                correctness = self.betas[k].logcdf(in_chroma_sums) #Check correctness of pitch class -> Not wrong/incorrect/unexpected notes

                if in_chroma_composition.shape[1] > 1:
                    in_chroma_composition = np.apply_along_axis(alr, 1, in_chroma_composition)
                balance = self.balanceGMMs[k].score_samples(in_chroma_composition) # Check that notes that are played are balanced in terms of intensity.
                # Gausian Mixture that assigns probability of belonging to a pitch class set for each chroma detected by NNLS Chroma
                lps[:, pos + ki] = (correctness + balance) # Save probability of belonging to a specific pitch class set into a matrix
                ki += 1
            chromas = np.roll(chromas, -1, axis=1) # Change the firts positon of the chroma to the final position -> (Is the same of changing the rooot) ROOT is the first element of the chroma array
        if normalize:
            norm_sum = logsumexp(lps, axis=1)
            return lps - norm_sum[:, np.newaxis]
        else:
            return lps

    def correctness(self, chromas, normalize=False):
        res = np.zeros((len(chromas), len(self.externalNames)))
        chromas = chromas.astype('float64')
        for basePitch in range(len(PITCH_CLASS_NAMES)):
            pos = basePitch * self.n_kinds
            # NOTE: log-ratio preprocessing should be applied to shifted
            # chroma, so we always do it inside loop.
            pre_chromas = self.preprocess(chromas)
            ki = 0
            for k in self.kinds:
                partition = [self.in_degree_dict[k], self.out_degree_dict[k]]
                in_chroma_sums = amalgamate(partition, pre_chromas).transpose()[0]
                res[:, pos + ki] += self.betas[k].logcdf(in_chroma_sums)
                ki += 1
            chromas = np.roll(chromas, -1, axis=1)
        if normalize:
            norm_sum = logsumexp(res, axis=1)
            return res - norm_sum[:, np.newaxis]
        else:
            return res

    def balance(self, chromas, normalize=False):
        res = np.zeros((len(chromas), len(self.externalNames)))
        chromas = chromas.astype('float64')
        for basePitch in range(len(PITCH_CLASS_NAMES)):
            pos = basePitch * self.n_kinds
            # NOTE: log-ratio preprocessing should be applied to shifted
            # chroma, so we always do it inside loop.
            pre_chromas = self.preprocess(chromas)
            ki = 0
            for k in self.kinds:
                res[:, pos + ki] += self.score_balance(k, pre_chromas)
                ki += 1
            chromas = np.roll(chromas, -1, axis=1)
        if normalize:
            norm_sum = logsumexp(res, axis=1)
            return res - norm_sum[:, np.newaxis]
        else:
            return res

    def log_utilities_given_sequence(self, chromas, pitched_patterns, normalize=False):
        if normalize:
            lu = self.log_utilities(chromas) # Per Chroma probabilities of belonging to a specific pitch class set
            indices = [p.pitch_class_index * self.n_kinds + self.kinds.index(p.kind) for p in pitched_patterns]
            return np.array([lu[i, indices[i]] for i in range(len(indices))])
        else:
            return self.correctness_given_sequence(chromas, pitched_patterns) +\
                   self.balance_given_sequence(chromas, pitched_patterns)

    def correctness_given_sequence(self, chromas, pitched_patterns, normalize=False):
        res = np.zeros(len(chromas))
        if len(chromas) != len(pitched_patterns):
            raise ValueError("Input vectors need to be equal size.")
        if normalize:
            c = self.correctness(chromas, True)
            indices = [p.pitch_class_index * self.n_kinds + self.kinds.index(p.kind) for p in pitched_patterns]
            return np.array([c[i, indices[i]] for i in range(len(indices))])
        else:
            for i in range(len(pitched_patterns)):
                c = self.preprocess(np.roll(chromas[i].reshape(1, -1), -pitched_patterns[i].pitch_class_index))
                k = pitched_patterns[i].kind
                partition = [self.in_degree_dict[k], self.out_degree_dict[k]]
                in_chroma_sums = amalgamate(partition, c)[:, 0]
                res[i] = self.betas[k].logcdf(in_chroma_sums)
        return res

    def balance_given_sequence(self, chromas, pitched_patterns, normalize=False):
        res = np.zeros(len(chromas))
        if len(chromas) != len(pitched_patterns):
            raise ValueError("Input vectors need to be equal size.")
        if normalize:
            b = self.balance(chromas, True)
            indices = [p.pitch_class_index * self.n_kinds + self.kinds.index(p.kind) for p in pitched_patterns]
            return np.array([b[i, indices[i]] for i in range(len(indices))])
        else:
            for i in range(len(pitched_patterns)):
                c = self.preprocess(np.roll(chromas[i].reshape(1, -1), -pitched_patterns[i].pitch_class_index))
                k = pitched_patterns[i].kind
                res[i] = self.score_balance(k, c)
        return res

    def max_balance(self):
        candidates = []
        for k in self.kinds:
            candidates.append(self.balanceGMMs[k].score_samples(
                self.balanceGMMs[k].means_))
        return max(candidates)

######################################################################


def load_file_list(listFileName, data_dir):
    result = []
    with open(listFileName) as list_file:
        for line in list_file:
            result.append(line.rstrip().replace('%PYSIM_CHORDS_TEST_DATA_DIR%', data_dir))
    return result


from pychord_tools.path_db import set_audio_path

class SimUidAndAudioPathExtractor(AudioPathExtractor, UidExtractor):
    def __init__(self, pysim_chords_test_data_dir):
        self.data_dir = pysim_chords_test_data_dir

    def audio_path_name(self, annotationFileName):
        with open(annotationFileName) as json_file:
            data = json.load(json_file)
            audioPath = str(
                data['sandbox']['path']).replace('%PYSIM_CHORDS_TEST_DATA_DIR%', self.data_dir)
            set_audio_path(audioPath, audioPath)
            return audioPath

    def uid(self, annotation_file_name):
        return self.audio_path_name(annotation_file_name)

##########################################

if __name__ == "__main__":
    pysim_chords_test_data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data'))

    chromaEstimator = AnnotatedBeatChromaEstimator(
        chroma_estimator=NNLSChromaEstimator(),
        segment_chroma_estimator=AdaptiveChromaEstimator(),
    #    segment_chroma_estimator=SmoothedStartingBeatChromaEstimator(0.6),
        label_translator=GuitarLabelTranslator(),
        uid_extractor=SimUidAndAudioPathExtractor(pysim_chords_test_data_dir))
    l = load_file_list(
        os.path.join(pysim_chords_test_data_dir, 'annotations/correct.txt'),
        pysim_chords_test_data_dir)
    segments = chromaEstimator.load_chromas_for_annotation_file_list(l)

    #
    # Adding data from exercises.
    #

    exercise_id2annotations = {
        26: 'data/exercises/Leah17Dec2018/Lesson01Ex1/l1ex1.json',
        20: 'data/exercises/Leah17Dec2018/Lesson02Ex1/l2ex1.json',
        17: 'data/exercises/Leah17Dec2018/Lesson02Ex2/l2ex2.json',
        16: 'data/exercises/Leah17Dec2018/Lesson03Ex1/l3ex1.json',
        27: 'data/exercises/Leah17Dec2018/Lesson04Ex1/l4ex1.json',
        25: 'data/exercises/Leah17Dec2018/Lesson05Ex1/l5ex1.json'
    }

    # strumming
    strumming_ids=set()
    strumming_ids.update([26, 17, 25])

    with open("one_time_scripts/guitar_samples_annotation/chroma_pattern_dataset.json") as af:
        submissions = json.load(af)

    #pysim_chords_test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    pysim_chords_test_data_dir = os.path.abspath(os.path.join(os.getcwd(), 'data'))

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

    for s in submissions:
        # filter exercise
        # if s['exercise_id'] in strumming_ids:
            audio_file = os.path.join("one_time_scripts/guitar_samples_annotation", s['path'])
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


    #
    # Training
    #

    new_model = NewModel(
        {'maj':['I', 'III', 'V'], 'min':['I', 'IIIb', 'V'], '5':['I', 'V'], '1':['I', 'V', 'III'],
         '+3':['I','III'], 'b3':['I','bIII']},

        {'maj':{'n_components':1, 'covariance_type':'full', 'max_iter':200},
         'min':{'n_components':1, 'covariance_type':'full', 'max_iter':200},
         '5':{'n_components':1, 'covariance_type':'full', 'max_iter':200},
         '1':{'n_components':1, 'covariance_type':'full', 'max_iter':200},
         '+3':{'n_components':1, 'covariance_type':'full', 'max_iter':200},
         '-3':{'n_components':1, 'covariance_type':'full', 'max_iter':200}})
    new_model.fit(segments)
    new_model.save_model('new_model.pkl')
    
    m = IndependentPDFModel({'maj':['I', 'III', 'V'], 'min':['I', 'IIIb', 'V'], '5':['I', 'V'], '1':['I']})
    m.fit(segments)
