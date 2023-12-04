# 探索するディレクトリを指定
search_directory="/media/sora/SanDisk/cityscapes_1002/gtFine/val/frankfurt/"

# 'CL' を含むファイルを探索
find "$search_directory" -type f -exec grep -l 'lane*' {} +
