# HF_publication_demo
A brief proof-of-concept repo for publishing an audio dataset on HF hub.

This repo will use the results of [this SRT-to-CSV converter](https://github.com/niknah/SRT-to-CSV-and-audio-split/tree/master) that produces a directory called "ready_for_slice" with csv files. (For some reason, I do not get the promissed segmented audio output.)

## Data structure:

```
├── audio 
│   └── free.mp3
├── audio_segments
├── ready_for_slice
│   └── free.csv
├── 01_split_and_publish.py
├── README.md
└── requirements.txt
```
Put full length audio in `audio`. Put CSVs in `ready_for_slice`, with the same name. The `01_split_and_publish.py` script will populate `audio_segments`. Afterwards it can be deleted if not needed.


## Set up a new python environment

To be sure that the same versions of packages are used, I prepared a requirements.txt file. It's a good practice to create a new python environment to install the needed packages in. I list two options, one with pure python and another to use with conda/mamba:

### Pure python:

Use python>=3.10.

```bash
python -m venv .venv

# If you are on Windows:
.venv\Scripts\activate.bat

# If not:
source .venv/bin/activate

pip install -r requirements.txt
```


### Conda/mamba:

```bash
conda create -n hfpub python=3.11
conda activate hfpub
pip install -r requirements.txt
```

## Log in to huggingface

For publishing, we need to log in. Run
```bash
huggingface-cli login
```
and follow the instructions. You will need to get your token at https://huggingface.co/settings/tokens, and insert it. If you do not have any tokens yet, you can create a new one on the same website.
```

    _|    _|  _|    _|    _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|_|_|_|    _|_|      _|_|_|  _|_|_|_|
    _|    _|  _|    _|  _|        _|          _|    _|_|    _|  _|            _|        _|    _|  _|        _|
    _|_|_|_|  _|    _|  _|  _|_|  _|  _|_|    _|    _|  _|  _|  _|  _|_|      _|_|_|    _|_|_|_|  _|        _|_|_|
    _|    _|  _|    _|  _|    _|  _|    _|    _|    _|    _|_|  _|    _|      _|        _|    _|  _|        _|
    _|    _|    _|_|      _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|        _|    _|    _|_|_|  _|_|_|_|
    
    A token is already saved on your machine. Run `huggingface-cli whoami` to get more information or `huggingface-cli logout` if you want to log out.
    Setting a new token will erase the existing one.
    To login, `huggingface_hub` requires a token generated from https://huggingface.co/settings/tokens .
Token: (this is where you paste your token and press enter)
Add token as git credential? (Y/n) y
Token is valid (permission: write).
Your token has been saved in your configured git credential helpers (store).
Your token has been saved to /home/peter/.cache/huggingface/token
Login successful
```

## Start processing

I prepared one script that segments the audio and pushes results to HuggingFace.

First, let's create all the directories we need:
```bash
mkdir audio audio_segments ready_for_slice
```

Put the CSVs in `ready_for_slice` directory. Put the audio with the same name in `audio` (so free.csv should have free.mp3 or free.wav in the other directory).

Open `01_split_and_publish.py` and set your repo name (`TARGET_DATASET_NAME`). The rest of the paths should be OK, if you keep the same directory naming and structure.

Run 
```bash
python 01_split_and_publish.py
```

## Cleaning up

If you don't need the individual wav files, you can delete the whole audio_segments directory:

```bash
rm -r audio_segments
```