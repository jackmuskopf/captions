import os
import uuid
import logging
import wave
import shutil
import moviepy.editor
import subprocess

logger = logging.getLogger()

DATA_PATH = "/mnt"
INPUT_PATH = os.path.join(DATA_PATH, 'input')
OUTPUT_PATH = os.path.join(DATA_PATH, 'output')
MODEL_DIR = 'models'

def main():

    for file in os.listdir(INPUT_PATH):

        if file == '.gitignore':
            continue

        fpath = os.path.join(INPUT_PATH, file)
        name = file.split(".")[0]

        logger.info(f'Converting {file} to audio')

        clip = moviepy.editor.VideoFileClip(fpath)
        audio_name = f'{name}.wav'
        audio_path = os.path.join(OUTPUT_PATH, audio_name)

        clip.audio.write_audiofile(audio_path)

        logger.info(f'Running deepspeech on {audio_path}')

        output = subprocess.check_output([
            'deepspeech', 
            '--model', 'deepspeech-0.9.3-models.pbmm', 
            '--scorer', 'deepspeech-0.9.3-models.scorer',
            '--audio', audio_path
        ]).decode('utf-8')

        tokens = output.split(' ')
        n_per_line = 10
        formatted = "\n".join([
            " ".join(line)
            for line in map(
                lambda ix: tokens[ix*n_per_line:(ix+1)*n_per_line],
                range(len(tokens)//n_per_line + 1)
            )
        ])

        list(map(logger.info, formatted.split('\n')))

        with open(os.path.join(OUTPUT_PATH, f'{name}-out.txt'), 'w') as f:
            f.write(formatted)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()