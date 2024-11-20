import numpy as np 
import nibabel as nib
from scipy.ndimage import binary_opening
import os
import time
from utility_functions import *

OFFSET = 150
OPENING = 'cuda'
OPENING_LIST = ['cuda', 'scipy']
MODE = 'dynamic'
MODE_LIST = ['dynamic', 'static', 'average']
start_time = time.time()
if MODE not in MODE_LIST:
    print('Invalid mode, please select from: ', MODE_LIST)
    exit()
if OPENING not in OPENING_LIST:
    print('Invalid opening, please select from: ', OPENING_LIST)
    exit()

#The dataset has to be in a specific format, refer to README for more information
#TODO: maybe generalize this? (Won't be necessary when in a pipeline, thresholding will be automatically applied to selected outputs of TotalSegmentator agent)
image_path_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input')


#length is just for cleaning up the print to console at the end, serves no functional purpose
length = len(image_path_base)


list_directory = os.listdir(image_path_base)

#List all studies in the dataset directiory
for dir in list_directory:
    image_dir = os.path.join(image_path_base, dir)
    print('New Directory: '+ image_dir)
    
    #List all segmentation directories for each scan within a study
    list_subdir = [d for d in os.listdir(image_dir) if 'segmentation' in d and '.csv' not in d]
    for subdir in list_subdir:
        print('New Subdirectory: '+ subdir)

        image_path = os.path.join(image_dir, subdir.replace('_segmentation','.nii.gz'))
        print(image_path)
        #Read the CT scan as a numpy array
        image_array = nib.load(image_path).get_fdata()
        
        #List all bone segmentations for each scan
        segmentation_list = os.listdir(os.path.join(image_dir, subdir))
        print(segmentation_list)
        
        for segmentation in segmentation_list:
            bone_mask_path = os.path.join(image_dir, subdir, segmentation)
            #Check that this specific mask is not already a bone marrow mask and that it is a nifti file
            if '_marrow' not in segmentation and '.nii.gz' in bone_mask_path:
                print("Processing: ", bone_mask_path)

                #Change save name convention based on selected mode
                match MODE:
                    case 'dynamic':
                        save_suffix = '_marrow_dynamic_' + str(OFFSET)
                    case 'static':
                        save_suffix = '_marrow_sub' + str(OFFSET)
                    case 'average':
                        save_suffix = '_marrow_dynamic_average'
                if OPENING == 'cuda':
                    save_suffix += '_cuda'
                output_path = os.path.join(image_dir , subdir , segmentation.replace('.nii.gz', save_suffix + '.nii.gz'))
                if OPENING == 'cuda':
                    try:
                        #Apply the full pipeline to the bone mask to obtain and save bone marrow
                        full_pipeline(image_array, bone_mask_path, output_path, length, OFFSET, MODE, OPENING)
                    except Exception as e:
                        print('Failed to process with gpu, trying cpu: ', bone_mask_path)
                        opening = 'scipy'
                        output_path = os.path.join(image_dir , subdir , segmentation.replace('.nii.gz', save_suffix + '_scipy.nii.gz'))
                        full_pipeline(image_array, bone_mask_path, output_path, length, OFFSET, MODE, opening)
                else:
                #Apply the full pipeline to the bone mask to obtain and save bone marrow
                    full_pipeline(image_array, bone_mask_path, output_path, length, OFFSET, MODE, OPENING)
end_time = time.time()
print('Total time: ', (end_time - start_time)/3600, ' hours')