## Synopsis

This repository has code to convert an **imscc** file to a folder with all the content in the defined folder structure.
Every imscc file will have the following,
* A list of folders - Each folder has just one file inside it.
* An xml (imsmanifest.xml) - This file contains information about the folder structure for all files. It also contains some metadata about the individual files.
* A folder named resources - It contains some files which were originally shared as resources in the course.

## Requirements

Python version - python 2

## Code Example

Using the script to convert a single imscc file.
* python convert_imscc_file.py -f "path_to_file"
* python convert_imscc_file.py --file "path_to_file"

Example:
```shell
* python convert_imscc_file.py -f "Users/diwakar/file1.imscc"
* python convert_imscc_file.py --file "Users/diwakar/file1.imscc"
```

Using the script to convert a list of imscc files.
* python convert_imscc_file.py -l "path_to_file" "path_to_file"
* python convert_imscc_file.py --list "path_to_file" "path_to_file"

Example:
```shell
* python convert_imscc_file.py -l "Users/diwakar/file1.imscc" "Users/diwakar/file2.imscc"
* python convert_imscc_file.py --list "Users/diwakar/file1.imscc" "Users/diwakar/file2.imscc"
```

Using the script to convert a list of imscc files which are present in one folder. This will consider imscc files which are present the immediate folder only.
* python convert_imscc_file.py -d "path_to_directory"
* python convert_imscc_file.py --dir "path_to_directory"

Example:
```shell
* python convert_imscc_file.py -d "Users/diwakar"
* python convert_imscc_file.py --dir "Users/diwakar"
```

**Note** Either one of the above three arguments are required for the script to function.

Using the script to change the log level. The default value is INFO whereas changing it to DEBUG will help gather more information. The values which are accepted by this parameter are DEBUG/INFO/WARNING/ERROR/CRITICAL.
* python convert_imscc_file.py -f "path_to_file" -ll DEBUG
* python convert_imscc_file.py --file "path_to_file" --loglevel DEBUG

Example:
```shell
* python convert_imscc_file.py -f "Users/diwakar/file1.imscc" -ll DEBUG
* python convert_imscc_file.py --file "Users/diwakar/file1.imscc" --loglevel DEBUG
```
**Note** The default value for this variable is INFO.

Using the script to change the final result. It can be a folder or a zip file. The resultant folder/file will be present in the same place as the source file. The values which are accepted by this parameter are zip/folder.
* python convert_imscc_file.py -f "path_to_file" -r zip
* python convert_imscc_file.py --file "path_to_file" --result zip

Example:
```shell
* python convert_imscc_file.py -f "Users/diwakar/file1.imscc" -r zip
* python convert_imscc_file.py --file "Users/diwakar/file1.imscc" --result zip
```
**Note** The default value for this variable is folder.

## Motivation

The imscc file extension is mainly related to Canvas by Instructure and used for one of its default file types. An imscc file contains exported course, that contains all the content and arrangement. Used for education purposes. 
The situation arised where the need was to convert an imscc file to a proper folder with all the content in order. Changing the extension to zip and unzipping the file provided all the files but couldn't maintain the folder structure. The solution was to have a script which could parse the imsmanifest file (which has the folder structure) and provide the required result.

## License

Code released under the [MIT license](https://github.com/diwakargrandhi/imscc-file-converter/blob/master/LICENSE).