import os

# Process flow control
ENABLE_CONVERT = True
SPLIT_DURATION = 100  # in seconds, 0 for no splitting
ENABLE_ASR = True

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
