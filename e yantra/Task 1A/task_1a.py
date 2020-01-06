
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1A of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Team ID:		3523	[ Team-ID ]
# Author List:		Harsh Thakur [ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1a.py
# Functions:		readImage, solveMaze, make_list, check_maze, valid, find_end
# 					[ Comma separated list of functions in this file ]
# Global variables:	CELL_SIZE
# 					[ List of global variables defined in this file ]


# Import necessary modules
# Do not import any other modules
import cv2
import numpy as np
import os


# To enhance the maze image
import image_enhancer


# Maze images in task_1a_images folder have cell size of 20 pixels
CELL_SIZE = 20


def readImage(img_file_path):

	"""
	Purpose:
	---
	the function takes file path of original image as argument and returns it's binary form

	Input Arguments:
	---
	`img_file_path` :		[ str ]
		file path of image

	Returns:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path

	Example call:
	---
	original_binary_img = readImage(img_file_path)

	"""

	binary_img = None

	#############	Add your Code here	###############
	path = img_file_path
	
	# print(path)
	original_image = cv2.imread(img_file_path)
	cv2.imshow('Original', original_image)
	
	'''
	for i in range(9):
		for j in range(9):
			print(original_image[i][j], end=" ")
		print()
	'''
	
	binary_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	ret, binary_img = cv2.threshold(binary_img, 10, 255, cv2.THRESH_BINARY)
	
	#cv2.imshow('binary_img', binary_img)
	#cv2.waitKey(0)
	cv2.destroyAllWindows()

	###################################################

	return binary_img


def make_list(add, shortestPath, initial_point):
	#print(type(shortestPath))
	
	length_add = len(add)
	i = initial_point[0]
	j = initial_point[1]	
	
	shortestPath.append(tuple((i, j)))
	
	for a in range(length_add):
		move = add[a]
		if move == "L":
			j = j - 1
			
		elif move == "R":
			j = j + 1
	
		elif move == "U":
			i = i - 1
	
		elif move == "D":
			i = i + 1
			
		shortestPath.append(tuple((i, j)))
	
	# print(shortestPath)
	# print("Length = ", len(shortestPath))
		
	return shortestPath
		


def check_maze(original_binary_img, moves, i, j, flag):
	# print()
	# print("In check line")
	if flag == 0:
		j = j + CELL_SIZE//2		
		for a in range(i-6, i+6):
			# This condition is if it found a black line
			if original_binary_img[a][j] == 0:
				return True
		return False
		
	if flag == 1:
		# print("I = ", i)
		# print("J = ", j)
		j = j - CELL_SIZE//2
		# print("J = ", j)
		for a in range(i-6, i+6):
			# print("I = ", a, end=" ")
			# print(original_binary_img[a][j])
			# This condition is if it found a black line
			if original_binary_img[a][j] == 0:
				return True
		return False
		
	if flag == 2:
		i = i + CELL_SIZE//2
		for a in range(j-6, j+6):
			# This condition is if it found a black line
			if original_binary_img[i][a] == 0:
				return True
		return False
		
	if flag == 3:
		# print("I = ", i)
		# print("J = ", j)
		i = i - CELL_SIZE//2
		# print("I = ", i)
		for a in range(j-6, j+6):
			# print("J = ", a, end=" ")
			# print(original_binary_img[i][a])
			# This condition is if it found a black line
			if original_binary_img[i][a] == 0:
				return True
		return False

def valid(original_binary_img, moves, initial_point, final_point):
	height, width = original_binary_img.shape
	
	i = ( initial_point[0] * 20 ) + 10
	j = ( initial_point[1] * 20 ) + 10
	
	a = ( final_point[0] * 20 ) + 10
	b = ( final_point[1] * 20 ) + 10
	
	for move in moves:
		if move == "L":
			j = j - CELL_SIZE
			flag = 0
			
		elif move == "R":
			j = j + CELL_SIZE
			flag = 1
			
		elif move == "U":
			i = i - CELL_SIZE
			flag = 2
			
		elif move == "D":
			i = i + CELL_SIZE
			flag = 3
			
		if not(0 <= i <= a and 0 <= j <= b):
			# print("F len")
			return False
			
		elif( check_maze(original_binary_img, moves, i, j, flag) ):
			# print("F bin")
			return False
	# print("T")
	return True
	 
