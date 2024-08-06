from flask import Flask, request, render_template
from PIL import Image
import os
filename = './static/dawn hill.jpg'
with Image.open(filename) as img:
    type = img.format
    filepath = img.filename
    width, height = img.size
    mode = img.mode

    file_size = os.path.getsize(filepath)
    file_name = os.path.basename(filepath)
    creation_date = os.path.getctime(filepath)
    modification_date = os.path.getmtime(filepath)
    print(mode,width,height,file_size,file_name,creation_date,modification_date)