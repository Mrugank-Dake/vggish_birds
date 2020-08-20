import pickle
import numpy as np
import os
import random
from sklearn.ensemble import RandomForestClassifier
from save_text import make_annotation_file

days = ['test']
concatenated_pickle = []
Project_path = input('Project path: ')
save_folder = Project_path + '/ARU_annotations/'

# Load training data from pickle files
path_here = os.path.join(Project_path, 'Data/birds_with_noise_100.pickle')
with open(path_here, 'rb') as savef:
  birds = pickle.load(savef)
birds = np.transpose(np.array(birds))
audio_feats_data, species, num_vecs = birds
BIRDS_LIST = []
for i in range(audio_feats_data.shape[0]):
  toto = np.array(audio_feats_data[i], dtype = ('O')).astype(np.float)
  BIRDS_LIST.append(toto)
BIRDS = np.array(BIRDS_LIST)
print(BIRDS.shape)
# Train classifier
clf = RandomForestClassifier(random_state=0, n_estimators=100)
clf.fit(BIRDS, species)

for day in days:
  folder_name = Project_path + 'ARU_embeddings_no_overlap/' + day + '/'
  file_names = os.listdir(folder_name)
  print(['We are on day ' + day]) 
  print(file_names)
  for FILE in file_names:
    with open(os.path.join(folder_name, FILE), 'rb') as savef:
      wtf = pickle.load(savef)
    day_label, audio_feats_data, time_stamp = wtf['day'], wtf['raw_audioset_feats_960ms'], wtf['time_stamp']
    species_prediction = []
    species_prediction.append(clf.predict(audio_feats_data))
    print(audio_feats_data.shape)
    species_prediction = np.transpose(np.asarray(species_prediction))
    print(species_prediction.shape)
    save_path = save_folder + day_label + '/' + time_stamp +  '.txt'
    make_annotation_file(save_path, day_label, time_stamp, species_prediction)
#save_folder = Project_path + '/Data/'    
#save_file_name = save_folder + 'birds_with_noise_100.pickle'
#with open(save_file_name, 'wb') as opo:
#  pickle.dump(concatenated_pickle, opo)