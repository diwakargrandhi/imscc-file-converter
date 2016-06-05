# diwakargrandhi
# works with python 3

import logging
import os
import shutil
import xml.etree.ElementTree as ET
import zipfile

# user inputs
imscc_file_path = "/Users/rdiwakar/SLP/exports/Home-SLP-2016-LEAD-Section-1.imscc"

# global defaults
temp_folder_name = "temp"
imsmanifest_file_name = "imsmanifest.xml"
file_extension_zip = "zip"
structured_suffix = "-structured"

logging.basicConfig(filename='convert_imscc.log', 
					filemode='w', 
					level=logging.DEBUG,
					format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

def create_directory(directory_path):
	if not os.path.exists(directory_path):
	    os.makedirs(directory_path)
	    logging.debug("Created the {0} folder.".format(directory_path))

def copy_file(src_file_path, dst_folder_path):
	create_directory(dst_folder_path)
	src_file_name = os.path.basename(src_file_path)
	dst_file_path = os.path.join(dst_folder_path, src_file_name)
	if os.path.isfile(src_file_path):
		shutil.copyfile(src_file_path, dst_file_path)
		logging.debug("Copied the {0} file to {1} location.".format(src_file_path, dst_file_path))
	return dst_file_path

def get_file_name_without_ext(file_path):
	file_name_without_extension = ""
	if os.path.isfile(file_path):
		file_name = os.path.basename(file_path)
		file_name_without_extension = os.path.splitext(file_name)[0]
		logging.debug("For path {0}, the file name is: {1}.".format(file_path, file_name_without_extension))
	else:
		logging.debug("Given file {0} doesnt exist.".format(file_path))
	return file_name_without_extension

def rename_file_change_extension(file_path, new_extension):
	new_file_path = ""
	if os.path.isfile(file_path):
		file_name_without_extension = get_file_name_without_ext(file_path)
		file_folder_path = os.path.dirname(file_path)
		new_file_path = os.path.join(file_folder_path, file_name_without_extension + "." + new_extension)
		os.rename(file_path, new_file_path)
		logging.debug("Renamed {0} file to {1} file.".format(file_path, new_file_path))
	else:
		logging.debug("Given file {0} doesnt exist.".format(file_path))
	return new_file_path

def unzip(src_file_path):
	file_name_without_extension = get_file_name_without_ext(src_file_path)
	src_dir_path = os.path.dirname(src_file_path)
	dst_dir_path = os.path.join(src_dir_path, file_name_without_extension)
	with zipfile.ZipFile(src_file_path) as zf:
		zf.extractall(dst_dir_path)
	return dst_dir_path

# Main Program Logic
if __name__ == '__main__':
	
	# Create a temporary folder where all the work can be done
	# Copy the provided file here
	# Rename the file to have a zip extension
	# Extract the zip folder
	# Create a tmp folder to store the structured data
	# Parse the imsmanifest file

	dir_path = os.path.dirname(os.path.abspath(__file__))
	temp_dir_path = os.path.join(dir_path, temp_folder_name)
	create_directory(temp_dir_path)

	imscc_file_in_tmp_path = copy_file(imscc_file_path, temp_dir_path)

	imscc_file_path_with_zip_ext = rename_file_change_extension(imscc_file_in_tmp_path, file_extension_zip)

	imscc_zip_file_extracted_path = unzip(imscc_file_path_with_zip_ext)

	tmp_folder_for_structured_data_path = imscc_zip_file_extracted_path + structured_suffix
	create_directory(tmp_folder_for_structured_data_path)

	imsmanifest_file_path = os.path.join(imscc_zip_file_extracted_path, imsmanifest_file_name)

	xml_data = ET.parse(imsmanifest_file_path)
	root = xml_data.getroot()
	for child in root:
		