import os
import shutil

scr_folder = "/home/sora/datasets/CeyMo/test/"
dest_folder = "/home/sora/Dataset/Rexroth/png_annotated/"

def move_json_files(src_folder, dest_folder):
    # ソースフォルダ内のファイル名を取得
    filenames = os.listdir(src_folder)
    
    # 出力フォルダが存在しない場合、作成
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    for filename in filenames:
        # ファイルがJSON形式であるかを確認
        if filename.endswith('.json'):
            # ソースと目的地のパスを生成
            src_path = os.path.join(src_folder, filename)
            dest_path = os.path.join(dest_folder, filename)
            
            # ファイルを移動
            shutil.copy(src_path, dest_path)
            
# 使用例
move_json_files(scr_folder, dest_folder)
