from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import array
from random import *
import pandas as pd
import matplotlib.pyplot as plt
from math import log10, sqrt
from PIL import Image
from matplotlib import cm
import statistics


PATH="/home/amani/Desktop/myproject/images/"
IMAGE_PATH=""

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


def read_pgm(path):
    with open(path, 'r') as f :
        pgm = f.read()
    image = np.array([x.split() for x in np.array(pgm.split('\n'))[4:]])
    return image.astype('int32')

def write_pgm(filename, matrice):
  height=matrice.shape[0]
  width=matrice.shape[1]
  data = ""
  for i in range(0, height):
    for j in range(0, width):
      data += str(matrice[i][j]) + " "
    data +="\n"
  fout = open(PATH+filename, "w")
  pgm_header = 'P2' + '\n' + str(width) + ' ' + str(height) + ' ' + str(255) + '\n'
  fout.write(pgm_header)
  fout.write(data)
  fout.close()


def apply_convolution(image, kernel):

    kernel = np.flipud(np.fliplr(kernel))    
    output = np.zeros_like(image)            
    
    image_padded = np.zeros((image.shape[0] + (kernel.shape[0]-1), 
                             image.shape[1] + (kernel.shape[1]-1)))   
    image_padded[(kernel.shape[0]//2):-(kernel.shape[0]//2), 
                 (kernel.shape[1]//2):-(kernel.shape[1]//2)] = image
    
    for x in range(image.shape[1]):     
        for y in range(image.shape[0]):
            
            output[y,x]=(kernel*image_padded[y:y + kernel.shape[0], x:x + kernel.shape[1]]).sum()
    return output


def moyenneur(size):
  return np.ones((size, size)) / size ** 2

def apply_linear_filter(path, filtre, filter_name=''):
  
  image = read_pgm(path)
  # print("original image : ", image)
  #image_bruit = bruit(image)
  # print("image bruitée : ", image_bruit) 
  #write_pgm(image.shape[0], image.shape[1], "noise_image.pgm", image_bruit)
  image_convolue = apply_convolution(image, filtre)
  # print("image convolue avec ce filtre : ", image_convolue)
  write_pgm('{}_image.pgm'.format(filter_name), image_convolue)

  return image_convolue



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if "save" in request.form.keys(): 
            image_name= request.form['save']
            global IMAGE_PATH
            IMAGE_PATH = PATH+image_name
            if image_name.split(".")[1]=="pgm":
                matrice=read_pgm(IMAGE_PATH)

        if "moyenneur" in request.form.keys() :
            apply_linear_filter(IMAGE_PATH,moyenneur(3),"moyenneur")
        return render_template("index.html", image_path=IMAGE_PATH)
    else :
        return render_template("index.html" , image_path="")
   

@app.route('/moyenneur', methods=['POST', 'GET'])
def xxxx():
    if request.method == 'POST':
        apply_linear_filter(image_path, moyenneur(5),"moyenneur")

        return render_template("index.html", image_path=IMAGE_PATH)
    else :
        return render_template("index.html" , image_path="")
   
if __name__ == "__main__":
    app.run(debug=True)
