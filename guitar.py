import numpy as np
import matplotlib.pyplot as plt
import jinja2
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import os
import re
from subprocess import call
from scipy.stats import gamma
import essentia.standard as ess
from PIL import Image
from tempfile import NamedTemporaryFile
import simmusic.feature_extraction as feature_extraction
import joblib
from pychord_tools.models import load_model
import simmusic

class AssessmentWorkflow:
    def __init__(self,
                 tuning_estimator,
                 rhythm_estimator,
                 chroma_estimator,
                 overall_estimator,
                 tuning_feature_names,
                 timing_feature_names,
                 chroma_feature_names,
                 tuning_max_frame_peaks=1,
                 tuning_min_frequency=100,
                 tuning_max_frequency=3000,
                 onset_max_spectral_centroid=3500,
                 onset_threshold=2,
                 onset_series_delta=0.22):
        self.tuning_estimator=tuning_estimator
        self.rhythm_estimator=rhythm_estimator
        self.chroma_estimator=chroma_estimator
        self.overall_estimator=overall_estimator
        self.tuning_feature_names=tuning_feature_names
        self.timing_feature_names=timing_feature_names
        self.chroma_feature_names=chroma_feature_names
        self.tuning_max_frame_peaks=tuning_max_frame_peaks
        self.tuning_min_frequency=tuning_min_frequency
        self.tuning_max_frequency=tuning_max_frequency
        self.onset_max_spectral_centroid=onset_max_spectral_centroid
        self.onset_threshold=onset_threshold
        self.onset_series_delta=onset_series_delta

    def chroma_scores(self, anno_file, audio_file):
        pass

    def save_model(self, file_name):
        joblib.dump(self, file_name)


class StrummingWorkflow(AssessmentWorkflow):
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
        return feature_extraction.strumming_chroma_scores(anno_file, audio_file)


class PicknigWorkflow(AssessmentWorkflow):
    def __init__(self,
                 tuning_estimator,
                 rhythm_estimator,
                 chroma_estimator,
                 overall_estimator,
                 tuning_feature_names,
                 timing_feature_names,
                 chroma_feature_names,
                 onset_series_delta=0.1):
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
        return feature_extraction.picking_chroma_scores(anno_file, audio_file)


class ColorIterator:
    def __init__(self, rgbas):
        self.rgbas = rgbas
        self.pos = -1

    def current(self):
        return " %.3f %.3f %.3f" %\
               (self.rgbas[self.pos, 0],
                self.rgbas[self.pos, 1],
                self.rgbas[self.pos, 2])

    def __iter__(self):
        return self

    def next(self):
        self.pos += 1
        if self.pos < len(self.rgbas):
            #print('Pos' + str(self.pos))
            #print(self.current())
            return self.current()
        else:
            raise StopIteration


def dummy_eps(first_bar, last_bar):
    img = Image.new('RGB', (200,10))
    fname = NamedTemporaryFile(suffix='.eps', delete=False)
    img.save(fname)
    fname.close()
    return fname.name


class TempWaveFormsGenerator:
    def __init__(self, gen_lambda):
        self.gen_lambda = gen_lambda
        self.all_files = []

    def eps(self, first_bar, last_bar, w = 1, h = 0.1, left_border_shift=-0.15, right_border_shift=-0.2):
        f = self.gen_lambda(first_bar, last_bar,w, h, left_border_shift, right_border_shift)
        self.all_files.append(f)
        return f

    def clear(self):
        for f in self.all_files:
            os.unlink(f)


