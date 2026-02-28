# DSP - Guess The Sound Source Game
Purpose is to guess the source type from given analytics, based on time, spectral, perceptual, rhythm and quality features of already processes audios.

## Overview:
- to create an ETL pipeline and run
- extract and analyze basic DSP features with Librosa and Numpy from a sample music-speech-noise dataset from [MUSAN](https://openslr.org/17),
- gamify the process

## ETL Flow
```
 1- INGEST 	- discover '*.wav' files within given data path, hash an return the file[] 
 2- ANALYZE - load the audio files from path, apply basic DSP analyses over them
 3- LABEL 	- extract speech confidence using Silero VAD, and label audio files
 4- PERSIST - persist the data to PostgreSQL using bulk COPY inserts
```


## Schema Design Decisions
- file_hash based idempotency: file paths break when data moves, hashes don''t. re-running the pipeline on the same dataset is safe
- since we are using already pre-defined sets by MUSAN, it makes more sense to create partition by source type
- audio_analytics partitioned by source_type: queries almost always filter by source category. partition pruning eliminates irrelevant partitions without touching indexes
- used bulk COPY due to performance improvements







## Setup
- Download the dataset from [MUSAN](https://openslr.org/17)
- Create a data folder in project, and unzip the dataset to this folder
- Create an .env file and set env variables
```
cp .env.example .env
```
- To install Prefect, follow the docs [here](https://docs.prefect.io/v3/get-started/quickstart)
- Just run the flow:
```
python -m pipeline.flow
```