# HF_publication_demo
A brief proof-of-concept repo for publishing an audio dataset on HF hub.

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