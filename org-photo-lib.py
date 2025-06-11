## Organize you photo library
#Copying or moving photos and video files in organized directories in chronological order
#
#Purpose: Copy/Move image and video files in a folder based on date photo taken (from EXIF metadata) or video creation date.
#
#Usage: python.exe org-photo-lib.py <copy|move> \<input-folder> \<output-folder>
#  - input-folder = the directory containing the image files to be copied/movied
#  - output-folder =  the directory to which they images will be copied/movied
#
# Examples: python.exe rename.py copy /home/Images/src /home/images/dest
#           python.exe rename.py move /home/Images/src /home/images/dest
#
## Behavior:
#  - Given a photo named "Photo-May-001.jpg"  
#  - with EXIF date taken of "5/1/2025 12:01:00 PM"  
#  - when you run this script on its parent folder
#  - then it will be copy/move to "output-folder/2025/2025-05/20250501-120100.jpg"
## Notes:
#   - For safety, please make a backup of your photos before running this script
#   - Currently only designed to work with .jpg, .jpeg, .png, mp4, .mov, and .avi files
#   - If you omit the input folder, then the current working directory will be used instead.

# Import libraries
import locale
import os
import sys
import shutil
#import random
#import filecmp
# import PIL
from datetime import datetime
#from turtle import goto
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

# Set list of valid commands and file extensions for images and videos
exec_commands = ["copy", "move"]
image_extensions = [".jpg", ".jpeg", ".png",".thm"]
cr2_extensions = [".cr2"]
video_extensions = [".mp4", ".mov", ".avi"]
all_extensions = image_extensions + video_extensions + cr2_extensions
files_deleted = 0
files_moved = 0
files_copied = 0

def copy_file(exec_command,filefrom,fileto):
    global files_deleted
    global files_moved
    global files_copied
    if fileto != filefrom:

        while os.path.exists(fileto):
            filesize=os.path.getsize(filefrom)
            if filesize == os.path.getsize(fileto):
                if exec_command == "move":
                    print("Files have some sizes",str(filesize)," "+fileto,"...remove source")
                    os.remove(filefrom)
                    files_deleted = files_deleted + 1
                    return 1
                elif exec_command == "copy":
                    print("Files have some sizes",str(filesize)," "+fileto,"...ignore")
                    return 1
            else:
                print("File exist:"+fileto)
                filename=os.path.splitext(os.path.basename(fileto))[0]
                ext=os.path.splitext(os.path.basename(fileto))[1]
                dir=os.path.dirname(fileto)
#                filename = filename + '#' + str(random.randrange(0, 100))
                #filename1 = filename + '(' + str(n) + ')'
                fileto = os.path.join(dir+'/', filename + '+' + ext)

        if exec_command == "copy":
            shutil.copy(filefrom, fileto)
            files_copied = files_copied + 1
        if exec_command == "move":
            shutil.move(filefrom, fileto)
            files_moved = files_moved + 1
    else:
           print(f"File '{fileto}' already named correctly")
    return 0

# Function to get the date from image EXIF data
def get_image_date(filepath):
    try:
        img = Image.open(filepath)
        exif_data = img._getexif()
        if exif_data:
            # EXIF DateTimeOriginal tag
            date_str = exif_data.get(36867)
            if date_str:
                return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error retrieving image date: {e}")
    return None

# Function to get the date from Canon raw CR2 image EXIF data
def get_cr2_date(filepath):
    try:
        img = Image.open(filepath)
        exif_data = img.getexif()
        if exif_data:
            # EXIF DateTimeOriginal tag
            date_str = exif_data.get(306)
            if date_str:
                #print(datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S"))
                return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error retrieving cr2 date: {e}")
    return None

# Function to get the date from video metadata
def get_video_date(filepath):
    try:
        parser = createParser(filepath)
        if not parser:
            print(f"Unable to parse video file: {filepath}")
            return None
        metadata = extractMetadata(parser)
        if metadata and metadata.has("creation_date"):
            return metadata.get("creation_date")
    except Exception as e:
        print(f"Error retrieving video date: {e}")
    return None

# Main function to rename files based on extracted date
def do_files(exec_command,input_folder,output_folder):
    for root, _, files in os.walk(input_folder):
        # cut off the directory name relative to the original path
        cutdir = root.replace(input_folder,'',1)
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            
            filepath = os.path.join(root, filename)
            if ext in all_extensions:
                
                # Get date based on file type
                if ext in image_extensions:
                    date = get_image_date(filepath)
                elif ext in video_extensions:
                    date = get_video_date(filepath)
                elif ext in cr2_extensions:
                    date = get_cr2_date(filepath)
                else:
                    continue

                # If a date was found, work with file
                # If a date was after 2000, work with file
                if date and date.year > 2000:
                    new_name = date.strftime("%Y%m%d-%H%M%S")
                    new_fold=output_folder+date.strftime("/%Y/%Y-%m")
                    new_filepath = os.path.join(new_fold+'/', new_name + ext)

                    os.makedirs(new_fold,exist_ok=True)
                    copy_file(exec_command,filepath,new_filepath)

                else:
                    print(f"No true date metadata found for '{filename}'")
                    new_filepath = os.path.join(output_folder+"/no-meta/"+cutdir+"/"+filename)

                    os.makedirs(output_folder+"/no-meta/"+cutdir,exist_ok=True)
                    copy_file(exec_command,filepath,new_filepath)
            else:
                print(f"Unknown format:'{filename}'")
                os.makedirs(output_folder+"/unknown-format/"+cutdir,exist_ok=True)
                new_filepath = os.path.join(output_folder+"/unknown-format/"+cutdir+'/'+filename)
                copy_file(exec_command,filepath,new_filepath)
                continue

# Entry point
if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] not in exec_commands or len(sys.argv[2])==0 or len(sys.argv[3])==0:
        print("Error in command arguments, enter a command like:\n" \
        "python rename.py copy|move input-folder output-folder")
        exit
    else:
        locale.setlocale(locale.LC_TIME, '')
        do_files(sys.argv[1],sys.argv[2],sys.argv[3])
        print("Files copied:",files_copied," moved:", files_moved," deleted:",files_deleted)

