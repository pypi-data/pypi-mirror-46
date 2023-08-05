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

def RP_rootdiameter(parameters):
	'''
	SUMMARY:
	'RP_rootdiameter': creates a 'bincount'x2 size text file of root diameter distribution 
	based on the radial values calculated from the medial axis of the mask image.  All 
	diameter values are outputted in terms of pixel lengths.

	USING CODE:
	Necessary images are just the binary root mask (located in 'mask_filename').  
	'output_filename' specifies the folder where the text file be placed.  'bincount' 
	specifies how many individual bins the data is to be fit into.

	PARAMETERS:
	1. mask_filename: filename of the root mask image.
	2. output_filename: filename where the text files are to be saved.
	3. bincount: the number of bins the root diameter is to be classified into.

	'''

	starttime = time.time()
	scriptname = 'rootdiameter'

	RP_timerstart(scriptname)

	mask_filename = parameters['mask_filename']
	output_filename = parameters['output_filename']
	bincount = parameters['bincount']

	IO_rootimage_mask = os.path.isfile(mask_filename)
	if IO_rootimage_mask is not True:
		raise ValueError('Input files are not present in specified file location.  Please recheck input files.')

	if bincount < 0:
		raise ValueError('bincount is assigned a negative, and thus invalid, number.  Please recheck input files.')
	
	image = Image.open(mask_filename)
	image = np.array(image)
	image = image > 0

	if np.sum(image) == 0:
		raise ValueError('No masked objects present in image, and thus, no analysis can be done.')

	#Create radius-labeled skeleton (medial axis of root)
	skel = skeletonize(image)
	skel = skel > 0

	rootdist = ndimage.morphology.distance_transform_edt(image)
	rootdist[~skel] = 0

	#ID position of all skeleton pixels
	skelpos = np.where(skel)
	skelpos_y = skelpos[0]
	skelpos_x = skelpos[1]

	#1D-array of all radial values assigned to skeleton
	rootdistvals = np.ravel(rootdist)
	removedvals = rootdistvals == 0
	rootdistvals = rootdistvals[~removedvals]

	[hist, edges] = np.histogram(rootdistvals, bins = bincount)

	histvals = np.zeros((np.shape(hist)[0], 2))
	for i in range(np.shape(hist)[0]):
		histvals[i, 0] = edges[i]
		histvals[i, 1] = hist[i]

	np.savetxt(output_filename, histvals)
	RP_timerend(starttime)







































