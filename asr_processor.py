import os
import requests
import re
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
    wav_files = sorted([f for f in os.listdir(settings.OUTPUT_DIR) if f.endswith('.wav')],
                       key=lambda x: int(re.search(r'_(\d{3})_', x).group(1)))
    combined_output = []

    for wav_file in tqdm(wav_files, desc="Processing WAV files"):
        file_path = os.path.join(settings.OUTPUT_DIR, wav_file)
        asr_result = process_wav_file(file_path)

        if asr_result:
            # Individual file output
            base_name = os.path.splitext(wav_file)[0]
            individual_output_file = os.path.join(settings.ASR_OUTPUT_DIR, f"{base_name}_asr.txt")
            with open(individual_output_file, 'w') as ind_file:
                ind_file.write(asr_result)
            logging.info(f"ASR result saved to {individual_output_file}")

            # Append to combined output
            combined_output.append(f"File: {wav_file}\n{asr_result}\n\n")

    # Write combined output
    combined_output_file = os.path.join(settings.ASR_OUTPUT_DIR, 'asr_output.txt')
    with open(combined_output_file, 'w') as comb_file:
        comb_file.writelines(combined_output)
    logging.info(f"Combined ASR output saved to {combined_output_file}")

    logging.info("ASR processing complete.")
