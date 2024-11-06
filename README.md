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


MODES:

Modes are the different ways of obtaining the upper threshold for bone marrow built into this algorithm. There are currently 3 available modes:
- Static mode: The threshold is a fixed value specified by the user as the constant OFFSET, which is going to be applied to all bones
- Dynamic mode: The thershold is going to be a fixed offset from the 5th percentile value of bone voxels. The fixed offset is added onto the 5th percentile value to obtain the upper threshold. The offset is a fixed value specified by the user as the constant OFFSET. The threshold thus dynamically adjust on a bone by bone basis depending on how the distribution of voxel values changes for each bone.
- Average mode (or dynamic average mode): The threshold for each bone is going to be the average of the 5th percentile value voxel (assumed to be bone marrow value) and the 95th percentile value voxel (assumed to be cortical bone). The threshold thus dynamically adjust on a bone by bone basis depending on how the distribution of voxel values changes for each bone. The OFFSET constant is not needed in this case, and can be set to anything.