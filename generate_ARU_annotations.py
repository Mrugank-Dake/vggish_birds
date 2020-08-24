import pickle
import numpy as np
import os
import random
from sklearn.ensemble import RandomForestClassifier
from save_text import make_annotation_file

days = ['02']
concatenated_pickle = []
Project_path = input('Project path: ')

# Load training data from pickle files
path_here = os.path.join(Project_path, 'Data/birds_with_noise_100.pickle')
with open(path_here, 'rb') as savef:
  birds = pickle.load(savef)
birds = np.transpose(np.array(birds))
audio_feats_data_training, species_training, num_vecs = birds
BIRDS_LIST = []
for i in range(audio_feats_data_training.shape[0]):
  toto = np.array(audio_feats_data_training[i], dtype = ('O')).astype(np.float)
  BIRDS_LIST.append(toto)
BIRDS = np.array(BIRDS_LIST)

# Train classifier
clf = RandomForestClassifier(random_state=0, n_estimators=100)
clf.fit(BIRDS, species_training)

# Load sound files for annotations
for day in days:
  folder_name = Project_path + 'ARU_embeddings_no_overlap/' + day + '/'
  file_names = os.listdir(folder_name)
  print(['We are on day ' + day]) 
  save_folder = Project_path + 'ARU_annotations_no_overlap/' + day + '/'
  if not os.path.exists(save_folder):
    os.mkdir(save_folder)
  
  # Make annotations
  for FILE in file_names:
    species_prediction = []
    with open(os.path.join(folder_name, FILE), 'rb') as savef:
      wtf = pickle.load(savef)
    day_label, audio_feats_data, time_stamp = wtf['day'], wtf['raw_audioset_feats_960ms'], wtf['time_stamp']
    average_size = 5
    feat = np.zeros((audio_feats_data.shape[0] - average_size + 1, 128))
    for feat_count in range(feat.shape[0]):
      for size in range(average_size):
        feat[feat_count] += audio_feats_data[feat_count + size]
      feat[feat_count] = feat[feat_count] / average_size
    species_prediction.append(clf.predict(feat))
    species_prediction = np.transpose(np.asarray(species_prediction))
    save_path = save_folder + time_stamp +  '.txt'
    make_annotation_file(save_path, day_label, time_stamp, species_prediction, average_size)