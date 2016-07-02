'''
author - diwakargrandhi
version - python3
documentation links -
# minidom parsing
## http://www.mkyong.com/python/python-read-xml-file-dom-example/
## http://muktvijay.blogspot.in/2013/04/how-to-parse-xml-in-python-using-minidom.html
# dom official documentation - https://docs.python.org/2/library/xml.dom.html#module-xml.dom
key decisions - 
# we went with dom to parse the xml instead of element tree because of the complications with namespaces
'''

import argparse
import logging
import os
import shutil
import sys
import zipfile

from xml.dom import minidom
from xml.parsers.expat import ExpatError

# global defaults
temp_folder_name = "temp"
imsmanifest_file_name = "imsmanifest.xml"
file_extension_zip = "zip"
structured_suffix = "-structured"

logging.basicConfig(filename='logs/convert_imscc.log', 
					filemode='w', 
					level=logging.DEBUG,
					format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
logger = logging.getLogger()

def create_directory(directory_path):
	if not os.path.exists(directory_path):
		logger.debug("Created the {0} folder.".format(directory_path))
		os.makedirs(directory_path)

# If the destination is an existing directory, then src is moved inside that directory
# If the destination already exists but is not a directory, it may be overwritten 
def move_directory(src_path, dst_path):
	if os.path.exists(dst_path) and os.path.isdir(dst_path):
		logger.debug("Moving directory from {0} to {1}".format(src_path, dst_path))
		shutil.move(src_path, dst_path)

def delete_directory(directory_path):
	if os.path.exists(directory_path):
		logger.debug("Deleting directory {0}".format(directory_path))
		shutil.rmtree(directory_path)

def rename_directory(directory_path, new_dir_name):
	logger.debug("rename_directory API, directory_path: {0}".format(directory_path))
	logger.debug("rename_directory API, new_dir_name: {0}".format(new_dir_name))
	if os.path.exists(directory_path):
		path, filename = os.path.split(directory_path)
		new_path = os.path.join(path, new_dir_name)
		logger.debug("Renaming directory from {0} to {1}".format(directory_path, new_path))
		os.rename(directory_path, new_path)

def copy_file(src_file_path, dst_folder_path, dst_file_name):
	create_directory(dst_folder_path)
	
	src_file_name = os.path.basename(src_file_path)
	logger.debug("src_file_name is {0}".format(src_file_name))
	
	# Using the destination file name if it is provided explicitly
	if dst_file_name != None and dst_file_name.strip() != "":
		dst_file_path = os.path.join(dst_folder_path, dst_file_name)
	else:
		dst_file_path = os.path.join(dst_folder_path, src_file_name)

	if os.path.isfile(src_file_path):
		shutil.copyfile(src_file_path, dst_file_path)
		logger.debug("Copied the {0} file to {1} location.".format(src_file_path, dst_file_path))
	else:
		logger.debug("Did not find any file at {0}".format(src_file_path))
	return dst_file_path

def get_file_name_without_ext(file_path):
	file_name_without_extension = ""
	if os.path.isfile(file_path):
		file_name = os.path.basename(file_path)
		file_name_without_extension = os.path.splitext(file_name)[0]
		logger.debug("For path {0}, the file name is: {1}.".format(file_path, file_name_without_extension))
	else:
		logger.debug("Given file {0} doesnt exist.".format(file_path))
	return file_name_without_extension

def rename_file_change_extension(file_path, new_extension):
	new_file_path = ""
	if os.path.isfile(file_path):
		file_name_without_extension = get_file_name_without_ext(file_path)
		file_folder_path = os.path.dirname(file_path)
		new_file_path = os.path.join(file_folder_path, file_name_without_extension + "." + new_extension)
		os.rename(file_path, new_file_path)
		logger.debug("Renamed {0} file to {1} file.".format(file_path, new_file_path))
	else:
		logger.debug("Given file {0} doesnt exist.".format(file_path))
	return new_file_path

def unzip(src_file_path):
	file_name_without_extension = get_file_name_without_ext(src_file_path)
	src_dir_path = os.path.dirname(src_file_path)
	dst_dir_path = os.path.join(src_dir_path, file_name_without_extension)
	with zipfile.ZipFile(src_file_path) as zf:
		zf.extractall(dst_dir_path)
	return dst_dir_path

def get_xml_data(file_path):
	xml_data = ""
	try:
		xml_data = minidom.parse(file_path)
	except ExpatError as e:
		logger.error("Error while reading xml from {0}.".format(file_path), exc_info=True)
	
	return xml_data

def process_file(file_name, src_dir_path, dst_dir_path, dst_file_name):
	src_file_path = os.path.join(src_dir_path, file_name)
	copy_file(src_file_path, dst_dir_path, dst_file_name)

def does_any_attribute_match_given_list_of_names(xml_element, attr_name_list):
	is_attr_name_matching_given_name = False
	if xml_element.hasAttributes():
		for attr_name in attr_name_list:
			if xml_element.hasAttribute(attr_name):
				is_attr_name_matching_given_name = True
				break
	return is_attr_name_matching_given_name

def does_any_child_nodes_match_given_node_name(xml_element, node_name):
	is_child_node_matching_given_name = False
	if xml_element.hasChildNodes():
		for child_element in xml_element.childNodes:
			child_node_name = child_element.nodeName
			if child_node_name != None and child_node_name == node_name:
				is_child_node_matching_given_name = True
				break
	logger.debug("is_child_node_matching_given_name being returned is {0}".format(str(is_child_node_matching_given_name)))
	return is_child_node_matching_given_name

def process_node(xml_element, resources_data, src_dir_path, dst_dir_path):
	logger.debug("XML element obtained is: {0}".format(xml_element.toprettyxml(indent = '  ').encode('utf-8').strip()))

	src_folder_identifier = xml_element.getAttribute('identifierref')
	logger.debug("src_folder_identifier obtained is: {0}".format(src_folder_identifier))
	new_src_dir_path = os.path.join(src_dir_path, src_folder_identifier)
	
	# We need to get the title which is an immediate childNode
	logger.debug("title node obtained is: {0}".format(xml_element.getElementsByTagName('title')[0].toprettyxml(indent = '  ')))
	title = xml_element.getElementsByTagName('title')[0].firstChild.nodeValue

	if does_any_child_nodes_match_given_node_name(xml_element, 'item'):
		# If there are further children in the xml tag with item as tag name, it means that this is a folder
		
		new_dst_dir_path = os.path.join(dst_dir_path, title)

		logger.info("Processing folder: {0}".format(title))
		logger.info("Source Path: {0}".format(new_src_dir_path))
		logger.info("Destination Path: {0}".format(new_dst_dir_path))
		create_directory(new_dst_dir_path)
		for each_item in xml_element.childNodes:
			if each_item.nodeName == 'item':
				process_node(each_item, resources_data, new_src_dir_path, new_dst_dir_path)
	else:
		resources_list = filter(lambda x: x.get('identifier') == src_folder_identifier, resources_data)
		if len(resources_list) > 0:
			file_name = resources_list[0].get('filename')
			file_name_without_ext = get_file_name_without_ext(file_name)
			ext = os.path.splitext(file_name)[1]
			
			dst_file_name = file_name
			if file_name_without_ext == src_folder_identifier:
				# In this case, instead of using the identifier, let's use the more meaningful title
				dst_file_name = title + ext
			
			logger.info("Processing file: {0}".format(file_name))
			logger.info("Source Path: {0}".format(new_src_dir_path))
			logger.info("Destination Path: {0}".format(dst_dir_path))
			logger.info("Destination File Name: {0}".format(dst_file_name))
			process_file(file_name, new_src_dir_path, dst_dir_path, dst_file_name)
		else:
			logger.error("Error in processing file: {0}".format(title))

def get_list_of_dicts_for_resources_info(resources_root_element):
	logger.info("Started building the resources information.")
	list_of_dicts_for_resources_info = []
	for each_resource in resources_root_element.getElementsByTagName('resource'):
		identifier = each_resource.getAttribute('identifier')
		href_info = each_resource.getElementsByTagName('file')[0].getAttribute('href')
		file_name = href_info.split('/')[-1]
		
		dicts_for_resources_info = {}
		dicts_for_resources_info['identifier'] = identifier
		dicts_for_resources_info['filename'] = file_name

		list_of_dicts_for_resources_info.append(dicts_for_resources_info)
		logger.debug("\nidentifier: {0}\nfilename: {1}".format(identifier, file_name))
	logger.info("Completed building the resources information.")
	return list_of_dicts_for_resources_info

def process_xml_data(xml_data, src_dir_path, dst_dir_path):
	organizations_root = xml_data.getElementsByTagName('organizations')[0]
	# This is useful to get the metadata of files. resources_data = [{"identifier":"abc","filename":"123"},{"identifier":"def","filename":"456"}]
	resources_root = xml_data.getElementsByTagName('resources')[0]
	resources_data = get_list_of_dicts_for_resources_info(resources_root)

	# Assuming that we have only a single organization in the xml
	# Easily extensible for multiple organizations by adding a for loop
	organization_element = organizations_root.getElementsByTagName('organization')[0]
	logger.debug("Obtained organization_element: " + str(organization_element))

	# the only node inside organization element will be the item node with attribute identifier set to root
	item_root = organization_element.childNodes[0]

	if(item_root.hasChildNodes()):
		has_atleast_one_item_node = does_any_child_nodes_match_given_node_name(item_root, 'item')
		if has_atleast_one_item_node:
			for child_item_node in item_root.childNodes:
				process_node(child_item_node, resources_data, src_dir_path, dst_dir_path)

# Main Program Logic
if __name__ == '__main__':

	logger.info("Starting convert_imscc_to_zip script.")

	parser = argparse.ArgumentParser(description='This script converts imscc files into folders with all the content; in the defined folder structure.')
	
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-f', '--file', nargs=1, help='Please provide the path to the imscc file.')
	group.add_argument('-l', '--list', nargs='*', help='Please provide the paths to a list of imscc files.')
	group.add_argument('-d', '--dir', nargs=1, help='Please provide the path to the directory containing imscc file(s).')

	parser.add_argument('-ll', '--loglevel', nargs=1, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Please provide the appropriate level to change the detail of logs.')

	args = parser.parse_args()

	list_of_imscc_files = []

	if(args.file):
		list_of_imscc_files.extend(args.file)
	elif(args.list):
		list_of_imscc_files.extend(args.list)
	elif(args.dir):
		path_folder = ''.join(args.dir)
		logger.info("Obtained args.dir: {0}".format(path_folder))
		for file in os.listdir(path_folder):
			if file.endswith('.imscc'):
				list_of_imscc_files.append(os.path.join(path_folder, file))
	
	if(args.loglevel):
		level = logging.getLevelName(''.join(args.loglevel))
		logger.setLevel(level)

	logger.info("Obtained the following list of files: {0}".format(''.join(list_of_imscc_files)))

	dir_path = os.path.dirname(os.path.abspath(__file__))
	temp_dir_path = os.path.join(dir_path, temp_folder_name)
	create_directory(temp_dir_path)

	for each_imscc_file in list_of_imscc_files:

		# Create a temporary folder where all the work can be done
		# Copy the provided file here
		# Rename the file to have a zip extension
		# Extract the zip folder
		# Create a tmp folder to store the structured data
		# Parse the imsmanifest file
		# Organize the content in the tmp folder
		# move the folder to the same location as the imscc file
		# rename the moved file
		# delete the tmp folder

		logger.info("Working on file: {0}".format(each_imscc_file))

		imscc_file_path = each_imscc_file	

		folder_of_imscc_path, imscc_file_name = os.path.split(imscc_file_path)
		imscc_file_name_without_ext = os.path.splitext(imscc_file_name)[0]

		imscc_file_in_tmp_path = copy_file(imscc_file_path, temp_dir_path, None)

		imscc_file_path_with_zip_ext = rename_file_change_extension(imscc_file_in_tmp_path, file_extension_zip)

		imscc_zip_file_extracted_path = unzip(imscc_file_path_with_zip_ext)

		tmp_folder_for_structured_data_path = imscc_zip_file_extracted_path + structured_suffix
		create_directory(tmp_folder_for_structured_data_path)

		imsmanifest_file_path = os.path.join(imscc_zip_file_extracted_path, imsmanifest_file_name)

		xml_data = get_xml_data(imsmanifest_file_path)
		
		process_xml_data(xml_data, imscc_zip_file_extracted_path, tmp_folder_for_structured_data_path)

		move_directory(tmp_folder_for_structured_data_path, folder_of_imscc_path)

		rename_directory(os.path.join(folder_of_imscc_path, imscc_file_name_without_ext + structured_suffix), imscc_file_name_without_ext)

	delete_directory(temp_dir_path)

	logger.info("Ending convert_imscc_to_zip script.")