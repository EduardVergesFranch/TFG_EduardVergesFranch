# TFG_EduardVergesFranch
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

# Introduction
This repository contains the database and codes developed by Eduard Vergés Franch in his final degree project, in the course 2020/2021.

*The aim of this project is to contribute to the development of a music transcription system of guitar performances in the context of music education. Using the Music Critic system as a baseline we identified aspects to improve and then we implemented and tested our contributions. We show how the system reacts to different contextual variations and discuss possible repercussions on a real context application. Also, we studied how the model used behaves using different training conditions. Furthermore,  the *Five Guitar dataset*, with 90 guitar recordings, is designed especially for this project and publicly available. We use a data augmentation strategy to obtain a higher number of recordings simulating different rooms, mics, effects and recording setups. We observe that room acoustics and recording setup could generate biases on the final performance of the model and that the system is consistent according to timber. Also, we discover the need of representing all the pitch-class sets into the training set, which could be a limitation in a real situation, plus a high bias in the model.*

# Datasets
This project has two datasets inside:

* Impulse responses dataset, that could be downloaded in the link provided inside *Databases/IR/* repository.
* The Five Guitar Dataset,inside *Database/Raw_database/* repository, that can be found in Zenodo.

The process for obtaining the complete dataset is first two download the previous two datasets and paste its content inside the correspondend folders. Then, sequentially run the *Build_Augmented_dataset.ipynb* and *Renaming_files.ipynb* notebooks found inside *Code/* repository.

After doing all this steps, all the data used for the project would be disponible.

# Steps to run the code

* 1. Download the datasets in previous section.
* 2. Run *Build_Augmented_dataset.ipynb* and *Renaming_files.ipynb* notebooks found inside *Code/* repository.
* 3. Run the *Experiments* notebooks inside *Code/* repository.

**Download links**

Impulse responses: https://drive.google.com/file/d/1F37HKCLSSQfanLZT-jxTR8xCCTjqtPM2/view?usp=sharing

Five Guitar Dataset: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4988354.svg)](https://doi.org/10.5281/zenodo.4988354)


# Codes and Report
The notebooks inside *Code/* repository that contain *Experiments* in its file name, are the ones which correspond to the different sections in the **Experiments and Results** chapter found in the report conatined inside REPORT/ repository.

# Reproducibility

The project makes use of a private python library and little dataset (refered as *Basic Guitar dataset* in the report*), property of Music Technology Group in Universitat Pompeu Fabra. Hence, to reproduce the results you would need access to it.

# Dependencies

This project has a high number of dependencies. A part from the private MTG python library, it also makes use of:
* 1. Python version 3.6.8
* 2. pip install sox
* 3. pip install essentia
* 4. All the requirements used by MTG private library.
