import os
import csv
import numpy as np

days = ['02']
RF_NAME = 'ARU_annotations_no_overlap_smote_notes'
project_path = '/content/drive/My Drive/Sciurid Lab/CNN/VGGish_Birds/'
species_path = os.path.join(project_path, RF_NAME)
spec_dict = {'FINI': 'FINI', ' FINI': 'FINI', 'CUCE' : 'CUCE', ' CUCE' : 'CUCE', 'POHO' : 'POHO', ' POHO' : 'POHO', 'PHMA' : 'PHMA', ' PHMA' : 'PHMA', 'MOFA' : 'MOFA', ' MOFA' : 'MOFA', 'HYGA' : 'HYGA', ' HYGA' : 'HYGA', 'GASO' : 'GASO', ' GASO' : 'GASO'}
total_detections = {}
total_annotations = {}
tp = {}
fp = {}
fn = {}
precision = {}
recall = {}
F1 = {}
OMG_bored = ['CUCE', 'FINI', 'POHO', 'PHMA', 'HYGA', 'GASO', 'MOFA']
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
  ## Count total species detection for a day
  day_file = day + '.txt'
  detection_file = os.path.join(species_path, day_file)
  with open(detection_file, 'r') as dn:
    begin_time_dn = np.asarray([row_dn0[3] for row_dn0 in csv.reader(dn, delimiter = '\t')])[1:]
  begin_time_dn = np.asarray([float(time0) for time0 in begin_time_dn])
  with open(detection_file, 'r') as dn:  
    end_time_dn = np.asarray([row_dn1[4] for row_dn1 in csv.reader(dn, delimiter = '\t')])[1:]
  end_time_dn = np.asarray([float(time1) for time1 in end_time_dn])
  with open(detection_file, 'r') as dn:
    species_dn = np.asarray([row_dn2[7] for row_dn2 in csv.reader(dn, delimiter = '\t')])[1:]
  species_dn = np.asarray([spec_dict[sp] for sp in species_dn])
  species_dn_unique = np.unique(species_dn)
  for i in range(species_dn_unique.shape[0]):
    species = species_dn_unique[i]
    count = 0
    for j in range(species_dn.shape[0]):
      # Count detections of species
      if species_dn[j] == species:
        count+=1      
    total_detections[species] += count

  #*******************************************************************************#
  day_folder = day + '_Dec_2018'
  annotation_folder = os.path.join(project_path, 'New annotations/annotation_files', day_folder)
  rf_folder = os.path.join(species_path, day)
  annotation_files = os.listdir(annotation_folder)
  for annotation_file in annotation_files:
    annotation_file_path = os.path.join(annotation_folder, annotation_file)
    with open(annotation_file_path, 'r') as an:
      begin_time_an = np.asarray([row_an0[3] for row_an0 in csv.reader(an, delimiter = '\t')])[1:]
    begin_time_an = np.asarray([float(tm0) for tm0 in begin_time_an])
    with open(annotation_file_path, 'r') as an:
      end_time_an = np.asarray([row_an1[4] for row_an1 in csv.reader(an, delimiter = '\t')])[1:]
    end_time_an = np.asarray([float(tm1) for tm1 in end_time_an])
    with open(annotation_file_path, 'r') as an:
      species_an = np.asarray([row_an2[7] for row_an2 in csv.reader(an, delimiter = '\t')])[1:]
    species_an = np.asarray([sp.upper() for sp in species_an])
    for i in range(species_an.shape[0]):
      if species_an[i] == 'CCUE' or species_an[i] == 'CUC' or species_an[i] == 'CUCR' or species_an[i] == ' CUCE':
        species_an[i] = 'CUCE'
    
     
    rf_file = annotation_file[12:27] + annotation_file[-4:]
    rf_file_path = os.path.join(rf_folder, rf_file)
    with open(rf_file_path, 'r') as rn:
      begin_time_rn = np.asarray([row_rn0[3] for row_rn0 in csv.reader(rn, delimiter = '\t')])[1:]
    begin_time_rn = np.asarray([float(tm0p) for tm0p in begin_time_rn])
    with open(rf_file_path, 'r') as rn:
      end_time_rn = np.asarray([row_rn1[4] for row_rn1 in csv.reader(rn, delimiter = '\t')])[1:]
    end_time_rn = np.asarray([float(tm1p) for tm1p in end_time_rn])
    with open(rf_file_path, 'r') as rn:
      species_rn = np.asarray([row_rn2[7] for row_rn2 in csv.reader(rn, delimiter = '\t')])[1:]
    species_rn = np.asarray([spec_dict[sp] for sp in species_rn])
    
    for spec in OMG_bored:
      count1 = 0
      for j in range(species_an.shape[0]):
        # Count detections of species
        if species_an[j] == spec:
          count1 += 1 
      total_annotations[spec] += count1
    
    # Count true positives for species
    for i in range(begin_time_an.shape[0]):
      btan = begin_time_an[i]
      etan = end_time_an[i]
      for j in range(begin_time_rn.shape[0]):
        btrn = begin_time_rn[j]
        etrn = end_time_rn[j]
        if (btan <= btrn <= etan and btan <= etrn <= etan) or (btan <= btrn <= etan or btan <= etrn <= etan):
          if species_an[i] == species_rn[j]:
            tp[species_rn[j]] +=1

for omg in OMG_bored:
  if total_annotations[omg] > 0:
    if total_detections[omg] > 0:
      fp[omg] = total_detections[omg] - tp[omg]
      fn[omg] = total_annotations[omg] - tp[omg]
      precision[omg] = round(tp[omg]/total_detections[omg], 4)
      recall[omg] = round(tp[omg]/total_annotations[omg], 4)
      if precision[omg] + recall[omg] > 0:
        F1[omg] = round(2*precision[omg]*recall[omg] / (precision[omg] + recall[omg]), 4)
      else:
        F1[omg] = 100

val_file_name = species_path + '/detection_validation.txt'
text_file = open(val_file_name, 'w')
text_file.write("Species\t Annotations\t Detections\t TP\t FP\t FN\t Precison\t Recall\t F1\n")
for popo in OMG_bored:
  text_file.write(popo+'\t'+str(total_annotations[popo])+'\t'+str(total_detections[popo])+'\t'+str(tp[popo])+'\t'+str(fp[popo])+'\t'+str(fn[popo])+'\t'+str(precision[popo])+'\t'+str(recall[popo])+'\t'+str(F1[popo])+'\n')
text_file.close()