def score_image(template_dir, tamplate_name, normLu, eps_lambda=dummy_eps, image_format='png'):
    print('Number of notes detected normLu: {}'.format(len(normLu)))
    m = np.exp(normLu)
    sm = cm.ScalarMappable(
        norm=plt.Normalize(0, 1, clip=True), cmap=plt.get_cmap('RdYlGn'))
    rgbas = sm.to_rgba(m)
    it = ColorIterator(rgbas)

    print('Number of notes detected : {}'.format(len(rgbas)))

    latex_jinja_env = jinja2.Environment(
        block_start_string='%{',
        block_end_string='%}',
        variable_start_string='%{{',
        variable_end_string='}%}',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(template_dir))

    template = latex_jinja_env.get_template(tamplate_name)
    eps_generator = TempWaveFormsGenerator(eps_lambda)
    """
    res = template.render({
        'next_color': lambda: it.next(),
        'current_color': lambda: it.current(),
        'eps_waveform': eps_generator.eps
    })"""

    res = template.render({
        'eps_waveform': eps_generator.eps,
        'next_color': lambda: it.next(),
        'current_color': lambda: it.current()
    })

    fin = NamedTemporaryFile(suffix='.ly', delete=False)
    fin.write(res.encode('UTF8'))
    fin.close()

    if image_format == 'png':
        suffix = 'png'
        lily_format_option = '--png'
    elif image_format == 'pdf':
        suffix = 'pdf'
        lily_format_option = '--pdf'
    else:
        raise ValueError('Unknown image_format: ' + image_format)
    ext_cutter = re.compile('\.' + suffix + '$')
    fout = NamedTemporaryFile(suffix='.' + suffix, delete=False)
    fout.close()
    os.unlink(fout.name)
    call(["lilypond", lily_format_option, '-o', ext_cutter.sub('', fout.name), "-dresolution=300", fin.name])
    os.unlink(fin.name)
    eps_generator.clear()
    return fout.name


def attack_rgba(attack_dev):
    cdict = {'red': [(0.0, 0.0, 0.0),
                     (0.04, 0.0, 0.0),
                     (0.07, 0.99653979, 0.99653979),
                     (0.24, 0.64705882, 0.64705882),
                     (1, 0.64705882, 0.64705882)],

             'green': [(0.0, 0.40784314, 0.40784314),
                       (0.04, 0.40784314, 0.40784314),
                       (0.07, 0.89273356, 0.89273356),
                       (0.24, 0, 0),
                       (1, 0, 0)],

             'blue': [(0.0, 0.21568627, 0.21568627),
                      (0.04, 0.21568627, 0.21568627),
                      (0.07, 0.56908881, 0.56908881),
                      (0.24, 0.14901961, 0.14901961),
                      (1, 0.14901961,0.14901961)]}
    attacks_cm = LinearSegmentedColormap("attack_colors", cdict)
    sm = cm.ScalarMappable(
        norm=plt.Normalize(0, 1, clip=True), cmap=attacks_cm)
    if type(attack_dev) is not np.ndarray:
        attack_dev = np.array([attack_dev])
    abs_devs = np.abs(attack_dev)
    return sm.to_rgba(abs_devs)

# remove after generating pictures.
def attack_rgba_old(attack_dev):
    sm = cm.ScalarMappable(
        norm=plt.Normalize(0, 1, clip=True), cmap=plt.get_cmap('RdYlGn'))
    if type(attack_dev) is not np.ndarray:
        attack_dev = np.array([attack_dev])
    abs_devs = np.abs(attack_dev)
    abs_devs = abs_devs - 0.05
    abs_devs[abs_devs < 0] = 0
    res = 1 - gamma.cdf(abs_devs, 0.8, 0, 0.015)
    return sm.to_rgba(res)


def save_bar_plot(
        audio, expected_attacks, left_time=0.0, right_time=None,
        fs=44100, w=1, h=0.1, dpi=300,
        actual_attacks=np.array([], dtype=float),
        attack_color_func=attack_rgba):
    # half-beat margin
    left = int(left_time * fs)
    if right_time is None:
        right = len(audio)
        right_time = float(right) / fs
    else:
        right = int(right_time * fs)
    fig = plt.figure(frameon=False)
    fig.set_size_inches(w, h)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.set_xlim(left=0, right=right-left)
    fig.add_axes(ax)
    if left < 0:
        addon = np.zeros(-left)
        left = 0
        ax.plot(np.concatenate((addon, audio[left:right]), axis = None), lw=0.5)
    else:
        ax.plot(audio[left:right], lw=0.5)

    # filter events.
    filtered_expected = expected_attacks[(expected_attacks >= left_time) & (expected_attacks < right_time)]
    filtered_actual = actual_attacks[(actual_attacks >= left_time) & (actual_attacks < right_time)]
    for x in filtered_expected:
        plt.axvline((x - left_time) * fs, color='k', lw=0.5)
    for x in filtered_actual:
        i = np.searchsorted(expected_attacks, x)
        if i >= len(expected_attacks) or (0 < i and x - expected_attacks[i - 1] < expected_attacks[i] - x):
            expected_attack = expected_attacks[i - 1]
            x1 = expected_attacks[i - 1]
            x2 = x
            attack_dev = x - expected_attacks[i - 1]
        else:
            expected_attack = expected_attacks[i]
            x1 = x
            x2 = expected_attacks[i]
            attack_dev = x - expected_attacks[i]
        if (expected_attack in filtered_expected):
            rgbas = attack_color_func(attack_dev)
            plt.axvspan((x1 - left_time) * fs, (x2 - left_time) * fs, facecolor=rgbas[0], alpha=0.5)
    #plt.show()
    fname = NamedTemporaryFile(suffix='.eps', delete=False)
    plt.savefig(fname, dpi=dpi, format='eps')
    plt.close(fig)
    fname.close()
    return fname.name


