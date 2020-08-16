import pickle
import numpy as np
import os
import random

species = ['CUCE', 'FINI', 'MOFA', 'POHO', 'Noise']
concatenated_pickle = []
Project_path = input('Project path: ')
for spp in species:
  folder_name = Project_path + 'bird_embeddings/' + spp + '/'
  file_names = os.listdir(folder_name)
  print(['We are in species ' + spp]) 
  print(file_names)
  if spp == 'Noise':
    file_names = random.sample(file_names, 100)
  for FILE in file_names:
    with open(os.path.join(folder_name, FILE), 'rb') as savef:
      wtf = pickle.load(savef)
      audio_feats_data, sp_name = wtf['raw_audioset_feats_960ms'], wtf['species']
    updated_audio_feats = np.mean(audio_feats_data, 0) # Conatenate calls for all the audio files
    num_vecs = audio_feats_data.shape[0] # Taking time information from file
    concatenated_pickle.append([updated_audio_feats, sp_name, num_vecs])

save_folder = Project_path + '/Data/'    
save_file_name = save_folder + 'birds_with_noise_100.pickle'
with open(save_file_name, 'wb') as opo:
  pickle.dump(concatenated_pickle, opo)