import numpy as np

def RP_linedraw(i_p, j_p, i_c, j_c, for_back, extensionflag, imdim):
	'''
	SUMMARY: 
	'RP_linedraw': draws a raster-based line from the center pixel (i,j)_c
	to the edge pixel (i,j)_p.  Used primarily in the 'RP_thickness' code.

	USING CODE:
	Position 'i_p' and 'j_p', and 'i_c' and 'j_c' correspond to the pixel 
	position of the target pixel and center, respectively - these positions
	are relative to the window size created using the dimensions specified by
	'imdim'.  'for_back' specifies whether the line is to be extended forward
	('for_back' = 1) from the center pixel to the target pixel, or backwards
	('for_back = 0) away from the target pixel, but on the same slope.
	'extensionflag' specifies whether the line is to extend to the target 
	pixel ('extensionflag' = 0) or past it to the edge of the window 
	('extensionflag' = 1).

	PARAMETERS:
	A. INPUTS - 
	1. i_p: row position for the off-center pixel (y).
	2. j_p: column position for the off-center pixel (x).
	3. i_c: row position for the center pixel (y).
	4. j_c: column position for the center pixel (x).
	5. for_back: specification for whether the drawn line will extend forwards
	(1) or backwards (0).
	6. extensionflag: specification for whether the drawn line will stop at
	the off-center pixel (0) or at the edge of the window (1).

	B. OUTPUTS -
	1. img_out: image with dimensions 'imdim', with a line drawn under the 
	conditions specified above.


	EXAMPLE:
	For a 81x81 array, in which there are two pixel positions [60,30] and 
	[55,20], we can specify 'i_p' and 'j_p' to be 60 and 30, respectively, 
	and 'i_c' and 'j_c' to be 40 and 40, respectively.  'imdim' would correspond
	to [81,81].  If we set 'for_back' to 1 and 'extensionflag' to 0, a series of 
	pixels approximating a line will be drawn between the points of [60,30] and 
	[40,40], outputted under the variable name 'img_out'.

	'''

	img_out = np.zeros(imdim)
	#I. Determine quadrant
	if j_p == j_c:					#Vertical line
		if i_p < i_c:
			if for_back == 1:
				quadval = 12			#Vertical line upwards
			else:
				quadval = 34
		else:
			if for_back == 1:
				quadval = 34			#Vertical line downwards
			else:
				quadval = 12
	else:
		if i_p == i_c:				#Horizontal line
			if j_p < j_c:
				if for_back == 1:
					quadval = 13		#Horizontal line left
				else:
					quadval = 24
			else:
				if for_back == 1:
					quadval = 24		#Horizontal line right
				else:
					quadval = 13
		else:
			if i_p < i_c:
				if j_p < j_c:
					if for_back == 1:
						quadval = 1		#Top left
						x = np.array(range(0, j_c))
					else:
						quadval = 4
						x = np.array(range(j_c, imdim[1]))
				else:
					if for_back == 1:
						quadval = 2 	#Top right
						x = np.array(range(j_c, imdim[1]))
					else:
						quadval = 3
						x = np.array(range(0, j_c))
			else:
				if j_p < j_c:
					if for_back == 1:
						quadval = 3 	#Bottom left
						x = np.array(range(0, j_c))
					else:
						quadval = 2
						x = np.array(range(j_c, imdim[1]))

				else:
					if for_back == 1:
						quadval = 4 	#Bottom right
						x = np.array(range(j_c, imdim[1]))
					else:
						quadval = 1
						x = np.array(range(0, j_c))
			
			xrangeval = np.shape(x)[0]



	if quadval == 12:
		img_out[0:i_c, j_c] = img_out[0:i_c, j_c] + 2
	if quadval == 34:
		img_out[i_c:imdim[0], j_c] = img_out[i_c:imdim[0], j_c] + 2
	if quadval == 13:
		img_out[i_c, 0:j_c] = img_out[i_c, 0:j_c] + 2
	if quadval == 24:
		img_out[i_c, j_c:imdim[1]] = img_out[i_c, j_c:imdim[1]] + 2
	if quadval < 10:
		filledvals = np.zeros((xrangeval, 3))
		m = (i_p-i_c)/(j_p-j_c)
		b = i_c-m*j_c
		y = m*x+b
		for i in range(xrangeval-1):
			filledvals[i][0] = int(x[i])
			filledvals[i][1] = int(np.floor(y[i]))
			filledvals[i][2] = int(np.floor(y[i+1]))

		filledvals[xrangeval-1][0] = int(x[xrangeval-1])
		filledvals[xrangeval-1][1] = int(np.floor(y[xrangeval-1]))

		if quadval % 2 == 0:
			filledvals[xrangeval-1][2] = int(np.floor(y[xrangeval-1]))
		else:
			filledvals[xrangeval-1][2] = int(i_c)
		
		filledvals[filledvals[:, 1] < 0, 1] = 0
		filledvals[filledvals[:, 1] > imdim[1], 1] = int(imdim[1])
		filledvals[filledvals[:, 2] < 0, 2] = 0
		filledvals[filledvals[:, 2] > imdim[1], 2] = int(imdim[1])
		rrsize = np.shape(filledvals)[0]-1

		if quadval == 1:
			removedrows = filledvals[:, 1] + filledvals[:, 2] == 0
			if removedrows[0] == True:

				#zeropos_ = np.where(removedrows == 0)
				#zeropos = zeropos_[0][np.shape(zeropos_)[0][0]
				#zeropos = np.where(removedrows == 0)[0][0]

				zeropos = np.where(removedrows == True)[0][0]
				filledvals = filledvals[zeropos:xrangeval, :]
		if quadval == 2:
			removedrows = (filledvals[:, 1] + filledvals[:, 2] == 0) & (filledvals[:, 1] == 0)
			if removedrows[rrsize] == True:
				zeropos = np.where(removedrows == True)[0][0]
				filledvals = filledvals[0:zeropos+1, :]
		if quadval == 3:
			removedrows = (filledvals[:, 1] - filledvals[:, 2] == 0) & (filledvals[:, 2] == 0)
			if removedrows[rrsize] == True:
				zeropos = np.where(removedrows == True)[0][0]
				filledvals = filledvals[zeropos:xrangeval, :]
		if quadval == 4:
			removedrows = (filledvals[:, 1] - filledvals[:, 2] == 0) & (filledvals[:, 2] == imdim[1])
			if removedrows[rrsize] == True:
				zeropos = np.where(removedrows == True)[0][0]
				filledvals = filledvals[0:zeropos+1, :]


		for i in range(np.shape(filledvals)[0]):
			filledvals[i, 1:3] = np.sort(filledvals[i, 1:3])
			a0 = int(filledvals[i][0])
			a1 = int(filledvals[i][1])
			a2 = int(filledvals[i][2])

			img_out[a1:a2+1, a0] = img_out[a1:a2+1, a0] + 2

	if extensionflag == 0:
		if quadval == 1:
			img_out[:, 0:j_p] = 0
			img_out[0:i_p, :] = 0
		if quadval == 2:
			img_out[0:i_p, :] = 0
			img_out[:, (j_p+1):imdim[1]] = 0
		if quadval == 3:
			img_out[(i_p+1):imdim[0], :] = 0
			img_out[:, 0:j_p] = 0
		if quadval == 4:
			img_out[(i_p+1):imdim[0], :] = 0
			img_out[:, (j_p+1):imdim[1]] = 0
	
	img_out[i_c,j_c] = 1
	img_out[img_out > 0] = 1
	return(img_out)










