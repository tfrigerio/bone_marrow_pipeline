This repository contains the current thresholding algorithm to obtain bone marrow segmentation from a CT file and its bone_segmentations obtained using Totalsegmentator. 

The script navigates the input directory tree, identifies the file and its masks and:
- loads the CT scan and a bone mask
- isolates the bone on the CT image (setting every other value to 0) 
- obtains the upper threshold for the bone marrow by applying a fixed offset to the 5th percentile value of the bone masks
- thresholds to obtain bone marrow
- performs morphological opening (erosion and dilation) to refine the segmentation.

The input scan should be placed in a subdirectory along with a foler including its bone masks. This subdirectory should be inside of a directory named input/ 

The naming convention should be:
- Name of CT scan in format CT_{filename}.nii.gz
- Name of segmentation folder in format CT_{filename}_segmentations/