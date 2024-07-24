import os
import logging
from convert_mp3_to_wav import ENABLE_SPLIT
from asr_processor import process_asr
import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_directories():
    for directory in [settings.INPUT_DIR, settings.OUTPUT_DIR, settings.ASR_OUTPUT_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

def main():
    setup_directories()

    if settings.ENABLE_SPLIT:
        logging.info("Starting MP3 to WAV conversion and splitting process")
        ENABLE_SPLIT()
    else:
        logging.info("Skipping MP3 to WAV conversion and splitting as per settings")

    if settings.ENABLE_ASR:
        logging.info("Starting ASR processing")
        process_asr()
    else:
        logging.info("Skipping ASR processing as per settings")

    logging.info("All processes completed")

if __name__ == "__main__":
    main()
