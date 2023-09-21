from PIL import Image
import os

folder_path = "/home/sora/Dataset/Rexroth/images/val/"
output_folder = "/home/sora/Dataset/Rexroth/images/val_png/"

def convert_jpg_to_png(folder_path, output_folder):
    # 指定されたフォルダ内のファイル名を取得
    filenames = os.listdir(folder_path)
    
    # 出力フォルダが存在しない場合、作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in filenames:
        # ファイルがJPG形式であるかを確認
        if filename.endswith('.jpg') or filename.endswith('.jpeg'):
            # 画像を開く
            img = Image.open(os.path.join(folder_path, filename))
            
            # ファイル名から拡張子を除去
            basename = os.path.splitext(filename)[0]
            
            # PNG形式で保存
            img.save(os.path.join(output_folder, f"{basename}.png"))

# 使用例
convert_jpg_to_png(folder_path, output_folder)
