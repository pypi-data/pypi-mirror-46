'''
Methods to segment individual droplets from an array of drops in an emulsion
'''

import os

import numpy as np


from skimage import io, exposure
from skimage.color import label2rgb
from skimage.exposure import equalize_adapthist
from skimage.feature import peak_local_max
from skimage.filters import threshold_otsu
from skimage.segmentation import watershed
from skimage.measure import regionprops
from skimage.morphology import binary_closing, remove_small_holes, disk
import cv2
from tqdm import tqdm

from scipy import ndimage as ndi

from src.data.utils import select_rectangle, open_grey_scale_image, crop


def segment(img, exp_clip_limit=0.06, closing_disk_radius=4, rm_holes_area=8192, minima_minDist=100, mask_val=0.1):
    '''
    Segments droplets in an image using a watershed algorithm.

    Parameters
    ----------
    img: numpy.ndarray
        Array representing the greyscale values (0-255) of an image cropped to show only the droplets region
    exp_clip_limit: float [0-1], optional
        clip_limit parameter for adaptive equalisation
    closing_disk_radius: int, optional
        diamater of selection disk for the closing function
    rm_holes_area: int, optional
        maximum area of holes to remove
    minima_minDist: int, optional
        minimum distance between peaks in local minima determination
    mask_val: float, optional
        Masking value (0-1) for the distance plot to remove small regions. Default 0.2

    Returns
    -------
    (labeled: numpy.ndarray, num_maxima: int, num_regions: int)
        labeled: labeled array of the same shape as input image where each region is assigned a disctinct integer label.
        num_maxima: Number of maxima detected from the distance transform
        num_regions: number of labeled regions
    '''

    # Adaptive equalization
    img_adapteq = equalize_adapthist(img, clip_limit = exp_clip_limit)

    # Minimum threshold
    threshold = threshold_otsu(img_adapteq)

    binary = img_adapteq > threshold

    # Remove dark spots and connect bright spots
    closed = binary_closing(binary, selem=disk(closing_disk_radius))
    rm_holes_closed = remove_small_holes(closed, area_threshold=rm_holes_area, connectivity=2)

    # Calculate the distance to the dark background
    distance = ndi.distance_transform_edt(rm_holes_closed)
    #distance = cv2.distanceTransform(rm_holes_closed.astype('uint8'),cv2.DIST_L2,3) # TODO: test cv2 implementation for speed and acuraccy

    # Increase contrast of the the distance image
    cont_stretch = exposure.rescale_intensity(distance, in_range='image')

    # Mask the distance image to remove interstitial points
    masked = cont_stretch.copy()
    masked[masked < mask_val] = 0

    # Find local maximas of the distance image
    local_maxi = peak_local_max(masked, indices=False, min_distance=minima_minDist)

    # Markers for watershed are the local maxima of the distance image
    markers, num_maxima = ndi.label(local_maxi)

    # Run watershed algorithm on the inverse of the distance image
    segmented = watershed(-masked, markers, mask = masked > 0)

    # Label the segments of the image
    labeled, num_regions = ndi.label(segmented)

    return (labeled, num_maxima, num_regions)

def extract_indiv_droplets(img, labeled, border = 25, ecc_cutoff = 0.8):
    '''
    Separate the individual droplets as their own image.

    Parameters
    ----------
    img: numpy.ndarray
        Array representing the greyscale values (0-255) of the segmented image.
    labeled: numpy.ndarray
        Label array corresponding to 'img' where each region is assigned a disctinct integer value
    border: int, optional
        Number of pixels to add on each side of the labeled area to produce the final image.
    ecc_cutoff: float, optional
        Maximum eccentricity value of the labeled region. Regions with higher eccentricity will be ignored.

    Returns
    -------
    list(numpy.ndarray)
        list where each array corresponds to one of the labeled regions bounding box + the border region
    list(RegionProperties)
        regionProperties of the labeled regions
    '''

    # Get region props
    reg = regionprops(labeled, coordinates='rc')

    # Initialize list of images
    img_list = []

    # Get original image size
    max_col = img.shape[1]
    max_row = img.shape[0]

    reg_clean = [region for region in reg if (region.eccentricity < ecc_cutoff)]

    for region in reg_clean:
        (min_row, min_col, max_row, max_col) = region.bbox
        drop_image = img[np.max([min_row-border,0]):np.min([max_row+border,max_row]),np.max([min_col-border,0]):np.min([max_col+border,max_col])]
        resized = cv2.resize(drop_image, (150,150)) * 1./255
        expanded_dim = np.expand_dims(resized, axis=2)
        img_list.append(expanded_dim)

    return img_list, reg_clean

def segment_droplets_to_file(image_filename, crop_box=None, save_overlay=False):

    if os.path.isdir(image_filename):
        img_list = [os.path.join(image_filename,f) for f in os.listdir(image_filename) if f.endswith('.JPG')]
    elif os.path.isfile(image_filename):
        img_list = [image_filename]

    # Get the crop box from the first image if not provided
    print('Getting crop box from image {}'.format(img_list[0]))
    if not crop_box:
        crop_box = select_rectangle(open_grey_scale_image(img_list[0]))

    for image_file in tqdm(progress_bar):
        # Open image
        image = open_grey_scale_image(image_file)

        # Obtain crop box from user if not passed as argument
        if not crop_box:
            crop_box = select_rectangle(image)

        # Crop image
        cropped = crop(image, crop_box)

        # Segment image
        (labeled, num_maxima, num_regions) = segment(cropped)

        # Save the overlay image if requested
        if save_overlay:
            image_overlay = label2rgb(labeled, image=cropped, bg_label=0)
            filename = image_file.split('.')[0] + '_segmented.jpg'
            io.imsave(filename, image_overlay)

        # Extract individual droplets
        drop_images, _ = extract_indiv_droplets(cropped, labeled)

        # Output folder has the same name as the image by default
        out_directory = image_file.split('.')[0] + '/'

        if not os.path.exists(out_directory):
            os.mkdir(out_directory)

        # Save all the images in the output directory
        for (i, img) in enumerate(drop_images):
            name = out_directory + image_file.split('.')[0].split('/')[-1] + '_drop_' + str(i) + '.jpg'
            io.imsave(name, img, check_contrast=False)
