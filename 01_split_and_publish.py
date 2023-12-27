import pandas as pd
from pathlib import Path
from pydub import AudioSegment
import logging
import datasets

logging.basicConfig(level=logging.INFO)


# Set these directories and names to match your setup
TARGET_DATASET_NAME = "5roop/brisi"  # This is your repo name, under which dataset will be available on huggingface
CSV_DIR = Path("./ready_for_slice")  # Should contain csvs
AUDIO_DIR = Path("./audio")  # Should contain full length audio
SEGMENT_DIR = Path("./audio_segments")  # Should exist
DATAFRAME_PATH = Path("./dataframe.csv")


logging.info(f"Dataset will be published to huggingface repo {TARGET_DATASET_NAME}")
files_to_process = list(CSV_DIR.glob("*.csv"))
logging.info(f"Found the following csv files: {[i.name for i in files_to_process]}")
if not files_to_process:
    logging.critical(f"No files were found in {CSV_DIR.absolute()=}!")

logging.info("Splitting and converting audio...")
for file in files_to_process:
    # Test if audio file exists:
    root_name = file.with_suffix("").name
    audio_path = list(AUDIO_DIR.glob(f"{root_name}.*"))[0]
    if not audio_path.exists():
        logging.critical(f"Could not find audio files for {file.name}")
    else:
        logging.info(f"Found an audio file: {audio_path.name}")
    df = pd.read_csv(file)
    audio_segment = AudioSegment.from_file(str(audio_path))

    for i, row in df.iterrows():
        segment_path = SEGMENT_DIR / (row["id"] + ".wav")
        segment = audio_segment[int(row["start_times"]) : int(row["end_times"])]
        segment.export(
            str(segment_path),
            format="wav",
            parameters=["-ac", "1", "-acodec", "pcm_s16le", "-ar", "16000"],
        )


dfs = []
for file in files_to_process:
    # Test if audio file exists:
    root_name = file.with_suffix("").name
    audio_path = list(AUDIO_DIR.glob(f"{root_name}.*"))[0]
    if not audio_path.exists():
        logging.critical(f"Could not find audio files for {file.name}")
    else:
        logging.info(f"Found an audio file: {audio_path.name}")
    df = pd.read_csv(file)
    df["audio"] = df["id"].apply(lambda s: str(SEGMENT_DIR / f"{s}.wav"))
    assert df.audio.apply(
        lambda s: Path(s).exists()
    ).all(), "Some segment files do not exist!"
    dfs.append(df[["id", "audio", "transcript"]])
df = pd.concat(dfs).reset_index(drop=True)


# This is the fun part. df is a DataFrame with columns id, audio, and transcript.
# We will convert it to a dataset:
ds = datasets.Dataset.from_pandas(df)

# Before the column audio was just a string, telling us where the data can be found.
# We will cast the column to audio, meaning that the file will be read and entries will be
# a huggingface representation of the audio. At the same time, we will specify
# sampling rate and number of channels:
ds = ds.cast_column("audio", datasets.Audio(sampling_rate=16_000, mono=True))


# Now we publish the dataset to HuggingFace dataset hub under TARGET_DATASET_NAME:
logging.info("Pushing to HuggingFace:")
ds.push_to_hub(repo_id=TARGET_DATASET_NAME)

# And finally, let's export the dataframe to csv for our use locally:
df.to_csv(DATAFRAME_PATH, index=False)
