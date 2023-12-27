import datasets
import pandas as pd

# Let's make a dummy dataframe with only one row and two columns, audio and transcript:
#             audio   transcript
# 0  audio/free.mp3  bla bla bla

df = pd.DataFrame(data={"audio": ["audio/free.mp3"], "transcript": ["bla bla bla"]})

# Now this dataframe will be converted to a dataset:
ds = datasets.Dataset.from_pandas(df)

# And finally, the column audio, which contains the path to audio file, can be
# cast to Audio, which means
ds = ds.cast_column("audio", datasets.Audio(sampling_rate=16_000, mono=True))

# Now the audio column looks like:
# [{'path': 'audio/free.mp3', 'array': array([ 0.00000000e+...0000e+00]), 'sampling_rate': 16000}]
# This can be then used for training/finetuning/eval...
