import os
f = r'C:\Users\Administrator\AppData\Local\Autodesk\3dsMax\2012 - 64bit'

import glob

ff = glob.glob(f+"\\*\\scripts\\startup")
print(ff)