#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
import os

from Homevee.Utils.Constants import DATA_DIR


def get_image_directory_path(directory_name):
	path = os.path.join(DATA_DIR, "images", directory_name)

	return path

def create_image(filename, directory_name, img_data, optimize=False):
	filename = filename + ".jpeg"

	rel_path = os.path.join("images", directory_name)

	abs_path = os.path.join(DATA_DIR, rel_path)

	if not os.path.exists(abs_path):
		os.makedirs(abs_path)

	file_path = os.path.join(abs_path, filename)

	#Logger.log(img_data)

	img_data = base64.b64decode(img_data)

	fh = open(file_path, "wb")
	fh.write(img_data)
	fh.close()

	if(optimize):
		optimize_image(file_path)

	return os.path.join(rel_path, filename)

def optimize_image(file_path):
	return