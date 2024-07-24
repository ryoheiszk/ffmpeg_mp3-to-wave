import os

# Process flow control
ENABLE_SPLIT = True  # True to convert MP3 to WAV and split
SPLIT_DURATION = 300  # in seconds, 0 for no splitting
ENABLE_ASR = True  # True to perform ASR on WAV files

# ASR settings
ASR_URL = os.environ.get('ASR_URL')
TEMPERATURE = '0.0'
TEMPERATURE_INC = '0.2'
RESPONSE_FORMAT = 'json'
LANGUAGE = 'en'

# File paths
INPUT_DIR = '/app/input'
OUTPUT_DIR = '/app/output'
ASR_OUTPUT_DIR = '/app/asr'
