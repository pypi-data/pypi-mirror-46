import os

from cr_download.configuration import data as config
from cr_download.autocut import autocutter


TEST_FILENAME = "test*.mp3"
WAVFILE_DIR = "wav_files"

TEST_DIR = os.path.dirname(__file__)

wav_dir = os.path.join(TEST_DIR, WAVFILE_DIR)
output_file = os.path.join(TEST_DIR, TEST_FILENAME)

wav_files = [os.path.join(wav_dir, wavfile)
             for wavfile in sorted(os.listdir(wav_dir))]

config.cutting_sequence = None
autocutter.autocut(wav_files, output_file)
