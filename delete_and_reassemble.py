import numpy as np
import nibabel as nib
import os

def load_and_merge_nifti_files_with_keywords_without_keyword(root_dir, keyword_1, keyword_2):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            i = 0
            if keyword_1 in file and file.endswith('.nii.gz'):
                file_path = os.path.join(root, file)
                try:
                    
                    nifti = nib.load(file_path).get_fdata()
                    if i == 0:
                        merged_nifti = nifti
                        i+=1
                    else:
                        merged_nifti = np.logical_or(merged_nifti,nifti)
                    nifti_header = nib.load(file_path).header
                except Exception as e:
                    print(f"Error loading file: {file_path}")
                    print(e)
    return merged_nifti, nifti_header 

# def merge_nifti_files(nifti_files):
#     merged_nifti = np.zeros_like(nifti_files[0])
#     i=0
#     for nifti in nifti_files:
#         i+=1
#         merged_nifti = np.logical_or(merged_nifti,nifti)
#         print("Merged nifti: ", i)
#     return merged_nifti

root_dir = '/radraid/apps/personal/tfrigerio/bone_marrow_pipeline/input'
study_list = os.listdir(root_dir)
keyword_list = ['_dynamic_150', '_sub230', '_dynamic_average']
keyword_2 = 'spinal_cord'
for study in study_list:
    print(f"Processing study {study}")
    CT_list = [item for item in os.listdir(os.path.join(root_dir, study)) if 'segmentation' in item]
    for CT in CT_list:
        print(f"Processing CT {CT}")
        for keyword_1 in keyword_list:
            merged_nifti, last_nifti_header = load_and_merge_nifti_files_with_keywords_without_keyword(os.path.join(root_dir, study, CT), keyword_1, keyword_2)
            # merged_nifti = merge_nifti_files(nifti_files)
            print(f"Shape of merged nifti: {type(merged_nifti)}")
            #Save the merged nifti file
            output_path = os.path.join(root_dir, study, CT, 'assembled_segmentation' + keyword_1 + '.nii.gz')
            nifti = nib.Nifti1Image(merged_nifti, affine = None, header = last_nifti_header)
            print(f"Shape of nifti: {nifti.shape}")
            nib.save(nifti, output_path)