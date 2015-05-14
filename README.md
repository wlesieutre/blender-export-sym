# blender-export-sym

Blender export script for creating AGI32 symbol files (.sym) from mesh objects.

## Installation and Use

Download the io_export_sym.py script, and add it to blender with "Install from File..." in the Add-ons tab of the User Preferences window. Activate it with the checkbox on the right of the add-on listing.

Once installed and activated, the exporter can be found under File > Export > 

## Known Issues

The exporter doesn't export anything. But it's a planned feature!

## .sym File Format

A .sym file contains face data in two categories: luminous and housing. The two categories  have separate colors assigned in AGI, and the luminous faces are self-illuminating.

The .sym format is a simple text file listing the number of faces in each category, followed by the number of vertices in each face and the XYZ coordinates of those vertices. The following example is for a cube with the bottom face glowing:

ENTITY CUBE
LUMINOUS
1
4
 1  -1  -1
-1  -1  -1
-1   1  -1
 1   1  -1
HOUSING
5
4
 1  -1  -1
 1   1  -1
 1   1   1
 1  -1   1
4
 1   1  -1
-1   1  -1
-1   1   1
 1   1   1
4
-1   1  -1
-1  -1  -1
-1  -1   1
-1   1   1
4
-1  -1  -1
 1  -1  -1
 1  -1   1
-1  -1   1
4
 1   1   1
-1   1   1
-1  -1   1
 1  -1   1
ENDENTITY

It is not necessary that numbers be aligned, as long as there is whitespace between them.