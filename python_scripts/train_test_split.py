import glob, os
import shutil, random
from PIL import Image
import argparse


def traintestvalsplit(datapath, destpath):
    print("Specified dataset path:", datapath)
    total_data = len(glob.glob1(datapath, "*.jpg"))
    
    # Calculate the number of images for each set based on the ratio 6:3:1
    train_data_count = round(0.6 * total_data)
    test_data_count = round(0.3 * total_data)
    val_data_count = total_data - train_data_count - test_data_count
    
    print("Planned number of training images:", train_data_count)
    print("Planned number of test images:", test_data_count)
    print("Planned number of validation images:", val_data_count)
    
    # Create directories for train, test, and validation sets
    imgs_traindir = os.path.join(destpath, "images/train/")
    labels_traindir = os.path.join(destpath, "labels/train/")
    
    imgs_testdir = os.path.join(destpath, "images/test/")
    labels_testdir = os.path.join(destpath, "labels/test/")
    
    imgs_valdir = os.path.join(destpath, "images/val/")
    labels_valdir = os.path.join(destpath, "labels/val/")
    
    for dir_path in [imgs_traindir, labels_traindir, imgs_testdir, labels_testdir, imgs_valdir, labels_valdir]:
        try:
            os.makedirs(dir_path)
        except OSError:
            print(f"Creation of {dir_path} failed, the path probably already exists, skipping creation.")
        else:
            print(f"Creation of {dir_path} succeeded.")
    
    # Randomly sample files for training set
    train_data = random.sample(glob.glob1(datapath, "*.jpg"), train_data_count)
    
    # Get the remaining files
    remaining_files = list(set(glob.glob1(datapath, "*.jpg")) - set(train_data))
    
    # Randomly sample files for test set from the remaining files
    test_data = random.sample(remaining_files, test_data_count)
    
    # The rest go into the validation set
    val_data = list(set(remaining_files) - set(test_data))
    
    # Copy or move files into respective directories
    for dataset, img_dir, lbl_dir in zip([train_data, test_data, val_data], [imgs_traindir, imgs_testdir, imgs_valdir], [labels_traindir, labels_testdir, labels_valdir]):
        for f in dataset:
            shutil.move(os.path.join(datapath, f), img_dir)  # Move jpg files
            shutil.move(os.path.join(datapath, os.path.splitext(f)[0] + ".json"), lbl_dir)  # Move json files
    
    print("Data split complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--datapath", type=str, help="Path to the dataset.")
    parser.add_argument("--destpath", type=str, help="Destination path for the split datasets.")
    args = parser.parse_args()
    
    if args.datapath and args.destpath:
        traintestvalsplit(args.datapath, args.destpath)
    else:
        print("Wrong usage detected")
        parser.print_help()



	