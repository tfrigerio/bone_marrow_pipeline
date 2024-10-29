import numpy as np 
import nibabel as nib
from scipy.ndimage import binary_dilation, binary_erosion, binary_opening
import os
import time
from utility_functions import *

image_path_base = os.path.dirname(os.path.abspath(__file__)) + '/input'

length = len(image_path_base)


list_directory = os.listdir(image_path_base)
offset = 130
# image_dir = ''
# list_subdir = []

for i in range(len(list_directory)):
    image_dir = image_path_base + '/' + list_directory[i]
    print('New Directory: '+ image_dir)
    
    list_subdir = [d for d in os.listdir(image_dir) if 'segmentation' in d and '.csv' not in d]
    for j in range(len(list_subdir)):
        print('New Subdirectory: '+ list_subdir[j])

        image_path = image_dir + '/' + list_subdir[j][:-13] + '.nii.gz'
        image = nib.load(image_path)
        image_array = image.get_fdata()
        if np.max(np.shape(image_array)) != 512:
            print('Slice size is not 512x512, skipping')
            continue
        else:
            segmentation_list = os.listdir(image_dir+'/'+list_subdir[j])
    
            for k in range(len(segmentation_list)):
                bone_mask_path = image_dir + '/' + list_subdir[j] + '/' + segmentation_list[k]
                if '_marrow' not in bone_mask_path and '.nii.gz' in bone_mask_path:
                    print("LFG: ", bone_mask_path)
                    output_path = image_dir + '/' + list_subdir[j] + '/' + segmentation_list[k][:-7] + '_marrow_dynamic_' + str(offset) + '.nii.gz'
                    full_pipeline(image_path, bone_mask_path, output_path, length, offset)

