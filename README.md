---
title: DSP Guess The Sound Source
emoji: 🎵
colorFrom: purple
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# DSP - Guess The Sound Source Game
Purpose is to guess the source sound type(music, noise, speech) from given analytics, based on time, spectral, perceptual, rhythm and quality features of already processes audios.

## Overview:
- to create an ETL pipeline and run
- preprocess tha raw data
- create samples with sample rate to 16000, duration to 30 and extract features w Numpy & Librosa
- persist it to PostgresQL
- map features to UI

## Setup
- Download the dataset from [MUSAN](https://openslr.org/17)
- Create a data folder in project, and unzip the dataset to this folder
- Create an .env file and set env variables
```
cp .env.example .env
```
- Run backend
```
uvicorn backend.main:app --reload --port 8000
```