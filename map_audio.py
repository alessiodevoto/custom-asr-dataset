from aeneas.executetask import ExecuteTask
from aeneas.task import Task
import sys

"""
Use aeneas to create a mapping between audio file and its transcription.

USAGE:

python3 map_audio.py --audio_file <path_to_audio_file.mp3> --text_file <path_to_txt_file.txt> --out_file <path_to_output_file.json>

--audio_file is the original track in .mp3 format.
--text_file is the transcription with a sentence for each row.
--out_file is the path to the output syncmap in json format.
"""

def main(audio_file, text_file, out_file):
	if not out_file.endswith('json'):
		print('Ouput file must be json')
		sys.exit()

	# create Task object
	config_string = "task_language=it|is_text_type=plain|os_task_file_format=json"
	task = Task(config_string=config_string)
	task.audio_file_path_absolute = audio_file
	task.text_file_path_absolute = text_file
	task.sync_map_file_path_absolute = out_file

	# process Task
	ExecuteTask(task).execute()
	# output sync map to file
	task.output_sync_map_file()

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--audio_file", type=str)
parser.add_argument("--text_file", type=str)
parser.add_argument("--out_file", type=str)
args = parser.parse_args()
print(args)

main(args.audio_file, args.text_file, args.out_file)