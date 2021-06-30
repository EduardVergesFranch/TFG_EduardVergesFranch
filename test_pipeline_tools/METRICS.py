# Load pysimmusic assessement for a score
import sys
sys.path.append('../')

from Code.test_utils.training_individual_chord_model import *
from Code.test_utils.test_functionality import estimate_segment_scores

from pychord_tools.models import load_model

from sklearn.metrics import confusion_matrix,accuracy_score,\
                            precision_recall_fscore_support

import statistics
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import json

from IPython.display import display, Markdown

annotations_paths = ['../test_data/Lily Was Here/Lily Was Here.json',
        '../test_data/Mountain At My Gates/Mountain At My Gates.json',
        '../test_data/20th Century Boy/20th Century Boy.json',
        '../test_data/Where Did You Sleep Last Night/Where Did You Sleep Last Night.json',
        '../test_data/Hole In My Shoe/Hole In My Shoe.json', 
        '../test_data/Runaway Train/Runaway Train.json']    
songs = ['Lily','Mountain','Century','Where','Hole','Train']
guitars = ['Eastman','Larrivee','Telecaster','Epiphone','Ibanez']

def precison_recall_bar_plot(precision, recall, support, labels, path):
    x = np.arange(len(labels))  # the label locations
    width = 0.40  # the width of the bars

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.bar(x - width / 2, precision, width, label='Precision', align='center')
    ax.bar(x + width / 2, recall, width, label='Recall', align='center')

    present = np.where(support > 0)[0]
    for p in present:
        ax.axvline(x=p, color='r', linestyle='--')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_xlabel('Kinds')
    ax.set_title('Performance by Music Event kind')
    ax.set_xticks(x)

    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()
    plt.xticks(rotation=45)

    if path:
        plt.savefig(path)
    plt.show()
    
class Kind_Metrics ():
    def __init__(self, kinds, pred, labels= ['maj','min','1','5','+3','-3']):
        pred_kinds = [p.split(':')[-1] for p in pred]

        self.gt = kinds
        self.pred = pred_kinds
        self.labels = labels
    def accuracy(self, info = True):
        acc = np.round(accuracy_score(self.gt,self.pred), 4)
        if info : print('Accuracy: {}'.format(acc))
        return acc
    def conf_matrix(self, plot = True , path = None):

        cm = confusion_matrix(self.gt, self.pred, labels=self.labels)

        if plot:
            plt.figure(figsize=(5, 5))

            plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            plt.title('Confusion Matrix')
            plt.colorbar(fraction=0.046, pad=0.04)
            tick_marks = np.arange(len(self.labels))

            plt.xticks(tick_marks, self.labels, rotation=45)
            plt.yticks(tick_marks, self.labels)

            fmt = 'd'
            thresh = cm.max() / 2.

            for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
                if cm[i, j] > 0:
                    plt.text(j, i, format(cm[i, j], fmt),
                             horizontalalignment="center",
                             verticalalignment='center',
                             color="white" if cm[i, j] > thresh else "black")
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            if path:
                plt.savefig(path)
            plt.show()
        return cm    
    
    def per_kind_performance(self, path = None):
        precision, recall, f_score, support = precision_recall_fscore_support(self.gt,
                                                                              self.pred,
                                                                              labels=self.labels)
        precison_recall_bar_plot(precision, recall,support, self.labels, path)
        
        return precision, recall
    
