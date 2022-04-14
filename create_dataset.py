from pydub import AudioSegment
import pandas as pd
import json
import os
from os.path import basename
import os.path as osp
import sys
from pathlib import Path


"""
Given an audio file and syncamp.json file generate via aeneas, split the audio into smaller audio files
and create a csv mapping each file with its transcription.

USAGE:

python3 create_dataset.py --audio_file <path_to_audio.mp3> --syncmap <path_to_syncmap.json> --out_file <out_file.csv>

"""



def main(in_file, syncmap, out_dir):
    dataset_name = basename(in_file).split('.')[0]
    
    samples_dir = 'samples_' + dataset_name
    samples_dir_path = osp.join(out_dir, samples_dir)
    generic_sample_path = osp.join(samples_dir_path, dataset_name+'_sample')
    generic_sample_relative_path = osp.join('./', samples_dir, dataset_name+'_sample')

    print(samples_dir)
    print(samples_dir_path)
    print(generic_sample_path)
    print(generic_sample_relative_path)


    Path(samples_dir_path).mkdir(parents=True, exist_ok=True)

    full_track = AudioSegment.from_mp3(in_file)
    with open(syncmap) as f: 
        syncmap = json.loads(f.read())

    sentences = []
    for fragment in syncmap['fragments']:
        duration = ((float(fragment['end'])*1000) - float(fragment['begin'])*1000)
        if duration > 400:
            sentences.append({'audio':full_track[float(fragment['begin'])*1000:float(fragment['end'])*1000], 'text':fragment['lines'][0], 'duration':duration})

    df = pd.DataFrame(columns=['path','sentence','up_votes','down_votes','age', 'client_id', 'gender', 'locale', 'accent','duration', 'segment'])

    # export audio segment
    for idx, sentence in enumerate(sentences):
        text = sentence['text'].lower()
        sentence['audio'].export(generic_sample_path+'-'+str(idx)+'.mp3', format='mp3')
        duration = sentence['duration']
        temp_df = pd.DataFrame([{'path':generic_sample_relative_path+'-'+str(idx)+'.mp3','path':text, 'client_id':'', 'locale':'', 'segment':0, 'up_votes':0,'down_votes':0,'age':0,'gender':'','accent':'','duration':duration}], columns=['path','sentence','up_votes','down_votes','age', 'client_id', 'gender', 'locale', 'accent','duration', 'segment'])
        df = df.append(temp_df)

    df.to_csv(osp.join(out_dir,dataset_name+'.csv'),index=False)
    
 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--audio_file", type=str)
parser.add_argument("--syncmap", type=str)
parser.add_argument("--out_dir", type=str)
args = parser.parse_args()
print(args)
main(args.audio_file, args.syncmap, args.out_dir)






