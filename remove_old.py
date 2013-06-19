#!/usr/bin/env python

import os
import time
from colorama import Fore
import shutil

# Function to compare and remove files

def removeOldFile(defDir, f):
	""" We take as input the directory and the file to check
	    and we check if the file is older than 31 days.
	    If yes, we remove the file """

	fileTime = os.path.getmtime(defDir+f)
	if (now - fileTime) > 2678400:
		shutil.rmtree(defDir+f)
		print("\033[31m" + "File {} removed").format(defDir+f)
		print("\033[0m") # and reset to default color
	else:
		print("\033[32m" + "File {} kept").format(defDir+f)
		print("\033[0m") # and reset to default color)




defaultDir = "/home/plambri/"
defaultSxComDir = defaultDir+"sxarchive/ereports/"
defaultSxExtDir = defaultDir+"sxarchive/creports/"
defaultTicketDir = defaultDir+"Tickets/"

now = time.time()

dirList=os.listdir(defaultSxComDir)

for fname in dirList:
	removeOldFile(defaultSxComDir, fname)

dirList=os.listdir(defaultSxExtDir)

for fname in dirList:
	removeOldFile(defaultSxExtDir, fname)

dirList=os.listdir(defaultTicketDir)

for fname in dirList:
	removeOldFile(defaultTicketDir, fname)




