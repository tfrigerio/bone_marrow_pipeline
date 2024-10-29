import numpy as np 
import nibabel as nib
from scipy.ndimage import binary_dilation, binary_erosion, binary_opening
import os
import time
from utility_functions import *

def load_image_and_bone_mask(image_path, bone_mask_path):
    image = nib.load(image_path)
    image_array = image.get_fdata()
    bone_mask = nib.load(bone_mask_path)
    bone_mask_array = bone_mask.get_fdata()
    return image, bone_mask, image_array, bone_mask_array

def isolate_bone_on_image(image_array, bone_mask_array):
    bone_array = image_array * bone_mask_array
    return bone_array

def obtain_upper_threshold(image_array, bone_mask_array, offset):
    values = image_array[bone_mask_array==1]
    if np.array_equal(values, np.zeros(np.shape(values))) == True:
        return 0
    else:
        fifth_percentile = np.percentile(values, 5)
        threshold = fifth_percentile + offset
        return threshold

def threshold_segmentation_of_bone_marrow(bone_array, threshold_up, threshold_down, bone_mask_array):
    bone_marrow_array_mask = np.zeros(bone_array.shape)
    bone_marrow_array_mask[bone_array < threshold_up] = 1
    bone_marrow_array_mask[bone_array <= threshold_down] = 0
    bone_marrow_array_mask = bone_marrow_array_mask * bone_mask_array
    return bone_marrow_array_mask


def opening3D(bone_marrow_array_mask, iterations):
          
    kernel = np.ones((5, 5, 1), np.uint8)
        
    opened = binary_opening(bone_marrow_array_mask, structure=kernel, iterations=iterations)
    return opened
    

def header_processing(bone_marrow_array_mask,bone_mask):
    connected_components = nib.Nifti1Image(bone_marrow_array_mask, affine=None, header=bone_mask.header)
    #print(connected_components.header)
  
    connected_components.header['pixdim']=bone_mask.header['pixdim']
    connected_components.header['xyzt_units']=bone_mask.header['xyzt_units']
    connected_components.header['qform_code']=bone_mask.header['qform_code']
    connected_components.header['sform_code']=bone_mask.header['sform_code']
    connected_components.header['quatern_b']=bone_mask.header['quatern_b']
    connected_components.header['quatern_c']=bone_mask.header['quatern_c']
    connected_components.header['quatern_d']=bone_mask.header['quatern_d']
    connected_components.header['qoffset_x']=bone_mask.header['qoffset_x']
    connected_components.header['qoffset_y']=bone_mask.header['qoffset_y']
    connected_components.header['qoffset_z']=bone_mask.header['qoffset_z']
    connected_components.header['srow_x']=bone_mask.header['srow_x']
    connected_components.header['srow_y']=bone_mask.header['srow_y']
    connected_components.header['srow_z']=bone_mask.header['srow_z']
    
    return connected_components

def save_masks(connected_components, output_path):
    nib.save(connected_components, output_path)

def full_pipeline(image_path, bone_mask_path, output_path, length, offset):

    t0 = time.time()
    image, bone_mask, image_array, bone_mask_array = load_image_and_bone_mask(image_path, bone_mask_path)
    t1 = time.time()
    print('image_shape: ', image_array.shape)
    print('Time to load image and bone mask: ', t1-t0)

    t2 = time.time()
    
    if image_array.shape != bone_mask_array.shape:
        if image_array.shape[-1] == 1:
            image_array = image_array[:, :, :, 0]
        else:
            raise ValueError('Image and mask have different shapes')
    t3 = time.time()
    print('Time to check shapes: ', t3-t2)

    t4 = time.time()
    bone_array = isolate_bone_on_image(image_array, bone_mask_array)
    t5 = time.time()
    print('Time to isolate bone on image: ', t5-t4)

    t6 = time.time()
    upper_threshold = obtain_upper_threshold(image_array, bone_mask_array, offset)
    t7 = time.time()
    print('Time to obtain upper threshold: ', t7-t6)

    t8 = time.time()
    bone_marrow_array_mask = threshold_segmentation_of_bone_marrow(bone_array, upper_threshold, -100, bone_mask_array)
    t9 = time.time()
    print('Time to threshold segmentation of bone marrow: ', t9-t8)

    t10 = time.time()
    if np.max(np.shape(image_array))>= 100 :
        bone_marrow_array_mask = opening3D(bone_marrow_array_mask, 1)
    t11 = time.time()
    print('Time to open 3D: ', t11-t10)

    t12 = time.time()
    connected_components = header_processing(bone_marrow_array_mask, bone_mask)
    t13 = time.time()
    print('Time to process header: ', t13-t12)

    t14 = time.time()
    save_masks(connected_components, output_path)
    t15 = time.time()
    print('Time to save masks: ', t15-t14)
    return print(bone_mask_path[length:])