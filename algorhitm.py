import numpy as np 
import nibabel as nib
from scipy.ndimage import binary_opening
import os
import time
from utility_functions import *
OFFSET = 130

image_path_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input')


#length is just for cleaning up the print to console at the end, serves no functional purpose
length = len(image_path_base)


list_directory = os.listdir(image_path_base)
# image_dir = ''
# list_subdir = []

for dir in list_directory:
    image_dir = os.path.join(image_path_base, dir)
    print('New Directory: '+ image_dir)
    
    list_subdir = [d for d in os.listdir(image_dir) if 'segmentation' in d and '.csv' not in d]
    for subdir in list_subdir:
        print('New Subdirectory: '+ subdir)

        image_path = os.path.join(image_dir, subdir.replace('_segmentation','.nii.gz'))
        print(image_path)
        # image = nib.load(image_path)
        image_array = nib.load(image_path).get_fdata()
        
        # if np.max(np.shape(image_array)) != 512:
        #     print('Slice size is not 512x512, skipping')
        #     continue
        
        segmentation_list = os.listdir(os.path.join(image_dir, subdir))
        print(segmentation_list)
        
        for segmentation in segmentation_list:
            bone_mask_path = os.path.join(image_dir, subdir, segmentation)
            if '_marrow' not in segmentation and '.nii.gz' in bone_mask_path:
                print("Processing: ", bone_mask_path)
                output_path = os.path.join(image_dir , subdir , segmentation.replace('.nii.gz', '_marrow_dynamic_' + str(OFFSET) + '.nii.gz'))
                full_pipeline(image_array, image_path, bone_mask_path, output_path, length, OFFSET)

