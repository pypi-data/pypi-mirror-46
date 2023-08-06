import os, sys

files = [
'/Users/vt/Desktop/TEST/TEST.pdf',
'/Users/vt/Desktop/TEST/.DESDS',
'/Users/vt/Desktop/TEST/asd.IBM', 
]

for file in files:
    file_name = os.path.basename(file)
    suffix = os.path.splitext(file_name)[1] if not file_name.startswith('.') else os.path.splitext(file_name)[0]
    print(suffix)

