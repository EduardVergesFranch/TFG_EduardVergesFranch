import sys
import copy
sys.path.append('..')


from pychord_tools.low_level_features import  AnnotatedBeatChromaEstimator
from pychord_tools.third_party import NNLSChromaEstimator
from pychord_tools.labels import DEGREES
from pychord_tools import plots
from pychord_tools.compositional_data import substitute_zeros, amalgamate
from simmusic.feature_extraction import AdaptiveChromaEstimator, GuitarLabelTranslator

from test_code.test_utils.training_individual_chord_model import NewModel,SimUidAndAudioPathExtractor
from test_code.Training_Model import append_to_segments, load_segments_for_trainning

import joblib
import numpy as np

# Install if not
from sklearn import preprocessing
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
partitions = {'maj': [[DEGREES.index('I'), DEGREES.index('III'), DEGREES.index('V')],[DEGREES.index('II'), DEGREES.index('VII'), DEGREES.index('IIb'), DEGREES.index('IIIb'), DEGREES.index('IV'),
         DEGREES.index('Vb'), DEGREES.index('VIb'), DEGREES.index('VI'), DEGREES.index('VIIb')]],
              'min':[[DEGREES.index('I'), DEGREES.index('IIIb'), DEGREES.index('V')],[DEGREES.index('II'), DEGREES.index('VII'), DEGREES.index('IIb'), DEGREES.index('III'), DEGREES.index('IV'),
         DEGREES.index('Vb'), DEGREES.index('VIb'), DEGREES.index('VI'), DEGREES.index('VIIb')]],
              '1': [[DEGREES.index('I'), DEGREES.index('III'), DEGREES.index('V')],[DEGREES.index('II'), DEGREES.index('VII'), DEGREES.index('IIb'), DEGREES.index('IIIb'), DEGREES.index('IV'),
         DEGREES.index('Vb'), DEGREES.index('VIb'), DEGREES.index('VI'), DEGREES.index('VIIb')]],
              '5': [[DEGREES.index('I'), DEGREES.index('V')],[DEGREES.index('II'), DEGREES.index('IIIb'), DEGREES.index('VII'), DEGREES.index('IIb'), DEGREES.index('III'), DEGREES.index('IV'),
         DEGREES.index('Vb'), DEGREES.index('VIb'), DEGREES.index('VI'), DEGREES.index('VIIb')]],
              '+3':[[DEGREES.index('I'), DEGREES.index('III')],[DEGREES.index('II'), DEGREES.index('VII'), DEGREES.index('V'), DEGREES.index('IIb'), DEGREES.index('IIIb'), DEGREES.index('IV'),
         DEGREES.index('Vb'), DEGREES.index('VIb'), DEGREES.index('VI'), DEGREES.index('VIIb')]],
              '-3':[[DEGREES.index('I'), DEGREES.index('IIIb')],[DEGREES.index('II'), DEGREES.index('V') ,DEGREES.index('VII'), DEGREES.index('IIb'), DEGREES.index('III'), DEGREES.index('IV'),
         DEGREES.index('Vb'), DEGREES.index('VIb'), DEGREES.index('VI'), DEGREES.index('VIIb')]]}

class CHORDS_NOTES_VISUALIZATION():
    def __init__(self,segments_raw,event = None, kind = 'maj',normalize_to_C= False):
        self.partition = partitions[kind]
        self.kind  = kind
        if normalize_to_C:
            segments = copy.deepcopy(segments_raw)
            for i in range(len(segments.chromas)):
                shift = 12 - segments.pitches[i]
                segments.chromas[i] = np.roll(
                    segments.chromas[i], shift=shift)
        else:
            segments = segments_raw
        if event:
            self.segments = preprocessing.normalize(substitute_zeros(segments.chromas[segments.labels == event]), norm='l1')
        else:
            self.segments = preprocessing.normalize(substitute_zeros(segments.chromas[segments.kinds == kind]), norm='l1')
        self.dframe = pd.DataFrame(data=self.segments, columns=DEGREES)

    def mean_intensity_by_degree(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(18, 5), dpi=90, facecolor='w', edgecolor='k')

        m = np.mean(self.dframe)
        ax.set_title('Mean intensity by degree - ' + self.kind + ' chord/notes')
        ax.set_ylabel('Intensity')
        ax.set_xlabel('Degrees')
        m.plot(kind='bar', ax=ax)

    def intensity_distribution_by_degree(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(18, 5), dpi=90, facecolor='w', edgecolor='k')
        ax.set_title('Intensity distribution by degree - ' + self.kind + ' chord/notes')
        ax.set_ylabel('Intensity')
        ax.set_xlabel('Degrees')
        sns.violinplot(data=self.dframe, inner="point", axes=ax)

    def hexagram(self):
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 8), dpi=90, facecolor='w', edgecolor='k')
        sorted_degrees = plots.sorted_degrees(self.segments, flip=True)

        ax[0].set_title('Strong degrees - ' + self.kind + ' chord/notes')
        ax[1].set_title('Weak degrees -  ' + self.kind + ' chord/notes')
        plots.plot_strong_weak_hexagrams(ax[0], ax[1], self.segments, sorted_degrees)
        plt.show()

    def ratio(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(18, 5), dpi=90, facecolor='w', edgecolor='k')
        print(self.partition)
        chord_ratio = amalgamate(self.partition, self.segments).transpose()[0]
        plt.title('Strong/Weak degrees ratio')
        plt.hist(chord_ratio, range=(0, 1), bins=20)

    def plot_all(self):
        # Marginal degrees distribution
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 5), dpi=90, facecolor='w', edgecolor='k')

        m = np.mean(self.dframe)
        ax[0].set_title('Mean intensity by degree ('+ self.kind +')')
        m.plot(kind='bar', ax=ax[0])

        ax[1].set_title('Intensity distribution by degree ('+ self.kind +')')
        sns.violinplot(data=self.dframe, inner="point", axes=ax[1])

        # joint degrees distribution

        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 8), dpi=90, facecolor='w', edgecolor='k')
        sorted_degrees = plots.sorted_degrees(self.segments, flip=True)

        ax[0].set_title('Strong degrees - Joint Distribution ('+ self.kind +')')
        ax[1].set_title('Weak degrees - Joint Distribution ('+ self.kind +')')
        plots.plot_strong_weak_hexagrams(ax[0], ax[1], self.segments, sorted_degrees)
        plt.show()

        # Strong/weak ratio
        chord_ratio = amalgamate(self.partition, self.segments).transpose()[0]
        plt.title('Strong/Weak degrees ratio ('+ self.kind +')')
        plt.hist(chord_ratio, range=(0, 1), bins=20)