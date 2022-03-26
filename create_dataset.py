from pydub import AudioSegment
import pandas as pd
import json
import os
import sys

"""
Given an audio file and syncamp.json file generate via aeneas, split the audio into smaller audio files
and create a csv mapping each file with its transcription.

USAGE:

python3 create_dataset.py --audio_file <path_to_audio.mp3> --syncmap <path_to_syncmap.json> --out_file <out_file.csv>

"""

def main(in_file, syncmap, out_file):
    if not os.path.isdir('./samples/'):
        os.makedirs('./samples/')
        print("Created folder : ", './samples/')
    else:
        print('./samples/', "Folder already exists. Exiting.")
        sys.exit()

    full_track = AudioSegment.from_mp3(in_file)
    with open(syncmap) as f: 
        syncmap = json.loads(f.read())

    sentences = []
    for fragment in syncmap['fragments']:
        duration = ((float(fragment['end'])*1000) - float(fragment['begin'])*1000)
        if duration > 400:
            sentences.append({'audio':full_track[float(fragment['begin'])*1000:float(fragment['end'])*1000], 'text':fragment['lines'][0], 'duration':duration})

    df = pd.DataFrame(columns=['filename','text','up_votes','down_votes','age','gender','accent','duration'])

    # export audio segment
    for idx, sentence in enumerate(sentences):
        text = sentence['text'].lower()
        sentence['audio'].export('./samples/sample-'+str(idx)+'.mp3', format='mp3')
        duration = sentence['duration']
        temp_df = pd.DataFrame([{'filename':'./samples/sample-'+str(idx)+'.mp3','text':text,'up_votes':0,'down_votes':0,'age':0,'gender':'male','accent':'','duration':duration}], columns=['filename','text','up_votes','down_votes','age','gender','accent','duration'])
        df = df.append(temp_df)

    df.to_csv(out_file,index=False)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--audio_file", type=str)
parser.add_argument("--syncmap", type=str)
parser.add_argument("--out_file", type=str)
args = parser.parse_args()
print(args)
main(args.audio_file, args.syncmap, args.out_file)






