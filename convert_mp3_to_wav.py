import os
import subprocess
import logging
from pydub import AudioSegment
import settings

def convert_mp3_to_wav(input_file, output_file):
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-acodec', 'pcm_s16le',
        '-ac', '1',
        '-ar', '16000',
        output_file
    ])

    audio = AudioSegment.from_wav(output_file)
    logging.info(f"Converted file: {output_file}")
    logging.info(f"Channels: {audio.channels}")
    logging.info(f"Sample width: {audio.sample_width * 8} bits")
    logging.info(f"Frame rate: {audio.frame_rate} Hz")
    logging.info(f"Duration: {len(audio) / 1000} seconds")
    return audio

def split_audio(audio, output_dir, base_name, split_duration):
    total_duration = len(audio)
    split_count = 0
    for i in range(0, total_duration, split_duration * 1000):
        start = i
        end = min(i + split_duration * 1000, total_duration)
        split = audio[start:end]
        split_file = os.path.join(output_dir, f"{base_name}_{split_count:03d}_{start//1000}_{end//1000}.wav")
        split.export(split_file, format="wav")
        logging.info(f"Created split file: {split_file}")
        split_count += 1

def convert_and_split():
    for filename in os.listdir(settings.INPUT_DIR):
        if filename.endswith('.mp3'):
            input_path = os.path.join(settings.INPUT_DIR, filename)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(settings.OUTPUT_DIR, f"{base_name}.wav")

            audio = convert_mp3_to_wav(input_path, output_path)

            if settings.SPLIT_DURATION > 0:
                logging.info(f"Splitting audio into {settings.SPLIT_DURATION} second segments")
                split_audio(audio, settings.OUTPUT_DIR, base_name, settings.SPLIT_DURATION)
                os.remove(output_path)  # 元のWAVファイルを削除
            else:
                logging.info(f"No splitting requested. Full WAV file saved: {output_path}")
