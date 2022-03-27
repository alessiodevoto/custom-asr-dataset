# Custom-asr-dataset
This repo shows how to create a custom dataset for automatic speech recognition, if you have at your disposal:
- an audio track with human utterings (an .mp3 file). 
- the transcription of the track (a .txt file).

Before starting, please make sure that the transcription is correct and possibly the audio file only contains the transcription and not also other voices/conversation/music. Also, the audio file should be encoded with a non-variable bitrate. If this is not the case, you can easily change it with any audio editing tool. 

The process consists in the following steps:

1. Edit the transcription file by substituting unwanted or out-of-vocabulary characters. 
2. Edit the transcription file by splitting it in sentences, one for each line. Each sentence will later be a sample of our custom dataset.
3. Generate the syncmap, that is a mapping between sentences and the time where they are found in the audio.
4. Fine tune (manually) the syncmap to check that audio and transcript are actually synced.
5. Generate dataset in csv format.
5. Use validation to (manually) double check and eliminate unwanted samples.

## Steps 1 & 2
Steps 1 and 2 are done at the same time, using 

```
python3 normalize.py --in_file <transcription.txt> --remove_lines 'line1;line2;...;lineN'

``` 
where 
- ` --in_file`  -> raw transcription in txt file
- ` --remove_lines`  -> (optional) list of lines, separated by ';' that should be removed from transcription (example name of peoples spaking)
- ` --sentence_min_len`  -> (optional) minimum words for generated sentences

once the output file is generated (this will be a .txt file with name = <original_name>-out.txt), you should check that generated rows are fine, keeping in mind that each row will be a sample in the final dataset. You can manually edit this file.

## Step 3
To generate the syncmap, we use aeneas (pip install aeneas). Run:
```
python3 map_audio.py --audio_file <path_to_audio_file.mp3> --text_file <path_to_txt_file.txt> 
```
where
- `--audio_file` is the original track in .mp3 format.
- `--text_file` is the transcription with a sentence for each row.
- `--out_file` -> (optional) is the path to the output syncmap in json format. Default: `syncmap.json`.

## Step 4
Once you have generated a syncmap, you can use this tool: to check if transcriptions are well adjusted. 
Just donwload it locally and open the file `finetuneaeneas.html` in any browser. Follow  instructions provided 
to generate a fine-tuned `syncmap.json`.

## Step 5
In order to generate our final dataset, we just need to run:

```
python3 create_dataset.py --audio_file <path_to_audio.mp3> --syncmap <path_to_syncmap.json> --out_dir <path_to_out_dir>
```

Output of this command, stored in `out_dir`, will be a .csv file plus a subdirectory where all audio files will be saved.

## Step 6 (only on colab / notebook so far)
Use the notebook in `validate.ypn`. You just need to provide the path to dataset directory and
validate all the dataset sample by sample. 





