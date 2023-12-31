import json

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


# 与えられたJSONデータ
def deal_json(json_file):
    num = -1
    num = num + 1
    if not json_file.endswith('.json'):
        print('Cannot generating dataset from:', json_file)
        return None
    
    with open(json_file) as f:
        print('Generating dataset from:', json_file)
        data = json.load(f)
    # 並べ替える順序（逆順に設定）
        order = [
            "straight left arrow",
            "straight right arrow",
            "right arrow",
            "left arrow",
            "straight arrow",
            "ego vehicle",
            "rectification border",
            "out of roi"
        ]

        # objectsを指定された順序で並べ替え
        data["objects"].sort(key=lambda x: order.index(x['label']) if x['label'] in order else -1)

    return data



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
