import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import collections

# Define a class to receive the characteristics of each line detection
class Line():
	def __init__(self, n):
		# was the line detected in the last iteration?
		self.detected = False  
		# x values of the last n fits of the line
		self.recent_xfitted = [] 
		#average x values of the fitted line over the last n iterations
		self.bestx = None     
		#polynomial coefficients averaged over the last n iterations
		self.best_fit = [np.array([0,0,0])]
		#polynomial coefficients for the most recent fit
		self.current_fit = collections.deque(maxlen=n)   

		#radius of curvature of the line in some units
		self.radius_of_curvature = None 
		#distance in meters of vehicle center from the line
		self.line_base_pos = None 
		#difference in fit coefficients between last and new fits
		self.diffs = np.array([0,0,0], dtype='float') 
		#x values for detected line pixels
		self.allx = None  
		#y values for detected line pixels
		self.ally = None

	def append_fit(self, fit):
		self.current_fit.append(fit)
		self.best_fit = np.mean(self.current_fit,axis=0)
		
		return(self.best_fit)
		
	def get_best_fit(self):
		return(self.best_fit)
