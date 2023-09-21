import os

def rename_files_in_directory_labels(directory_path):
    for filename in os.listdir(directory_path):
        # ファイル名と拡張子に分割（ここでは "1b_color" と ".png" など）
        main_part, ext = os.path.splitext(filename)
        main_split = main_part.split('_')
        # 拡張子に基づいて処理を分岐
        if ext == ".json":
            new_filename = f"ceymotrain_{main_split[0]}_gtFine_polygons{ext}"
        elif ext == ".png":
            new_filename = f"ceymotrain_{main_split[0]}_gtFine_{'_'.join(main_split[1:])}{ext}"
        else:
            continue  # その他の拡張子の場合はスキップ
        
        # ファイル名を変更
        os.rename(
            os.path.join(directory_path, filename),
            os.path.join(directory_path, new_filename)
        )

        
        
def rename_files_in_directory_imgs(directory_path):
    for filename in os.listdir(directory_path):
        # ファイル名と拡張子に分割（ここでは "1a" と ".png"）
        main_part, ext = os.path.splitext(filename)
        
        # 新しいファイル名を生成
        new_filename = f"ceymotrain_{main_part}_leftImg8bit{ext}"
        
        # ファイル名を変更
        os.rename(
            os.path.join(directory_path, filename),
            os.path.join(directory_path, new_filename)
        )


# 実行例
# directory_path には対象となるディレクトリのパスを指定してください。
directory_path = "/home/sora/datasets/cityscapes/gtFine/train/ceymotrain"
rename_files_in_directory_labels(directory_path)

