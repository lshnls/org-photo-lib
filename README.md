# Copy/Movie Images and Videos with Date Taken or Creation Date

# Purpose: Copy/Move image and video files in a folder based on date photo taken (from EXIF metadata) or video creation date.

# Author: Lysukhin Ilya
# Update: 20250611

# Usage: python.exe rename.py input-folder output-folder
#   - input-folder = the directory containing the image files to be copied/movied
#   - output-folder =  the directory to which they images will be copied/movied

# Examples: python.exe rename.py copy /home/Images/src /home/images/dest
#           python.exe rename.py move /home/Images/src /home/images/dest

# Behavior:
#  - Given a photo named "Photo-May-001.jpg"  
#  - with EXIF date taken of "5/1/2025 12:01:00 PM"  
#  - when you run this script on its parent folder
#  - then it will be copy/move to "/<output-folder>/2025/2025-05/20250501-120100.jpg"

# Notes:
#   - For safety, please make a backup of your photos before running this script
#   - Currently only designed to work with .jpg, .jpeg, .png, mp4, .mov, and .avi files
#   - If you omit the input folder, then the current working directory will be used instead.
