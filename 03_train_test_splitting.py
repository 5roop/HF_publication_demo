from sklearn.model_selection import train_test_split
import pandas as pd
from pathlib import Path
from pydub import AudioSegment
import logging
import datasets


CSV_PATH = "dataframe.csv"
HF_DATASET_NAME = "5roop/brisi2"
train_proportion = 0.8
test_proportion = 0.1
dev_proportion = 0.1


# Let's load the csv we prepared in 01:

df = pd.read_csv(CSV_PATH)

# Let's calculate how many instance we need in each split:
N = df.shape[0]
train_N = int(
    N * train_proportion / (train_proportion + test_proportion + dev_proportion)
)
test_N = int(
    N * test_proportion / (train_proportion + test_proportion + dev_proportion)
)
dev_N = int(N * dev_proportion / (train_proportion + test_proportion + dev_proportion))

# Let's construct train-test-dev splits:
train, devtest = train_test_split(df, train_size=train_N)
dev, test = train_test_split(devtest, test_size=test_N)


# Let's transform these dataframes to datasets:
train = datasets.Dataset.from_pandas(train).cast_column(
    "audio", datasets.Audio(sampling_rate=16_000, mono=True)
)
dev = datasets.Dataset.from_pandas(dev).cast_column(
    "audio", datasets.Audio(sampling_rate=16_000, mono=True)
)
test = datasets.Dataset.from_pandas(test).cast_column(
    "audio", datasets.Audio(sampling_rate=16_000, mono=True)
)


# Now let's join them together and push to huggingface:
ds = datasets.DatasetDict({"train": train, "dev": dev, "test": test})
ds.push_to_hub(HF_DATASET_NAME)

# Just for fun, let's save the dataset to disk:
ds.save_to_disk("my_dataset")

# and now we can load it with:
datasets.DatasetDict.load_from_disk("my_dataset")
