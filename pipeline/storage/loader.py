import json
import subprocess
from uuid import UUID

import psycopg
import boto3

from dotenv import load_dotenv

load_dotenv()

from config.config import config
from pipeline.schema import AudioAnalytic
from pipeline.schema.audio_metadata import AudioFileMetadata

s3_client = boto3.client(
    "s3",
    region_name=config.S3_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
)


class Loader:
    def __init__(self):
        self.conn_str = config.CONNECTION_STRING
        self.conn = None

    def __enter__(self):
        self.conn = psycopg.connect(self.conn_str)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f'{exc_type}: {exc_val}')
        if self.conn:
            self.conn.close()

        return False

    def get_or_create_audio_source(self, source_name: str) -> UUID:
        # try to find existing
        with self.conn.cursor() as cursor:
            cursor.execute('select id '
                           'from audio_sources '
                           'where audio_source_name = %s ',
                           (source_name,))

            row = cursor.fetchone()
            if row is not None:
                return row[0]
            # if not found, insert and return new id
            else:
                cursor.execute('insert into audio_sources '
                               '(audio_source_name) '
                               'values (%s) '
                               'returning id;',
                               (source_name,))
                new_id = cursor.fetchone()[0]
                self.conn.commit()
                return new_id

    def get_file_status(self, file_hash) -> str | None:
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT status '
                           'FROM audio_files '
                           'WHERE file_hash = %s', (file_hash,))
            row = cursor.fetchone()
            return row[0] if row else None

    def get_or_insert_audio_file(self, metadata: AudioFileMetadata):
        with self.conn.cursor() as cursor:
            cursor.execute('select id '
                           'from audio_files '
                           'where file_hash = %s ',
                           (metadata.file_hash,))

            row = cursor.fetchone()
            if row is not None:
                return row[0]
            # if not found, insert and return new id
            else:
                cursor.execute('insert into audio_files('
                               'file_path, file_name, file_size, file_hash,'
                               's3_key, s3_bucket,'
                               ' audio_source_id, duration_ms'
                               ') '
                               'values (%s, %s, %s, %s, %s, %s, %s, %s) '
                               'returning id;',
                               (metadata.file_path, metadata.file_name, metadata.file_size, metadata.file_hash,
                                metadata.s3_key, metadata.s3_bucket,
                                metadata.audio_source_id, metadata.duration_ms))
                new_id = cursor.fetchone()[0]
                self.conn.commit()

                return new_id

    def insert_audio_analytics(self, analytic: AudioAnalytic):
        with self.conn.cursor() as cursor:
            cursor.execute('insert into audio_analytics('
                           'audio_file_id, audio_source_id, snr_db,clipping_ratio,max_amplitude,dynamic_range,'
                           'signal_to_quantatization_ratio,band_energy_ratio,spectral_centroid_mean,zcr_std,zcr_mean,'
                           'silence_ratio,bandwith_mean,bandwith_std,source_type'
                           ') '
                           'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                           (analytic.audio_file_id, analytic.audio_source_id, analytic.snr_db, analytic.clipping_ratio,
                            analytic.max_amplitude, analytic.dynamic_range, analytic.signal_to_quantatization_ratio,
                            analytic.band_energy_ratio, analytic.spectral_centroid_mean, analytic.zcr_std,
                            analytic.zcr_mean, analytic.silence_ratio, analytic.bandwith_mean,
                            analytic.bandwith_std, analytic.source_type,))

            self.conn.commit()

    def bulk_insert_analytics(self, analytics: list[AudioAnalytic]):
        with self.conn.cursor() as cursor:
            with cursor.copy(
                    "COPY audio_analytics("
                    "audio_file_id,audio_source_id,hop_length,n_fft,n_mfcc,rms_energy,zcr,crest_factor,attack_time_ms,autocorr,"
                    "spectral_centroid,spectral_bandwidth,spectral_rolloff,spectral_flatness,spectral_flux,spectral_contrast,"
                    "mfcc,mfcc_mean,mfcc_variance,mel_stats_mean,mel_stats_std,chroma,tonnetz,tempo_bpm,tempo_confidence,beat_strength,"
                    "onset_density,snr_db,silence_ratio,clipping_ratio,dynamic_range_db,source_type"
                    ") FROM STDIN "
            ) as copy:
                for analytic in analytics:
                    copy.write_row((
                        analytic.audio_file_id, analytic.audio_source_id, config.HOP_LENGTH, config.N_FFT,
                        config.N_MFCC, json.dumps(analytic.rms_energy),
                        json.dumps(analytic.zcr), analytic.crest_factor, analytic.attack_time_ms, json.dumps(analytic.autocorr),
                        analytic.spectral_centroid, analytic.spectral_bandwidth, analytic.spectral_rolloff,
                        analytic.spectral_flatness,
                        json.dumps(analytic.spectral_flux), json.dumps(analytic.spectral_contrast), 
                        json.dumps(analytic.mfcc), json.dumps(analytic.mfcc_mean),
                        json.dumps(analytic.mfcc_variance),
                        json.dumps(analytic.mel_stats_mean), json.dumps(analytic.mel_stats_std), 
                        json.dumps(analytic.chroma), json.dumps(analytic.tonnetz),
                        analytic.tempo_bpm,
                        analytic.tempo_confidence, analytic.beat_strength, analytic.onset_density, analytic.snr_db,
                        analytic.silence_ratio,
                        analytic.clipping_ratio, analytic.dynamic_range_db, analytic.source_type,
                    ))
        self.conn.commit()

    def update_file_status(self, file_id: UUID, status: str, processed_at=None):
        with self.conn.cursor() as cursor:
            if processed_at:
                cursor.execute('UPDATE audio_files '
                               'SET status = %s, processed_at = %s '
                               'WHERE id = %s',
                               (status, processed_at, file_id))
            else:
                cursor.execute('UPDATE audio_files '
                               'SET status = %s '
                               'WHERE id = %s',
                               (status, file_id))

            self.conn.commit()
    def upload_to_s3(self,file_path: str, file_name: str) -> tuple[str, str]:
        bucket = config.S3_BUCKET
        s3_key = f"audio/raw/{file_name}"
        s3_client.upload_file(file_path, bucket, s3_key)
        return bucket, s3_key
    def preprocess_audio(self, input_path: str, output_path: str, duration_sec: int = config.DEFAULT_SAMPLE_DURATION_IN_SECONDS, sample_rate: int = config.DEFAULT_SAMPLE_RATE) -> str:
        """
        Normalize audio with ffmpeg:
        - Clip to max duration (take middle segment, more representative than start)
        - Convert to mono
        - Resample to target sr
        - Normalize to WAV
        """
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-ss", str(duration_sec // 4),   # start from quarter
            "-t", str(duration_sec),          # take N seconds
            "-ac", "1",                        # mono
            "-ar", str(sample_rate),          # resample
            "-acodec", "pcm_s16le",           # WAV PCM
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {result.stderr}")
        return output_path