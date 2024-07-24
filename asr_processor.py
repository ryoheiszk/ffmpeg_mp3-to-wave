import os
import requests
import json
import logging
from tqdm import tqdm
import settings

def process_wav_file(file_path):
    with open(file_path, 'rb') as audio_file:
        files = {'file': audio_file}
        data = {
            'temperature': settings.TEMPERATURE,
            'temperature_inc': settings.TEMPERATURE_INC,
            'response_format': settings.RESPONSE_FORMAT,
            'language': settings.LANGUAGE
        }
        response = requests.post(settings.ASR_URL, files=files, data=data)

    if response.status_code == 200:
        return response.json()['text']
    else:
        logging.error(f"Error processing file {file_path}: {response.status_code}")
        return None

def process_asr():
    output_file = os.path.join(settings.ASR_OUTPUT_DIR, 'asr_output.txt')

    wav_files = sorted([f for f in os.listdir(settings.OUTPUT_DIR) if f.endswith('.wav')])

    with open(output_file, 'w') as out_file:
        for wav_file in tqdm(wav_files, desc="Processing WAV files"):
            file_path = os.path.join(settings.OUTPUT_DIR, wav_file)
            asr_result = process_wav_file(file_path)
            if asr_result:
                out_file.write(f"File: {wav_file}\n")
                out_file.write(f"{asr_result}\n\n")

    logging.info(f"ASR processing complete. Output saved to {output_file}")
