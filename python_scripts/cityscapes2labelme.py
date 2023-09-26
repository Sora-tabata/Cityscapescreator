
#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import glob
import json
import os
import os.path as osp
import numpy as np


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def deal_json(json_file):
    data_cs = {}
    objects = []
    num = -1
    num = num + 1
    if not json_file.endswith('.json'):
        print('Cannot generating dataset from:', json_file)
        return None
    
    with open(json_file) as f:
        print('Generating dataset from:', json_file)
        data = json.load(f)
        file_name = os.path.basename(json_file)
        file_name_without_gtFine = file_name.replace('_gtFine_polygons', '')  # 1. '_gtFine_polygons'を削除
        file_name_org = os.path.splitext(file_name_without_gtFine)[0]  # 拡張子を削除
        converted_json = {
            "version": "4.5.6",
            "flags": {},
            "shapes": [
                {
                    "label": data["objects"][0]["label"],
                    "points": data["objects"][0]["polygon"],
                    "group_id": None,
                    "shape_type": "polygon",
                    "flags": {}
                }
            ],
            "imagePath": file_name_org + "_leftImg8bit"+ ".png",
            "imageData": None,
            "imageHeight": data["imgHeight"],
            "imageWidth": data["imgWidth"],
            "vehicle": 1,
            "camera": 1
        }
        data_cs = converted_json
    return data_cs


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, )
    parser.add_argument('--json_input_dir', help='input annotated directory')
    parser.add_argument(
        '--output_dir',
        help='output dataset directory', )

    args = parser.parse_args()
    try:
        assert os.path.exists(args.json_input_dir)
    except AssertionError as e:
        print('The json folder does not exist!')
        os._exit(0)

    # Deal with the json files.
    total_num = len(glob.glob(osp.join(args.json_input_dir, '*.json')))
    for json_name in os.listdir(args.json_input_dir):
        data_cs = deal_json(osp.join(args.json_input_dir, json_name))
        if data_cs is None:
            continue
        json.dump(
            data_cs,
            open(osp.join(args.output_dir, json_name), 'w'),
            indent=4,
            cls=MyEncoder, )


if __name__ == '__main__':
    main()