def visualize(
        template_dir,
        template_name,
        bars,
        events,
        onsets,
        chroma_scores,
        audio,
        image_format='png',
        attack_color_func=attack_rgba):
    eps_lambda = lambda first_bar, last_bar, w, h, left_border_shift, right_border_shift:\
        save_bar_plot(
            audio, events,
            actual_attacks = onsets,
            w=w,
            h=h,
            left_time=bars[first_bar][0] + left_border_shift,
            right_time=bars[last_bar][1] + right_border_shift,
            attack_color_func=attack_color_func)
    return score_image(
        template_dir,
        template_name,
        chroma_scores,
        eps_lambda=eps_lambda,
        image_format=image_format)


def fool_proof_assess(estimator, data_vector):
    if np.sometrue(np.isnan(data_vector)):
        return 1
    else:
        return estimator.predict([data_vector])[0]

def assess_guitar_exercise(
        anno_file,
        lilypond_template_file,
        latency,
        student_filename,
        assessment_workflow,
        sample_rate=44100,
        image_format='png',
        attack_color_func=attack_rgba):
    audio = ess.MonoLoader(filename=student_filename)()
    frames = int(latency * sample_rate)
    audio = audio[frames:]
    audio_file = NamedTemporaryFile(suffix='.wav', delete=False)
    audio_file.close()
    os.unlink(audio_file.name)
    ess.MonoWriter(filename=audio_file.name, format='wav')(audio)
    chroma_scores = assessment_workflow.chroma_scores(anno_file, audio_file.name) #nlu

    print('Len Chroma Scores: {}'.format(len(chroma_scores)))
    tuning_statistics = feature_extraction.\
        calculate_statistics_for_deviation_from_equal_temperament(
        audio_file.name,
        max_frame_peaks=assessment_workflow.tuning_max_frame_peaks,
        min_frequency=assessment_workflow.tuning_min_frequency,
        max_frequency=assessment_workflow.tuning_max_frequency)

    timing_features = feature_extraction.timing_features(
        anno_file, audio_file.name,
        max_spectral_centroid=assessment_workflow.onset_max_spectral_centroid,
        onset_threshold=assessment_workflow.onset_threshold,
        series_delta=assessment_workflow.onset_series_delta)
    lilypond_basedir = os.path.dirname(lilypond_template_file)
    lilypond_shortname = os.path.basename(lilypond_template_file)
    img_file_name = visualize(
        lilypond_basedir,
        lilypond_shortname,
        timing_features['bars'],
        timing_features['events'],
        timing_features['onsets'],
        chroma_scores,
        audio,
        image_format=image_format,
        attack_color_func=attack_color_func)
    os.unlink(audio_file.name)

    timing_statistics = feature_extraction.timing_statistics(timing_features['devs'])
    timing_statistics.update(timing_features)
    chroma_statistics = feature_extraction.chroma_statistics(chroma_scores)
    X_tuning = [tuning_statistics[f] for f in assessment_workflow.tuning_feature_names]
    X_timing = [timing_statistics[f] for f in assessment_workflow.timing_feature_names]
    X_chroma = [chroma_statistics[f] for f in assessment_workflow.chroma_feature_names]
    X_overall = []
    X_overall.extend(X_tuning)
    X_overall.extend(X_timing)
    X_overall.extend(X_chroma)
    results = {}
    results["Tuning"] = fool_proof_assess(assessment_workflow.tuning_estimator, X_tuning)
    results["Rhythm"] = fool_proof_assess(assessment_workflow.rhythm_estimator, X_timing)
    results["Pitch"] = fool_proof_assess(assessment_workflow.chroma_estimator, X_chroma)
    results["Overall"] = fool_proof_assess(assessment_workflow.overall_estimator, X_overall)

    # hack, until we'll have enough balanced data to train the model
    results["Overall"] = max(results["Overall"], min(results["Tuning"], results["Rhythm"], results["Pitch"]))

    with open(img_file_name, "rb") as img_file:
        results["ImageBytes"] = img_file.read()
    os.unlink(img_file_name)

    return results


