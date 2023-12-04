
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
from shapely.geometry import Polygon, MultiPolygon


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
    if not json_file.endswith('.json'):
        print('Cannot generating dataset from:', json_file)
        return None
    with open(json_file) as f:
        print('Generating dataset from:', json_file)
        data = json.load(f)
        data_cs['imgHeight'] = data['imageHeight']
        data_cs['imgWidth'] = data['imageWidth']
        
        # 画像全体をカバーするポリゴンを作成
        full_image_polygon = Polygon([(0, 0), (0, data_cs['imgHeight']), (data_cs['imgWidth'], data_cs['imgHeight']), (data_cs['imgWidth'], 0)])
        
        otherclass_polygon = full_image_polygon  # 初期値として画像全体のポリゴンを設定
        
        for shapes in data['shapes']:
            obj = {}
            label = shapes['label']
            obj['label'] = label
            points = shapes['points']
            p_type = shapes['shape_type']
            if p_type == 'polygon':
                obj['polygon'] = points
                objects.append(obj)  # 既存のラベル（SL, RAなど）の領域をそのまま保持
                
                # shapelyを使用してポリゴンオブジェクトを作成
                existing_polygon = Polygon(points)
                
                # 既存のポリゴン（SL, RAなど）を除去して、新しいポリゴン（otherclass）を更新
                otherclass_polygon = otherclass_polygon.difference(existing_polygon)
        
        # otherclassのポリゴンが複数の部分から構成されている場合、それぞれを個別に処理
        if isinstance(otherclass_polygon, MultiPolygon):
            otherclass_polygons = list(otherclass_polygon)
        else:
            otherclass_polygons = [otherclass_polygon]
        
        # 新しいshapeを作成してobjectsに追加
        for poly in otherclass_polygons:
            if poly.is_valid and not poly.is_empty:  # ポリゴンが有効かつ空でないことを確認
                otherclass_obj = {
                    "label": "otherclass",
                    "polygon": list(poly.exterior.coords)
                }
                objects.append(otherclass_obj)
        
        data_cs['objects'] = objects
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
            open(osp.join(args.output_dir, 'all_'+json_name), 'w'),
            indent=4,
            cls=MyEncoder, )


if __name__ == '__main__':
    main()
