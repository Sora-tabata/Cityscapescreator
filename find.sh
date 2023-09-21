# 探索するディレクトリを指定
search_directory="/home/sora/datasets/cityscapes/gtFine/test/ceymotest/"

# 'CL' を含むファイルを探索
find "$search_directory" -type f -exec grep -l 'CL' {} +