def assess_picking_exercise(
        annotation_file,
        lilypond_template_file,
        latency,
        student_filename,
        image_format='png',
        attack_color_func=attack_rgba):
    assessment_workflow = load_model(os.path.join(simmusic.__path__[0], 'extractors/guitar_models/picking_workflow.pkl'))
    return assess_guitar_exercise(
        annotation_file,
        lilypond_template_file,
        latency,
        student_filename,
        assessment_workflow,
        image_format = image_format,
        attack_color_func=attack_color_func)


def assess_monophonic_exercise(
        anno_file,
        lilypond_template_file,
        latency,
        student_filename,
        assessment_workflow,
        sample_rate=44100,
        image_format='png',
        attack_color_func=attack_rgba):
    audio = ess.MonoLoader(filename=student_filename)()
    frames = int(latency * sample_rate)
    audio = audio[frames:]
    audio_file = NamedTemporaryFile(suffix='.wav', delete=False)
    audio_file.close()
    os.unlink(audio_file.name)
    ess.MonoWriter(filename=audio_file.name, format='wav')(audio)
    chroma_scores = assessment_workflow.chroma_scores(anno_file, audio_file.name)
    timing_features = feature_extraction.timing_features(
        anno_file, audio_file.name,
        max_spectral_centroid=assessment_workflow.onset_max_spectral_centroid,
        onset_threshold=assessment_workflow.onset_threshold,
        series_delta=assessment_workflow.onset_series_delta)
    lilypond_basedir = os.path.dirname(lilypond_template_file)
    lilypond_shortname = os.path.basename(lilypond_template_file)
    img_file_name = visualize(
        lilypond_basedir,
        lilypond_shortname,
        timing_features['bars'],
        timing_features['events'],
        timing_features['onsets'],
        chroma_scores,
        audio,
        image_format=image_format,
        attack_color_func=attack_color_func)
    os.unlink(audio_file.name)

    timing_statistics = feature_extraction.timing_statistics(timing_features['devs'])
    timing_statistics.update(timing_features)
    chroma_statistics = feature_extraction.chroma_statistics(chroma_scores)
    X_tuning = [0]
    X_timing = [timing_statistics[f] for f in assessment_workflow.timing_feature_names]
    X_chroma = [chroma_statistics[f] for f in assessment_workflow.chroma_feature_names]
    X_overall = []
    X_overall.extend(X_tuning)
    X_overall.extend(X_timing)
    X_overall.extend(X_chroma)
    results = {}
    results["Rhythm"] = fool_proof_assess(assessment_workflow.rhythm_estimator, X_timing)
    results["Pitch"] = fool_proof_assess(assessment_workflow.chroma_estimator, X_chroma)
    results["Overall"] = fool_proof_assess(assessment_workflow.overall_estimator, X_overall)

    # hack, until we'll have enough balanced data to train the model
    results["Overall"] = max(results["Overall"], min( results["Rhythm"], results["Pitch"]))

    with open(img_file_name, "rb") as img_file:
        results["ImageBytes"] = img_file.read()
    os.unlink(img_file_name)

    return results


def assess_generic_monophonic_exercise(
        annotation_file,
        lilypond_template_file,
        latency,
        student_filename,
        image_format='png',
        attack_color_func=attack_rgba):
    assessment_workflow = load_model(os.path.join(simmusic.__path__[0], 'extractors/guitar_models/picking_workflow.pkl'))
    return assess_monophonic_exercise(
        annotation_file,
        lilypond_template_file,
        latency,
        student_filename,
        assessment_workflow,
        image_format = image_format,
        attack_color_func=attack_color_func)


def assess_strumming_exercise(
        annotation_file,
        lilypond_template_file,
        latency,
        student_filename,
        image_format='png',
        attack_color_func=attack_rgba):
    assessment_workflow = load_model(os.path.join(simmusic.__path__[0], 'extractors/guitar_models/strumming_workflow.pkl'))
    return assess_guitar_exercise(
        annotation_file,
        lilypond_template_file,
        latency,
        student_filename,
        assessment_workflow,
        image_format = image_format,
        attack_color_func=attack_color_func)



