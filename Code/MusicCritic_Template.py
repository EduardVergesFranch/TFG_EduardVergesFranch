
from pychord_tools.models import load_model
import simmusic

import simmusic.extractors.guitar as guitar

import sys
sys.path.append('./')
sys.path.append('./test_code/test_utils/models/')
sys.path.append('./test_code/test_utils/')

from test_utils.training_individual_chord_model import *

from test_utils.test_functionality import GenericWorkflow


if __name__ == "__main__":
    assessment_workflow = load_model(os.path.join(simmusic.__path__[0], 'extractors/guitar_models/picking_workflow.pkl'))
    hacked_workflow = GenericWorkflow(
        assessment_workflow.tuning_estimator,
        assessment_workflow.rhythm_estimator,
        assessment_workflow.chroma_estimator,
        assessment_workflow.overall_estimator,
        assessment_workflow.tuning_feature_names,
        assessment_workflow.timing_feature_names,
        assessment_workflow.chroma_feature_names,
        onset_series_delta=0.22)


    json = 'test_data/Mountain At My Gates/Mountain At My Gates.json' #json annotation
    lily = 'test_data/Mountain At My Gates/Mountain At My Gates.ly' #lilypond annotation
    target_audio = './test_data/Mountain At My Gates/3_gtrX_Mountain At My Gates_Foals_Gtr Gr0.wav' #student recording

    results = guitar.assess_guitar_exercise(json, lily, 0.0, target_audio,
                                            assessment_workflow= hacked_workflow,
                                            image_format='pdf')

    # print the results and save resulting pdf to desired path
    store_path  = "./Code/model_naive_testing_results/Mountain_Thirds.pdf"
    with open(store_path, "wb") as out_file:
        out_file.write(results["ImageBytes"])
    print('Overall:', results['Overall'])
    print('Rhythm:', results['Rhythm'])
    print('Tuning:', results['Tuning'])
    print('Pitch:', results['Pitch'])

