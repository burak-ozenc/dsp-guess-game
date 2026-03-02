from datetime import datetime
from pathlib import Path

from config.config import config
from pipeline.dsp.analyze import analyze_audio
from pipeline.ingestion.discover import discover_files
from pipeline.schema import AudioFileMetadata, AudioAnalytic
from pipeline.storage.loader import Loader


def process_audio_pipeline(source_dir: str):
    files = discover_files(source_dir, config.TOTAL_FILE_LIMIT_TO_PROCESS)
    analytics_batch = []

    with Loader() as loader:
        for file in files:
            try:
                print('Processing file: {}'.format(file['file_name']))
                status = loader.get_file_status(file['file_hash'])
                if status == 'completed':
                    continue
                source_type = Path(file['file_path']).parts[3]
                audio_source_id = loader.get_or_create_audio_source(source_type)
                bucket, s3_key = loader.upload_to_s3(file_path=file['file_path'], file_name=file['file_name'])
                # 1. insert file record, mark as processing
                print('Inserting audio file: {}'.format(file['file_name']))
                new_audio_file_id = loader.get_or_insert_audio_file(AudioFileMetadata(
                    file_path=file['file_path'],
                    file_name=file['file_name'],
                    file_size=file['file_size'],
                    file_hash=file['file_hash'],
                    audio_source_id=audio_source_id,
                    s3_key=s3_key,
                    s3_bucket=bucket,
                ))
                print('Updating audio file: {}'.format(file['file_name']))
                loader.update_file_status(file_id=new_audio_file_id, status='processing')

                # 2. run dsp analysis
                print('Analyzing audio file: {}'.format(file['file_name']))
                analysis = analyze_audio(file_path=file['file_path'])

                # add bulk insert for dsp analysis
                print('Adding to batch: {}'.format(file['file_name']))
                analytics_batch.append(
                    AudioAnalytic(
                        audio_source_id=audio_source_id,
                        audio_file_id=new_audio_file_id,

                        # Quality
                        snr_db=analysis.snr_db,
                        clipping_ratio=analysis.clipping_ratio,
                        dynamic_range_db=analysis.dynamic_range_db,  # corrected field name
                        silence_ratio=analysis.silence_ratio,

                        # Spectral
                        spectral_centroid=analysis.spectral_centroid,
                        spectral_rolloff=analysis.spectral_rolloff,
                        spectral_flatness=analysis.spectral_flatness,
                        spectral_bandwidth=analysis.spectral_bandwidth,
                        spectral_flux=analysis.spectral_flux,
                        spectral_contrast=analysis.spectral_contrast,

                        # Time Domain
                        rms_energy=analysis.rms_energy,
                        zcr=analysis.zcr,
                        crest_factor=analysis.crest_factor,
                        attack_time_ms=analysis.attack_time_ms,
                        autocorr=analysis.autocorr,

                        # Perceptual
                        mfcc=analysis.mfcc,
                        mfcc_mean=analysis.mfcc_mean,
                        mfcc_variance=analysis.mfcc_variance,
                        mel_stats_mean=analysis.mel_stats_mean,
                        mel_stats_std=analysis.mel_stats_std,
                        chroma=analysis.chroma,
                        tonnetz=analysis.tonnetz,

                        # Rhythm
                        tempo_bpm=analysis.tempo_bpm,
                        tempo_confidence=analysis.tempo_confidence,
                        beat_strength=analysis.beat_strength,
                        onset_density=analysis.onset_density,

                        # Metadata
                        hop_length=analysis.hop_length,
                        n_fft=analysis.n_fft,
                        n_mfcc=analysis.n_mfcc,
                        created_at=analysis.created_at,
                        source_type=source_type,
                    )
                )


                if len(analytics_batch) >= config.BULK_COPY_SIZE:
                    try:
                        print('Limit reached, bulk copy starting')
                        loader.bulk_insert_analytics(analytics_batch)
                        for analytic in analytics_batch:
                            loader.update_file_status(
                                file_id=analytic.audio_file_id,
                                status='completed',
                                processed_at=datetime.now()
                            )
                    except Exception as e:
                        print("Failed to bulk insert analytics: {}".format(e))
                        for analytic in analytics_batch:
                            loader.update_file_status(
                                file_id=analytic.audio_file_id,
                                status='failed'
                            )
                        
                    analytics_batch.clear()

                print("File processed {}".format(file['file_name']))

            except Exception as e:
                # mark as failed
                import traceback
                print("Error processing:", traceback.format_exc())
                print('Error occurred during processing file :' f'{file["file_path"]}')
                pass
        # flush remaining  analysis
        print('Inserting leftover batches')
        if analytics_batch:
            loader.bulk_insert_analytics(analytics_batch)
            for analytic in analytics_batch:
                loader.update_file_status(
                    file_id=analytic.audio_file_id,
                    status='completed',
                    processed_at=datetime.now()
                )


process_audio_pipeline(config.DATA_ROOT_PATH)