class Overall_Metrics():
    def __init__(self, gt, pred):
        self.gt = gt
        self.pred = pred
        self.labels = list(set(self.gt + self.pred))

    def accuracy(self, info = True):
        acc = np.round(accuracy_score(self.gt,self.pred), 4)
        if info : print('Accuracy: {}'.format(acc))
        return acc

    def conf_matrix(self, plot = True, path = None):

        cm = confusion_matrix(self.gt, self.pred, labels=self.labels)

        if plot:
            plt.figure(figsize=(15, 15))

            plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            plt.title('Confusion Matrix')
            plt.colorbar(fraction=0.046, pad=0.04)
            tick_marks = np.arange(len(self.labels))

            plt.xticks(tick_marks, self.labels, rotation=45)
            plt.yticks(tick_marks, self.labels)

            fmt = 'd'
            thresh = cm.max() / 2.

            for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
                if cm[i, j] > 0:
                    plt.text(j, i, format(cm[i, j], fmt),
                             horizontalalignment="center",
                             verticalalignment='center',
                             color="white" if cm[i, j] > thresh else "black")
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            if path:
                plt.savefig(path)
            plt.show()
        return cm

    def per_class_performance(self, path = None):
        precision, recall, f_score, support = precision_recall_fscore_support(self.gt,
                                                                              self.pred,
                                                                              labels=self.labels)
        precison_recall_bar_plot(precision, recall,support, self.labels , path)

def accuracy_by_source(test_segments,pred, test_audios):
    performance_source_dict = {}
    
    for aud in test_audios:
        audio = aud['name'] #recording name
        uid = aud['id'] #recording id
        
        #Get performance and recording source/effect/filter
        performance = audio.split('_')
        performance = '_'.join(performance[:3])
        source = audio.split('_')[-1].replace('.wav','')
        
        indices = [x == uid for x in test_segments.uids] #indices of chromas belonging to a recording

        #get predictions and gt for a recording anc calculate accuracy
        gt = list(np.array(test_segments.labels)[indices])
        p = list(np.array(pred)[indices])

        OM = Overall_Metrics(gt, p)
        acc = OM.accuracy(info = False)
        
        
        if performance not in performance_source_dict.keys():
            performance_source_dict[performance] = {}
        
        performance_source_dict[performance][source] = acc
    
    results = pd.DataFrame(performance_source_dict).transpose()
    
    def get_song(s):
        recording_name = s.name.split('_')
        s['Song'] = recording_name [0]
        
        s['Performance'] = '_'.join(recording_name[:2])
        return s
    results = results.apply(lambda x: get_song(x), axis=1)
    
    return results

class Individual_Metrics():
    def __init__(self,annotation, audio,
                 model = '../MODELS/cross-validation/Baseline_Case.pkl',
                 info = True, debug = True, labels_kinds = ['maj','min','5','1','+3','-3'] ):

        self.info = info
        self.debug = debug
        #Store annotation and audio files
        self.annotation = annotation
        self.audio_file = open(audio, "r", encoding="utf-8")
    
        #Load GT and Predicitons
        no_thirds = True
        if ('+3' in labels_kinds) and ('-3' in labels_kinds):
            no_thirds = False
            
        self.real_segments, self.pred = self.all_chroma_scores(self.annotation, self.audio_file.name, model, no_thirds = no_thirds)
        
        self.audio_file.close()
        
        self.pred = [str(self.pred[i]) for i in range(0,len(self.pred))]
        self.gt = [x.replace('(','') for x in self.real_segments.labels]
        self.gt = [x.replace(')','') for x in self.gt]
        
        for i,p in enumerate(self.gt):
            if '1,3' in p:
                self.gt[i] = self.gt[i].replace('1,3','+3')
            elif '1,b3' in p:
                self.gt[i] = self.gt[i].replace('1,b3','-3')
            else:
                pass
        
        #Load all possible pitch class sets defined by the model