def find_end(original_binary_img, add, initial_point, final_point):
	height, width = original_binary_img.shape
	i = ( initial_point[0] * 20 ) + 10
	j = ( initial_point[1] * 20 ) + 10
	
	a = ( final_point[0] * 20 ) + 10
	b = ( final_point[1] * 20 ) + 10
	 
	for move in add:
		if move == "L":
			j = j - CELL_SIZE
			
		elif move == "R":
			j = j + CELL_SIZE
	
		elif move == "U":
			i = i - CELL_SIZE
	
		elif move == "D":
			i = i + CELL_SIZE
	# print("I = ", i)
	# print("J = ", j)
	
	if i == a and j == b:
	 	# print("Found: ", add)
	 	# print("Length: ", len(add))
	 	return True
	 	
	return False

def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):

	"""
	Purpose:
	---
	the function takes binary form of original image, start and end point coordinates and solves the maze
	to return the list of coordinates of shortest path from initial_point to final_point

	Input Arguments:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path
	`initial_point` :		[ tuple ]
		start point coordinates
	`final_point` :			[ tuple ]
		end point coordinates
	`no_cells_height` :		[ int ]
		number of cells in height of maze image
	`no_cells_width` :		[ int ]
		number of cells in width of maze image

	Returns:
	---
	`shortestPath` :		[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Example call:
	---
	shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

	"""
	
	shortestPath = []

	#############	Add your Code here	###############
	
	height, width = original_binary_img.shape
	# print("Height = ", height)
	# print("Width = ", width)
	
	# print(no_cells_height)
	# print(no_cells_width)
	# print(initial_point)
	# print(final_point)
	
	
	#create_maze(original_binary_img, initial_point, final_point)
	
	'''
	contours, hierarchy = cv2.findContours(original_binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	print(len(contours))
	
	
	cv2.drawContours(original_binary_img, contours, -1, (0,255,0), 2)
	
	cv2.imshow('image',original_binary_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	'''
	
	
	'''
	a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
	print()
	print()
	for i in range(height):
		for j in range(width):
			if (i+2) % 20 == 0 and (j+2) % 20 == 0: 
				print(original_binary_img[i][j], end=" ")
		if (i+2) % 20 == 0:
			print()
	'''
	
	'''
	print()
	print()	
	for i in range(160, 200):
		for j in range(160, 200):
			print(original_binary_img[i][j], end=" ")
		print()
	'''
	
	num = []
	num.append("")
	add = ""
	
	#a = 0
	while not find_end(original_binary_img, add, initial_point, final_point):
		#print()
		#print("A = ", a)
		#a = a + 1		
		#print("length = ", len(add))
		#print(num)
		add = num.pop(0)
		for j in ["U", "D", "L", "R"]:
			flag = 0
			put = add + j
			#print("Put = ", put)
			length_put = len(put)
			#print("Length PUT = ", length_put)
			if length_put > 1:
				var_1 = put[length_put - 1]
				var_2 = put[length_put - 2]
				
				var_check = var_1 + var_2
				if var_check == "LR" or var_check == "RL" or var_check == "UD" or var_check == "DU":
					flag = 1
				
						
			if valid(original_binary_img, put, initial_point, final_point) and flag == 0:
				num.append(put)
		#if a == 1000:
		#	break
	
	# print("Num ", add)
	# print("Length = ", len(add))
	
	shortestPath = make_list(add, shortestPath, initial_point)
	
	###################################################
	
	return shortestPath


#############	You can add other helper functions here		#############



#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling readImage
# 					and solveMaze functions, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1a_images' folder or not

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1a_images/'				# path to directory of 'task_1a_images'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()
	
	no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
	no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
	initial_point = (0, 0)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
	
	print('\n============================================')
	
	cv2.imshow('canvas0' + str(file_num), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()
			
			no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
			no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
			
			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
	else:

		print('')


