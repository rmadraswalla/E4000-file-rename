# E4000-file-rename
Rename image files for cleaning station

Place photos in `data/` folder.

**NOTE**: This script assumes that photos are taken in the following order:
  1) All TSH BEFORE
  2) All TSH AFTER

  Only 1 photo per TSH per Before/After stage, no other photos in between.

In Command Prompt window, type:
`cd Documents/Source/E4000-file-rename`

`python rename.py -f FIRST_PHOTONAME -l STATION_LETTER -n SESSION_NO -d DISTANCE_TRAVELLED`

For help screen, type:
`python rename.py -h`
