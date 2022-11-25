# MachineTranslation
A machine translation model based on OpenNMT


## Task description

Train your own Polish-English machine translation system, and compare its quality with the one from HuggingFace (https://huggingface.co/models). You have to create the parallel corpus of pairs of sentences from these languages, choose the architecture (consider using OpenNMT), and train the model.

You can use any data to train the model. Consider the following sources:

http://2019.poleval.pl/index.php/tasks/task4 
tatoeba.org
https://clarin-pl.eu/index.php/zasoby/
Our main objective is to obtain the Polish versions of the following dialog corpora:

[1] https://paperswithcode.com/dataset/dailydialog

[2] https://github.com/facebookresearch/EmpatheticDialogues

[3] https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html

Teams doing this task are kindly asked to prepare translation of some parts of corpora [1], [2], [3] (using Google Translate and DeepL APIs). Part of this mini-corpus will be used as additional training data, part of this corpus will be used as a test set.

## Collecting resources

We used LRT-2610 a parallel corpora containing about one million sentences. Training on a whole dataset wasn't too successful, as the data was pretty messy, therefore we trimmed it with some heuristics. All of them can be found in a notebook: machine_translation/corpora_pol_en/LRT-2610/generate.ipynb

## Model

As main framework we used a OpenNMT - neural machine translation project from MIT (https://github.com/OpenNMT/OpenNMT-py). It provided a simple technic to choose and train the model. Architecture that we tested was a LSTM network.

## Results

We compared quality of our model with DeepL, Google Translate and one on HuggingFace. We chose BLEU, NIST and METEOR were metrics that we were evaluating.

![plot](https://raw.githubusercontent.com/AntoniDabrowski/MachineTranslation/main/machine_translation/machine_translation_model/results/Comparison.png)