#         self.pitch_class_names = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
#         self.pitch_class_kinds = labels_kinds
#         pitch_classes_matrix = np.array(np.meshgrid(self.pitch_class_names,self.pitch_class_kinds)).T.reshape(-1,2)
#         self.list_pitch_classes =[':'.join(x) for x in pitch_classes_matrix]
        self.list_pitch_classes = list(set(self.gt + self.pred))
        # Classify notes by its duration
        self.measure_duration, self.notes_durations = self.classify_note_durations()
        #Variable where the confusion matrix will be stored
        self.confusion_matrix = None
        
        
        with open(self.annotation, 'r') as myfile:
                data=myfile.read()
        obj = json.loads(data)
        self.title = obj['title']
        #Print Song Information
        if info:
            display(Markdown('**Title**: {}'.format(obj['title'])))
            display(Markdown('**Song Duration**: {} sec.'.format(obj['duration'])))
            display(Markdown('**Metre**: {}'.format(obj['metre'])))
            display(Markdown('**Tuning**: {}Hz'.format(obj['tuning'])))
            display(Markdown('**Measure duration**: {} sec.'.format(np.round(self.measure_duration,2))))
        
        
    def classify_note_durations(self):
        """
        Classify notes events according duration
        """
        with open(self.annotation, 'r') as myfile:
            data=myfile.read()
        obj = json.loads(data)
        if obj['metre'] == '3/4':
            measure_duration = np.round(obj['parts'][0]['beats'][3] - obj['parts'][0]['beats'][0],2)
        else:
            measure_duration = np.round(obj['parts'][0]['beats'][4] - obj['parts'][0]['beats'][0],2)
        
        notes_durations = {'full':[],'half':[],'quarter': [],'eight': [],'sixteenth':[]}
        
        if obj['metre'] == '4/4':
            i = 0
            for note,l in zip(self.real_segments.durations,self.real_segments.labels):
                value = np.round(measure_duration / note  ,0)
                if value <= 1:
                    notes_durations['full'].append(i)
                elif value <= 2:
                    notes_durations['half'].append(i)
                elif value <= 4:
                    notes_durations['quarter'].append(i)
                elif value <= 8:
                    notes_durations['eight'].append(i)
                else:
                    notes_durations['sixteenth'].append(i)
                i += 1
                
        if obj['metre'] == '3/4':
            i = 0
            for note,l in zip(self.real_segments.durations,self.real_segments.labels):
                value = np.round(measure_duration / note  ,0)
                if value <= 1:
                    notes_durations['full'].append(i)
                elif value <= 2:
                    notes_durations['half'].append(i)
                elif value <= 3:
                    notes_durations['quarter'].append(i)
                elif value <= 6:
                    notes_durations['eight'].append(i)
                else:
                    notes_durations['sixteenth'].append(i)
                i += 1
        return np.round(measure_duration,2), notes_durations
    
    def all_chroma_scores(self,anno_file, audio_file , model, no_thirds = False):
        """
        Return GT and predicte pitch class sets.
        """
        
        m = joblib.load(model)
        _,_, real_segments = estimate_segment_scores(anno_file, audio_file, m)
        
        if no_thirds: #filter out third intervals if needed for testing purposes
            for i, k in enumerate(real_segments.kinds):
                if k == '+3' or k == '-3':
                    real_segments.kinds[i] = 'unclassified'
                    
            is_defined = [x != 'unclassified' for x in real_segments.kinds]
            
            real_segments = AnnotatedChromaSegments(
                real_segments.labels[is_defined],
                real_segments.pitches[is_defined],
                real_segments.kinds[is_defined],
                real_segments.chromas[is_defined],
                real_segments.uids[is_defined],
                real_segments.start_times[is_defined],
                real_segments.durations[is_defined])  
            
        predicted,_ = m.predict(real_segments.chromas)

            
    #     plot_chroma_scores(real_segments,predicted)

        return real_segments, predicted
    
    def get_desired_notes(self,desired_notes):
        return list(np.array(self.gt)[desired_notes]), list(np.array(self.pred)[desired_notes])
    
    def conf_matrix(self,desired_notes = None):
        """
        Calculate the confusion matrix
        """
        if desired_notes:
            gt,pred = self.get_desired_notes(desired_notes)
        else:
            if self.debug: print('Note duration not specified / Not Found! -> PRINTING GENERAL STATS')
            gt = self.gt
            pred = self.pred
            
        self.confusion_matrix = confusion_matrix(gt,pred,labels = self.list_pitch_classes)
        return self.confusion_matrix
    
    def plot_simple_conf_matrix(self,plot = True, labels = None):
        cm = confusion_matrix(self.gt, self.pred, labels = labels)
        if labels == None:
            labels = list(set(self.gt + self.pred))
        if plot:
            plt.figure(figsize = (15,15))

            plt.imshow(cm, interpolation='nearest', cmap = plt.cm.Blues)
            plt.title('Simple Confusion Matrix')
            plt.colorbar(fraction=0.046, pad=0.04)
            tick_marks = np.arange(len(labels))

            plt.xticks(tick_marks, labels, rotation=45)
            plt.yticks(tick_marks, labels)

            fmt = 'd'
            thresh = cm.max() / 2.

            for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
                if cm[i,j] > 0:
                    plt.text(j, i, format(cm[i, j], fmt),
                             horizontalalignment="center",
                             verticalalignment = 'center',
                             color="white" if cm[i, j] > thresh else "black")
            plt.grid(alpha = 0.3)
            plt.tight_layout()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            plt.show()
        
        return cm
    def plot_confusion_matrix(self,desired_notes = None, normalize=False):
                         
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        
        """
       
        self.conf_matrix(desired_notes = desired_notes)
            
        cmap = plt.cm.Blues
        title = 'Confusion matrix'
        
        if normalize:
            self.confusion_matrix = self.confusion_matrix.astype('float') / self.confusion_matrix.sum(axis=1)[:, np.newaxis]
            if self.debug: print("Normalized confusion matrix")
        else:
            if self.debug: print('Confusion matrix, without normalization')
        
        plt.figure(figsize = (15,15))
        plt.imshow(self.confusion_matrix, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar(fraction=0.046, pad=0.04)
        tick_marks = np.arange(len(self.list_pitch_classes))
        
        plt.xticks(tick_marks, self.list_pitch_classes, rotation=45)
        plt.yticks(tick_marks, self.list_pitch_classes)

        fmt = '.2f' if normalize else 'd'
        thresh = self.confusion_matrix.max() / 2.
        
        for i, j in itertools.product(range(self.confusion_matrix.shape[0]), range(self.confusion_matrix.shape[1])):
            if self.confusion_matrix[i,j] > 0:
                plt.text(j, i, format(self.confusion_matrix[i, j], fmt),
                         horizontalalignment="center",
                         verticalalignment = 'center',
                         color="white" if self.confusion_matrix[i, j] > thresh else "black")
        plt.grid(alpha = 0.3)
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.show()
    def overall_accuracy(self,desired_notes = None):
        """
        Compute the overall accuracy -> Ideal would be 1
        """
        if desired_notes:
            gt,pred = self.get_desired_notes(desired_notes)
        else:
            if self.debug: print('Note duration not specified / Not Found! -> PRINTING GENERAL STATS')
            gt = self.gt
            pred = self.pred
            
        return accuracy_score(gt,pred)
    
    
    def per_class_performance(self,desired_notes = None,print_results = True):
        """
        Calculate precision and recall per pitch class set
        desired_notes = list type with indexes of wanted values
        """
        if desired_notes:
            gt,pred = self.get_desired_notes(desired_notes)
        else:
            if self.debug: print('Note duration not specified / Not Found! -> PRINTING GENERAL STATS')
            gt = self.gt
            pred = self.pred
            
        precision, recall, f_score, support = precision_recall_fscore_support(gt,
                                                                              pred,
                                                                              labels = self.list_pitch_classes)
        return precision, recall, f_score, support
    
    def plot_class_precision_recall(self,desired_notes = None):
        """
        Plot precision and recall for pitch class set
        """
        
        precision, recall,_ , support = self.per_class_performance(desired_notes = desired_notes)
        
        x = np.arange(len(self.list_pitch_classes))  # the label locations
        width = 0.50  # the width of the bars
        
        fig, ax = plt.subplots(figsize = (15,5))
        ax.bar(x - width/2, precision, width, label='Precision',align = 'center')
        ax.bar(x+ width/2, recall, width, label='Recall',align = 'center')
        
        present = np.where(support > 0)[0]
        for p in present:
            ax.axvline(x=p, color='r', linestyle='--')
        
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Scores')
        ax.set_xlabel('Pitch Class Sets')
        ax.set_title('Performance by class')
        ax.set_xticks(x)
        
        ax.set_xticklabels(self.list_pitch_classes)
        ax.legend()
        
        
        fig.tight_layout()
        plt.xticks(rotation=45)
        plt.show()
        
    def plot_class_fscore(self,desired_notes = None):
        """
        Plot f-score per pitch class set
        """
        _,_,fscore, support = self.per_class_performance(desired_notes = desired_notes)
        
        x = np.arange(len(self.list_pitch_classes))  # the label locations
        width = 0.35  # the width of the bars
        
        fig, ax = plt.subplots(figsize = (15,5))
        rects1 = ax.bar(x, fscore, width, label='F-score')
        
        present = np.where(support > 0)[0]
        for p in present:
            ax.axvline(x=p, color='r', linestyle='--')
        
        ax.set_ylabel('Scores')
        ax.set_xlabel('Pitch Class Sets')
        ax.set_title('F_score by class')
        ax.set_xticks(x)
        
        ax.set_xticklabels(self.list_pitch_classes)
        ax.legend()
        
        
        fig.tight_layout()
        plt.xticks(rotation=45)
        plt.show()
        
    def pitch_class_set_support_histogram(self,hist = True,desired_notes = None):
        _,_,_, support = self.per_class_performance(desired_notes = desired_notes)

        if hist:
            fig, ax = plt.subplots(figsize = (15,5))
            ax.bar(range(len(self.list_pitch_classes)), support, align='center')
            ax.set_xticks(range(len(self.list_pitch_classes)))
            ax.set_xticklabels(self.list_pitch_classes)

            ax.set_ylabel('Freq.')
            ax.set_xlabel('Pitch Class Sets')
            ax.set_title('Frequency of each Pitch Class Set')
            fig.tight_layout()
            plt.grid(axis='y', alpha=0.75)
            plt.xticks(rotation=45)
            plt.show()
        
        return support
        
    def miss_detection_errors(self,conf_matrix = False):
        not_found_chromas = [ind for ind, chroma in enumerate(self.real_segments.chromas) if all(chroma == 0)]
        
        percentage_missed = len(not_found_chromas) / len(self.gt)
        if self.debug: print('Missed {}% of the chromas.'.format(np.round(percentage_missed * 100,2)))
        
        if conf_matrix:
            self.plot_confusion_matrix(desired_notes = not_found_chromas)
                 
        return percentage_missed, not_found_chromas
    def plot_chroma_scores(self):
        plt.rcParams.update({'font.size': 30})
        fig = plt.figure(figsize=(40,10))
        ax = fig.add_subplot(111)
        
        img = ax.imshow(self.real_segments.chromas.T,cmap='inferno',aspect='auto',interpolation='nearest')
        
        
        not_found_chromas = [ind for ind, chroma in enumerate(self.real_segments.chromas) if all(chroma == 0)]
        for f in not_found_chromas:
            ax.axvline(x=f, color='r', linestyle='-',linewidth =2)
        
        
        
#         cbar = fig.colorbar(img, ax=ax, shrink=0.1, orientation="vertical")
#         cbar.set_label('Intensity')

        ax.set_xticks(range(len(self.pred)))
        ax.set_yticks(range(12))
        
        x_label_list = []
        for i, (n, c) in enumerate(zip(self.pred, self.gt)):
            x_label_list.append(n + '<--' + c)
        
        ax.set_xticklabels(x_label_list)
        ax.set_yticklabels(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
        ax.set_xlabel("Predicted <-- True ")
        ax.set_ylabel('Degrees')
        
        plt.xticks(rotation=-90)
 
        plt.grid(color='w',alpha = 0.3, linestyle='-', linewidth=1)
        plt.title('Pitch class set prediction per chroma')
        plt.show()

