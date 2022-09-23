import torch
from torch.utils.data import Dataset
import subprocess
import pandas as pd
import zipfile
import os

def download_extract_dataset(dest_dir, gdrive_id):
    """
    dest_dir:
    gdrive_id:
    """
    print(f"Downloading dataset to {dest_dir}")
    FILE_ID = gdrive_id
    OUT_FILE = "data.zip"

    os.makedirs(dest_dir, exist_ok=True)
    bashCommand = f"""wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id={FILE_ID}' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\\1\\n/p')&id={FILE_ID}" -O {OUT_FILE} && rm -rf /tmp/cookies.txt"""
    output = subprocess.check_output(''.join(bashCommand), shell=True)

    print('Extracting dataset...')
    with zipfile.ZipFile(OUT_FILE, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)

    print("Cleaning...")
    os.system(f'rm -rf {OUT_FILE}')

class TvShowIt(Dataset):
    """
    Dataset description.
    This is really basic, just for quick testing.
    """
    GDRIVE_ID = "1r3oB6l3iRpjZi00YD7811m2isD3LKmX5"

    def __init__(self, root):
        """
        Args:
            root: 
        """
        self.root=root
        self.csv_file = os.path.join(self.root, 'tvshow_dataset_it/validated_filepaths.csv')
        if not os.path.exists(self.csv_file):
            download_extract_dataset(root, gdrive_id=self.GDRIVE_ID)
        self.dataframe = pd.read_csv(self.csv_file)
        
        
    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        audio_path = os.path.join(self.root, self.dataframe.iloc[idx]['path'])
        transcription = self.dataframe.iloc[idx]['sentence']
        sample = {'path': audio_path, 'transcription': transcription}

        return sample