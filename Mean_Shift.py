# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import csv
import numpy as np
from sklearn.cluster import MeanShift
from sklearn.externals import joblib
# Set some parameters
F_n = 10 # Fold Count

# Images loading
def load_images_labels_RGB(img_folder, label_file):
    with open(label_file) as f:
        reader = csv.reader(f)
        next(reader) # skip header
        labels = []
        images = []
        for row in reader:
            img_filename = row[0]
            img = Image.open(os.path.join(img_folder,img_filename))
            if img is not None:
                images.append(np.array(img))
                labels.append(int(row[1]))
    return np.array(images), np.array(labels)

# Import data (normalized)
Img_Data, Label_Data = load_images_labels_RGB('train/', 'train.csv')
Size_Data = Img_Data.shape
Fold_size = Size_Data[0]//F_n
Mean_RGB = np.array([128.41563722, 115.24518493, 119.38645491])
Std_RGB = np.array([38.55379149, 35.64913446, 39.07419321])
Data_Norm = (Img_Data - Mean_RGB)/Std_RGB
Data_NFlat = np.reshape(Data_Norm, (Size_Data[0], 32*32*3))
# Shullf data
per = np.random.permutation(Data_Norm.shape[0])
Shuf_Data_Norm = Data_NFlat[per, :]
Shuf_Label_Data = Label_Data[per]

for i in range(F_n):
    DataN_te = Shuf_Data_Norm[Fold_size*i:Fold_size*(i+1), :]
    DataN_tr_1 = Shuf_Data_Norm[0:(Fold_size*i), :]
    DataN_tr_2 = Shuf_Data_Norm[Fold_size*(i+1):, :]
    DataN_tr = np.concatenate((DataN_tr_1,DataN_tr_2))
    DataN_te_y = Shuf_Label_Data[Fold_size*i:Fold_size*(i+1)]
    DataN_tr_y_1 = Shuf_Label_Data[0:(Fold_size*i)]
    DataN_tr_y_2 = Shuf_Label_Data[Fold_size*(i+1):]
    DataN_tr_y = np.concatenate((DataN_tr_y_1,DataN_tr_y_2))
    model_name_rbf = 'Model_' + str(i+1) + '_rbf.model'
    model_name_linear = 'Model_' + str(i+1) + '_linear.model'
    # Mean shift cluster
    clustering_Mf = MeanShift(n_jobs=-1)
    clustering_Mf.fit(DataN_tr)
    Cluster_predict = clustering_Mf.predict(DataN_te)
    print(Cluster_predict[0:40])
    '''
    score_rbf = clf_rbf.score(DataN_te,DataN_te_y)
    print("The score of rbf is : %f"%score_rbf)
    joblib.dump(clf_rbf, model_name_rbf)
    '''

