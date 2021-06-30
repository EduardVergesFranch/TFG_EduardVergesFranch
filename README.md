# TFG_EduardVergesFranch
Repository to store code and results realted to TFG

# Introduction
This repository contains the database and codes developed by Eduard Vergés Franch in his final degree project.

*The aim of this project is to contribute to the development of a music transcription system of guitar performances in the context of music education. Using the Music Critic system as a baseline we identified aspects to improve and then we implemented and tested our contributions. We show how the system reacts to different contextual variations and discuss possible repercussions on a real context application. Also, we studied how the model used behaves using different training conditions. Furthermore,  the \textit{Five Guitar dataset}, with 90 guitar recordings, is designed especially for this project and publicly available. We use a data augmentation strategy to obtain a higher number of recordings simulating different rooms, mics, effects and recording setups. We observe that room acoustics and recording setup could generate biases on the final performance of the model and that the system is consistent according to timber. Also, we discover the need of representing all the pitch-class sets into the training set, which could be a limitation in a real situation, plus a high bias in the model.*

Its main contribution is the creation of the **Five Guitar Dataset** and a series of codes to perform data augmentation and obtain a large number of recordings.
# Datasets
This project has two dataset inside:
* Impulse responses dataset, that could be downloaded in the link provided inside Databases/IR/ repository.
* The Five Guitar Dataset,inside Database/Raw_database/ repository, that can be found in Zenodo.

The process for obtaining the complete dataset is first two download the previous two datasets and paste its content inside the correspondend folders. Then, sequentially run the *Build_Augmented_dataset.ipynb* and *Renaming_files.ipynb* notebooks found inside Code/ repository.

After doing all this steps, all the data used for the project would be disponible.

**Download links**
Impulse responses: https://drive.google.com/file/d/1F37HKCLSSQfanLZT-jxTR8xCCTjqtPM2/view?usp=sharing
Five Guitar Dataset: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4988354.svg)](https://doi.org/10.5281/zenodo.4988354)


# Codes and Report
The notebooks that contain *Experiments* in its file name, are the ones which correspond to the different experiments done in the **Experiments and Results** chapter found in the report conatined inside REPORT/ repository.

# Reproducibility

The project makes use of a private python library and dataset, property of Music Technology Group in Universitat Pompeu Fabra. Hence, to reproduce the results you would need access to it.
