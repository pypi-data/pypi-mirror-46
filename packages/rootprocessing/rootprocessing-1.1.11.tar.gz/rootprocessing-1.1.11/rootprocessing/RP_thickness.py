import numpy as np
import time
import scipy.ndimage as imp
import datetime

from scipy import ndimage
from skimage.morphology import skeletonize
import scipy.misc
from scipy.signal import medfilt
from PIL import Image
import os

from rootprocessing.RP_timerstart import RP_timerstart
from rootprocessing.RP_timerprogress import RP_timerprogress
from rootprocessing.RP_timerend import RP_timerend
from rootprocessing.RP_windowrange import RP_windowrange
from rootprocessing.RP_distwindowrange import RP_distwindowrange
from rootprocessing.RP_remove import RP_remove
from rootprocessing.RP_linedraw import RP_linedraw

def RP_thickness(parameters):
    '''
    SUMMARY:
    'RP_thickness': creates a half-thickness image (with distance in pixels) from a binary 
    segmented image of a root, assuming a cylindrical shape.
    
    USING CODE:
    Using the binary image, a skeleton (i.e. medial axis transform) of the original image 
    is calculated. At the same time, the contour of the root (i.e. root edge) is calculated.  

    From here, for every pixel (x,y)_p, the nearest root edge pixel (x,y)_e that doesn't 
    intersect the medial axis is determined.  Using this trajectory, we extend the imaginary
    line connecting them to the medial skeleton.  We then use the radial distance R assigned 
    to the skeleton pixel.  Using these values, we then assume a cylindrical distribution, 
    and calculate the half-dome height H of the pixel as follows: H^2 = R^2 - (R-EP)^2, where 
    EP is the distance from the edge to the pixel.  

    
    PARAMETERS:
    1. image_filename: filename of evaluated image.  
    2. output_filename: filename where image is to be saved.
    
    SAMPLE INPUT: 
    ctype = 'Chamber10'
    
    wd_filename = '/Volumes/Untitled 2/rhizosphere'
    image_filename = wd_filename+'/morph_mask_crop/clean/'+ctype+'_clean.tif'
    output_filename = wd_filename+'/thickness/'+ctype+'_radmap.fits'
    
    '''
    
    starttime = time.time()
    scriptname = 'thickness map'
    
    image_filename = parameters['image_filename']
    output_filename = parameters['output_filename']
    
    IO_rootimage = os.path.isfile(image_filename)
    if IO_rootimage is not True:
        raise ValueError('Input files are not present in specified file location.  Please recheck input files.')
    

    RP_timerstart(scriptname)

    image = Image.open(image_filename)
    image = np.array(image)
    #image = fits.open(image_filename)[0].data

    image = medfilt(image, kernel_size = 7)
    imdim = np.shape(image)

    #image = np.asarray(image)
    #Skeletonization of root image
    skel = skeletonize(image > 0)

    #Distance transform from center of root to all other pixels
    dist = ndimage.morphology.distance_transform_edt(~skel)

    #Distance from edge of root to center
    rootdist = ndimage.morphology.distance_transform_edt(image)

    #Contour pixels of the root
    contour_img = RP_remove(image)
    
    [pixelpos_y,pixelpos_x] = np.where(image > 0)

    T_map = np.zeros(imdim)
    counter = 0
    pctval = 0
    totalcount = np.shape(pixelpos_x)[0]
    maxvalstop = int(2.5*np.floor(np.max(rootdist)))

    for m in range(0,np.shape(pixelpos_x)[0]):
        loopbreaker = 0
        [pctval,counter] = RP_timerprogress(counter,pctval,totalcount)

        i = pixelpos_y[m]
        j = pixelpos_x[m]

        #a. Eliminate Edge Effects (x-dimension only)
        if (j == 0) | (j == imdim[1]):
            T_map[i,j] = rootdist[i,j]*rootdist[i,j]
            loopbreaker = 1
            continue

        #I. ID if skeleton
        if skel[i, j]:
            T_map[i,j] = rootdist[i,j]*rootdist[i,j]
            loopbreaker = 1
            continue

        if loopbreaker:
            continue

        #II. Find closest contour
        advanceflag = 0
        windowcounter = 10
        windowsize = 11

        while advanceflag == 0:
            if windowsize > maxvalstop:
                T_map[i,j] = rootdist[i,j]*rootdist[i,j]
                loopbreaker = 1

            windowsize = int(2*np.floor(rootdist[i,j])+1+windowcounter)

            #Create local window images
            [y1,y2,x1,x2] = RP_windowrange(i,j,windowsize,imdim)
            [y_1,y_2,x_1,x_2,y_c,x_c] = RP_distwindowrange(i,j,windowsize,imdim)

            image_w = image[y1:y2,x1:x2]
            skel_w = skel[y1:y2,x1:x2]
            rootdist_w = rootdist[y1:y2,x1:x2]
            contour_w = contour_img[y1:y2,x1:x2]
            imdim_w = np.shape(contour_w)
            dist_pixel_edge = rootdist_w[y_c,x_c]
        
            #Find all contour pixels in local window
            conpos = np.where(contour_w)
            conpos_y = conpos[0]
            conpos_x = conpos[1]
            condist = np.sqrt((y_c-conpos_y)*(y_c-conpos_y) + (x_c-conpos_x)*(x_c-conpos_x))

            #Find closest contour pixel
            minconpos = np.where(condist == np.min(condist))
            minconpos_y = conpos_y[minconpos[0][0]]
            minconpos_x = conpos_x[minconpos[0][0]]

            dist_pixel_con = condist[minconpos[0][0]]

            if dist_pixel_con == 0:
                T_map[i,j] = 0
                advanceflag = 1
                loopbreaker = 1
                break

            img_check = RP_linedraw(minconpos_y,minconpos_x,y_c,x_c,1,0,imdim_w)
            img_check[minconpos_y,minconpos_x] = 0

            #Confirm it doesn't intersect with skeleton
            skel_int_img = skel_w[img_check > 0]
            if np.sum(skel_int_img) == 0:
                advanceflag = 1
                break

            #Case: pixel chosen intersects skeleton
            else:
                interfercheck = np.zeros(np.shape(condist))
                for k in range(np.shape(condist)[0]):
                    img_check = RP_linedraw(conpos_y[k],conpos_x[k],y_c,x_c,1,0,imdim_w)
                    #if greater than 0, then pixel fails to meet criteria
                    interfercheck[k] = np.sum(skel_w[img_check > 0])
                #Case 1: one or more points that don't interfere are found
                if np.sum(interfercheck == 0) > 0:
                    minconpos = condist*1
                    minconpos[interfercheck != 0] = float('inf')
                    minconpos = np.where(minconpos == np.min(minconpos))

                    minconpos_y = conpos_y[minconpos[0][0]]
                    minconpos_x = conpos_x[minconpos[0][0]]

                    dist_pixel_con = condist[minconpos[0][0]]

                    #Reality check
                    img_check = RP_linedraw(minconpos_y,minconpos_x,y_c,x_c,1,0,imdim_w)
                    skel_int_img = skel_w[img_check > 0]

                    if np.sum(skel_int_img) == 0:
                        advanceflag = 1
                        break
                    else:
                        T_map[i,j] = rootdist[i,j]*rootdist[i,j]
                #Case 2: no suitable pixels were found.  Re-do code with larger window.
                else:
                    #Eliminate edge effects
                    if dist[i,j] < 1.5:
                        T_map[i,j] = rootdist[i,j]*rootdist[i,j]
                        loopbreaker = 1
                        advanceflag = 1
                        break
                    if dist_pixel_con < 1.5:
                        T_map[i,j] = rootdist[i,j]*rootdist[i,j]
                        loopbreaker = 1
                        advanceflag = 1
                        break

                    windowcounter += 100
                    continue

        if loopbreaker:
            continue


        #III. Find closest skeleton
        advanceflag = 0
        windowcounter = 10
        windowsize_sk = 11
        while advanceflag == 0:
            if windowsize_sk > maxvalstop:
                T_map[i,j] = rootdist[i,j]*rootdist[i,j]
                loopbreaker = 1
                break

            windowsize_sk = int(2*np.floor(dist[i,j]+1+windowcounter))
            [a,b,c,d] = RP_windowrange(i,j,windowsize_sk,imdim)
            [y_1,y_2,x_1,x_2,y_c_,x_c_] = RP_distwindowrange(i,j,windowsize_sk,imdim)

            skel_im = skel[a:b,c:d]
            rootdist_im = rootdist[a:b,c:d]
            imdim_im = np.shape(skel_im)

            #Remapping of contour and center pixel into skeleton mapping
            mcp_y_rel = minconpos_y-(y_c-y_c_)
            mcp_x_rel = minconpos_x-(x_c-x_c_)

            img_check = RP_linedraw(mcp_y_rel,mcp_x_rel,y_c_,x_c_,0,1,imdim_im)

            #Find skeleton
            skelpos_im = np.zeros(imdim_im)
            im_check = np.zeros(imdim_im)
            im_skel = np.zeros(imdim_im)
            im_check[img_check > 0] = 1
            im_skel[skel_im] = 1
            skelpos_im = im_check+im_skel
            skelpos_im = skelpos_im > 1

            skelpos = np.where(skelpos_im)
            skelpos_y = skelpos[0]
            skelpos_x = skelpos[1]

            #Case 1: one or more skeleton pixels were found
            if np.sum(skelpos_im) > 0:
                #Case 1a: more than one was found - choose closest
                if np.shape(skelpos_y)[0] > 1:
                    skeldist = (skelpos_y-y_c_)*(skelpos_y-y_c_) + (skelpos_x-x_c_)*(skelpos_x-x_c_)
                    skeldist = np.sqrt(skeldist)
                    minskelpos = np.where(skeldist == np.min(skeldist))

                    minskelpos_y = skelpos_y[minskelpos[0][0]]
                    minskelpos_x = skelpos_x[minskelpos[0][0]]
                    dist_pixe_skel = skeldist[minskelpos[0][0]]
                    advanceflag = 1
                    break
                else:
                    minskelpos_y = skelpos_y[0]
                    minskelpos_x = skelpos_x[0]
                    dist_pixel_skel = (minskelpos_y-y_c_)*(minskelpos_y-y_c_) + (minskelpos_x-x_c_)*(minskelpos_x-x_c_)
                    dist_pixel_skel = np.sqrt(dist_pixel_skel)
                    advanceflag = 1
            #Case 1b: none were found - expand search
            else:
                if np.shape(skelpos_y)[0] == 0:
                    windowcounter += 100
                    continue

        if loopbreaker:
            continue

        rad_val = rootdist_im[minskelpos_y,minskelpos_x]
        T_map[i,j] = rad_val*rad_val-(rad_val-dist_pixel_edge)*(rad_val-dist_pixel_edge)
        if T_map[i,j] < 0:
            T_map[i,j] = rootdist[i,j]*rootdist[i,j]
            continue


    #imghdu = fits.PrimaryHDU(T_map)
    #hdulist = fits.HDUList([imghdu])
    #hdulist.writeto(output_filename)
    T_map_neg = T_map < 0
    pixelpos_neg = np.where(T_map_neg)
    pixelpos_neg_y = pixelpos_neg[0]
    pixelpos_neg_x = pixelpos_neg[1]
    for m in range(0,np.shape(pixelpos_x)[0]):
        i = pixelpos_neg_y[m]
        j = pixelpos_neg_x[m]
        T_map[i,j] = rootdist[i,j]*rootdist[i,j]


    T_map = np.sqrt(T_map)

    T_map = Image.fromarray(T_map)
    T_map.save(output_filename)
    
    RP_timerend(starttime)
    