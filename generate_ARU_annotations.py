import time
start_time = time.time()
import pickle
import numpy as np
import os
import random
import wave
import contextlib
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import Binarizer
from imblearn.over_sampling import SMOTE 
from save_text import make_annotation_file, make_day_annotation_file
from imblearn.under_sampling import RandomUnderSampler
from analysis_libs_birds_with_noise import rf_classifier_aru, rf_classifier_aru_simple
NOISE = [3000, 5000, 10000, 15000, 20000, 25000]
TREES = [100, 300, 500, 1000]
DEPTH = [50, 80, 100, 120]
SAMPLESPLIT = [2, 5, 10, 15, 20, 50, 100]
max_depth = 50
samplesleaf = 1
bootstrap = True
randomstate = 0
classweight = None
for samplesplit in SAMPLESPLIT:
  for tree_count in TREES:
    for noise_value in NOISE:
      print('We are in samples split = {}, tree_count = {}, noise_value = {}'.format(samplesplit, tree_count, noise_value))
      days = ['02', '04', '30']
      Project_path = '/content/drive/My Drive/Sciurid Lab/CNN/VGGish_Birds/'
      threshold = 0.5
      # Load training data from pickle files
      path_here = os.path.join(Project_path, 'Data/october.pickle')
      with open(path_here, 'rb') as savef:
        audio_feats_data_training, species_training, num_vecs = np.transpose(np.array(pickle.load(savef)))
      BIRDS_LIST = []
      for i in range(audio_feats_data_training.shape[0]):
        toto = np.array(audio_feats_data_training[i], dtype = ('O')).astype(np.float)
        BIRDS_LIST.append(toto)
      BIRDS = np.array(BIRDS_LIST)
      
      clf = rf_classifier_aru(BIRDS, species_training, noise_value, tree_count, max_depth, samplesplit, samplesleaf, bootstrap, randomstate, classweight)
      #sm = SMOTE(random_state = 2)
      #X_train, y_train = sm.fit_sample(BIRDS, species_training)

      #rus = RandomUnderSampler(random_state=0)
      #X_train, y_train = rus.fit_resample(BIRDS, species_training)

      # Train regressor
      #species_training[species_training == 'NOISE'] = 'AAA'
      #enc = OneHotEncoder(categories = 'auto', sparse = False, handle_unknown = 'error')
      #y_train = enc.fit_transform(species_training.reshape(species_training.shape[0], 1))
        
      #clf = RandomForestClassifier(random_state=0, n_estimators=100)
      #clf.fit(BIRDS, species_training)

      # Load sound files for annotations
      for day in days:
        folder_name = Project_path + 'ARU_embeddings/no_overlap/' + day + '/'
        file_names = sorted(os.listdir(folder_name))
        #print(['We are on day ' + day])

        save_folder = Project_path + 'ARU_oct_annotations/' + str(noise_value) + 'noise_' + str(tree_count) + 'trees_classifier/'
        if not os.path.exists(save_folder):
          os.mkdir(save_folder)
        day_fold = save_folder + day +'/'
        if not os.path.exists(day_fold):
          os.mkdir(day_fold)
        
        #duration_files = [0]
        #num_preds = 0
        #species_prediction_day = []
        #num_preds_file = []
        #duration = 0
        
        # Make annotations
        for FILE in file_names:
          species_prediction = []
          pickle_file_path = os.path.join(folder_name, FILE)
          with open(pickle_file_path, 'rb') as savef:
            wtf = pickle.load(savef)
          day_label, audio_feats_data, time_stamp = wtf['day'], wtf['raw_audioset_feats_960ms'], wtf['time_stamp']
          predictions = clf.predict(audio_feats_data)
          #overlap_predictions = clf.predict(audio_feats_data)
          #predictions = Binarizer(threshold = threshold).fit_transform(predictions)
          #predictions_cat = enc.inverse_transform(predictions)
          #predictions_cat[predictions_cat == 'AAA'] = 'NOISE'
          #predictions_cat = predictions_cat.flatten()
          #species_prediction.append(predictions_cat)
          #predictions = []
          #for i in range(overlap_predictions.shape[0]):
          # if i >= 10:
          #   spec_detected_array = []
          #   for j in range(i - 9, i + 1):
          #     spec_detected_array.append(overlap_predictions[j])
          #   spec_detected = np.unique(np.asarray(spec_detected_array))
          #   if spec_detected.shape[0] == 1:
          #     predictions.append(spec_detected[0])
          #   else:
          #     predictions.append('NOISE')
          # else:
          #   spec_detected_array = []
          #   for j in range(0, i + 1):
          #     spec_detected_array.append(overlap_predictions[j])
          #   spec_detected = np.unique(np.asarray(spec_detected_array))
          #   if spec_detected.shape[0] == 1:
          #     predictions.append(spec_detected[0])
          #   else:
          #     predictions.append('NOISE') 
          predictions = np.asarray(predictions)
          #print(predictions.shape)
          species_prediction.append(predictions)
          species_prediction = np.transpose(np.asarray(species_prediction))
          #species_prediction_day.append(np.asarray(species_prediction))
          #species_prediction[species_prediction == 'AAA'] = 'NOISE'
          #num_preds += species_prediction.shape[0]
          #num_preds_file.append(num_preds)
          save_path = save_folder + day + '/' + time_stamp +  '.txt'
          make_annotation_file(save_path, species_prediction)
          
          #wav_file_path = os.path.join(Project_path, 'ARU_Test', day, FILE[:-7] + '.wav')
          #with contextlib.closing(wave.open(wav_file_path,'r')) as f:
          #  frames = f.getnframes()
          #  rate = f.getframerate()
          #duration += frames / float(rate)
          #duration_files.append(duration)
        
        #species_prediction_day = np.asarray(species_prediction_day)
        #save_path_day = save_folder + day + '.txt'
        #make_day_annotation_file(save_path_day, species_prediction_day, num_preds_file, duration_files)
print(time.time() - start_time)