#!/bin/bash
python python_scripts/change_jsonorder.py --json_input_dir /media/sora/SanDisk/cityscapes_1002/gtFine/val/frankfurt/ --output_dir /media/sora/SanDisk/cityscapes_1002/gtFine/val/frankfurt/
python python_scripts/change_jsonorder.py --json_input_dir /media/sora/SanDisk/cityscapes_1002/gtFine/train/bochum/ --output_dir /media/sora/SanDisk/cityscapes_1002/gtFine/train/bochum/
python python_scripts/change_jsonorder.py --json_input_dir /media/sora/SanDisk/cityscapes_1002/gtFine/train/darmstadt/ --output_dir /media/sora/SanDisk/cityscapes_1002/gtFine/train/darmstadt/
