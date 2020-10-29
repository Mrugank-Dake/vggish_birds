import os
import csv
import numpy as np
#for classifier_type in array:
days = ['02', '04']
#RF_NAME = 'FINI'
project_path = '/content/drive/My Drive/Sciurid Lab/CNN/VGGish_Birds/ARU_oct_annotations/'
classifier_type = '2000noise_500trees_classifier'
#species_path = os.path.join(project_path, RF_NAME)
spec_dict = {'FINI': 'FINI', '': 'NS', ' ': 'NS', 'NS': 'NS', ' FINI': 'FINI', 'CUCE' : 'CUCE', ' CUCE' : 'CUCE', 'POHO' : 'POHO', ' POHO' : 'POHO', 'PHMA' : 'PHMA', ' PHMA' : 'PHMA', 'MOFA' : 'MOFA', ' MOFA' : 'MOFA', 'GASO' : 'GASO', ' GASO' : 'GASO', 'PYJO': 'PYJO', ' PYJO': 'PYJO'}
total_detections = {}
total_annotations = {}
tp = {}
fp = {}
fn = {}
precision = {}
recall = {}
F1 = {}
OMG_bored = ['CUCE', 'FINI', 'POHO', 'PHMA', 'GASO', 'MOFA', 'PYJO', 'NS']
for OMG in OMG_bored:
  tp[OMG] = 0
  total_detections[OMG] = 0
  total_annotations[OMG] = 0
  fp[OMG] = 0
  fn[OMG] = 0
  precision[OMG] = 1000
  recall[OMG] = 1000
  F1[OMG] = 1000


for day in days:
  #*******************************************************************************#
  detection_folder = os.path.join(project_path, classifier_type, day)
  annotation_folder = os.path.join(project_path, 'annotations', day)
  detection_files = sorted(os.listdir(detection_folder))
  time_array = np.arange(0, 300, 0.960)
  for detection_file in detection_files:
    detection_file_path = os.path.join(detection_folder, detection_file)
    with open(detection_file_path, 'r') as dn:
      begin_time_dn = np.asarray([row_dn0[3] for row_dn0 in csv.reader(dn, delimiter = '\t')])[1:]
    begin_time_dn = np.asarray([float(tm0) for tm0 in begin_time_dn])
    with open(detection_file_path, 'r') as dn:
      end_time_dn = np.asarray([row_dn1[4] for row_dn1 in csv.reader(dn, delimiter = '\t')])[1:]
    end_time_dn = np.asarray([float(tm1) for tm1 in end_time_dn])
    with open(detection_file_path, 'r') as dn:
      species_dn = np.asarray([row_dn2[7] for row_dn2 in csv.reader(dn, delimiter = '\t')])[1:]
    species_dn = np.asarray([spec_dict[sp] for sp in species_dn])
    
    annotation_file = '0009-SM4-03_' + detection_file[:-4] + '.Table.1.selections.txt'
    annotation_file_path = os.path.join(annotation_folder, annotation_file)
    if os.path.isfile(annotation_file_path):
      with open(annotation_file_path, 'r') as an:
        begin_time_an = np.asarray([row_an0[3] for row_an0 in csv.reader(an, delimiter = '\t')])[1:]
      begin_time_an = np.asarray([float(tm0p) for tm0p in begin_time_an])
      with open(annotation_file_path, 'r') as an:
        end_time_an = np.asarray([row_an1[4] for row_an1 in csv.reader(an, delimiter = '\t')])[1:]
      end_time_an = np.asarray([float(tm1p) for tm1p in end_time_an])
      with open(annotation_file_path, 'r') as an:
        if day == '30':
          species_an = np.asarray([row_an2[8] for row_an2 in csv.reader(an, delimiter = '\t')])[1:]
        else:
          species_an = np.asarray([row_an2[7] for row_an2 in csv.reader(an, delimiter = '\t')])[1:]
      species_an = np.asarray([spec_dict[sp.upper()] for sp in species_an])
      #print(species_dn.shape, begin_time_dn.shape)
      print(np.unique(species_an))
      for t in time_array:
        i_array = begin_time_dn[(begin_time_dn >= t - 0.0001) * (begin_time_dn <= t + 0.0001)]
        if len(i_array) != 0:
          print(species_dn.shape, begin_time_dn.shape)
          i = np.where(begin_time_dn == i_array[0])[0][0]
          print(i)
          btdn = begin_time_dn[i]
          etdn = end_time_dn[i]
          done = 0
          check = False
          while check == False:
            for j in range(begin_time_an.shape[0]):
              btan = begin_time_an[j]
              etan = end_time_an[j]
              if ((btdn < btan < etdn) or (btdn < etan < etdn) or (btan <= btdn and etan >= etdn)) and (species_dn[i] == species_an[j]):
                print("i = {}".format(i))                
                #if species_dn[i] == species_an[j]:
                #  print("tp = {}".format(i))
                done += 1
                tp[species_dn[i]] += 1
                begin_time_dn = np.delete(begin_time_dn, i)
                end_time_dn = np.delete(end_time_dn, i)
                species_dn = np.delete(species_dn, i)
                break
            break
          
        else:
          check = False
          while check == False:
            for j in range(begin_time_an.shape[0]):
              btan = begin_time_an[j]
              etan = end_time_an[j]
              if (t < btan < t+0.096) or (t < etan < t+0.096) or (btan <= t and etan >= t+0.096):
                fn[species_an[j]] += 1
                check = True
            check = True
      for t in time_array:
        i_array = begin_time_dn[(begin_time_dn >= t - 0.0001) * (begin_time_dn <= t + 0.0001)]
        if len(i_array) != 0:
          i = np.where(begin_time_dn == i_array[0])[0][0]
          btdn = begin_time_dn[i]
          etdn = end_time_dn[i]
          done = 0
          check = False
          while check == False:
            for j in range(begin_time_an.shape[0]):
              btan = begin_time_an[j]
              etan = end_time_an[j]
              if ((btdn < btan < etdn) or (btdn < etan < etdn) or (btan <= btdn and etan >= etdn)) and (species_dn[i] != species_an[j]):                
                done += 1
                fp[species_dn[i]] += 1
                fn[species_an[j]] += 1
                check = True
              check = True
            if done == 0:
              fp[species_dn[i]] += 1
    else:
      for sp in species_dn:
        fp[sp] += 1      
for omg in OMG_bored:
  prec_den = tp[omg] + fp[omg]
  if prec_den == 0:
    precision[omg] = 100
  else:
    precision[omg] = round(tp[omg]/(tp[omg] + fp[omg]), 4)
  recall[omg] = round(tp[omg]/(tp[omg] + fn[omg]), 4)
  #F1[omg] = round(2*precision[omg]*recall[omg] / (precision[omg] + recall[omg]), 4)
  if precision[omg] + recall[omg] > 0:
    F1[omg] = round(2*precision[omg]*recall[omg] / (precision[omg] + recall[omg]), 4)
  else:
    F1[omg] = 100

val_file_name = project_path + 'detector_validation/' + classifier_type + '.txt'
text_file = open(val_file_name, 'w')
text_file.write("Species\t TP\t FP\t FN\t Precison\t Recall\t F1\n")
for popo in OMG_bored:
  text_file.write(popo+'\t'+str(tp[popo])+'\t'+str(fp[popo])+'\t'+str(fn[popo])+'\t'+str(precision[popo])+'\t'+str(recall[popo])+'\t'+str(F1[popo])+'\n')
text_file.close()