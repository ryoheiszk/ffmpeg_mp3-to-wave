import os
import logging
import glob
import sys
from pydub import AudioSegment
from tqdm import tqdm
from convert_mp3_to_wav import convert_and_split
from asr_processor import process_asr
import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_directories():
    for directory in [settings.INPUT_DIR, settings.OUTPUT_DIR, settings.ASR_OUTPUT_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

def clean_output_directory():
    if settings.ENABLE_CONVERT:
        wav_files = glob.glob(os.path.join(settings.OUTPUT_DIR, "*.wav"))
        for file in wav_files:
            os.remove(file)
            logging.info(f"Removed existing WAV file: {file}")

def clean_asr_directory():
    txt_files = glob.glob(os.path.join(settings.ASR_OUTPUT_DIR, "*.txt"))
    for file in txt_files:
        os.remove(file)
        logging.info(f"Removed existing ASR output file: {file}")

def merge_mp3_files():
    mp3_files = glob.glob(os.path.join(settings.INPUT_DIR, "*.mp3"))
    if len(mp3_files) > 1:
        logging.info("Multiple MP3 files found. Merging...")
        combined = AudioSegment.empty()
        for mp3_file in tqdm(mp3_files, desc="Merging MP3 files"):
            audio = AudioSegment.from_mp3(mp3_file)
            combined += audio
        output_path = os.path.join(settings.INPUT_DIR, "merged_input.mp3")
        combined.export(output_path, format="mp3")
        logging.info(f"Merged MP3 file saved as: {output_path}")

        # Remove original MP3 files
        for mp3_file in mp3_files:
            os.remove(mp3_file)
            logging.info(f"Removed original MP3 file: {mp3_file}")

def main():
    setup_directories()

    if settings.ENABLE_CONVERT:
        clean_output_directory()
        merge_mp3_files()

        logging.info("Starting MP3 to WAV conversion process")
        convert_and_split()
    else:
        logging.info("Skipping MP3 to WAV conversion as per settings")

    if settings.ENABLE_ASR:
        clean_asr_directory()
        logging.info("Starting ASR processing")
        process_asr()
    else:
        logging.info("Skipping ASR processing as per settings")

    logging.info("All processes completed")
    sys.exit(0)

if __name__ == "__main__":
    main()
