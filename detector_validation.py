import os
import csv
import numpy as np

#annotation_file = 
detection_file = '/content/drive/My Drive/Sciurid Lab/CNN/VGGish_Birds/New annotations/FINI/02.txt'
#with open(annotation_file, 'r') as an:
#  begin_time_an = np.asarray([row_an[3] for row_an in csv.reader(an, delimiter = '\t')])
#  end_time_an = np.asarray([row_an[4] for row_an in csv.reader(an, delimiter = '\t')])
#  species_an = np.asarray([row_an[7] for row_an in csv.reader(an, delimiter = '\t')])

with open(detection_file, 'r') as dn:
  begin_time_dn = np.asarray([row_dn[3] for row_dn in csv.reader(dn, delimiter = '\t')])
  end_time_dn = np.asarray([row_dn[4] for row_dn in csv.reader(dn, delimiter = '\t')])
  species_dn = np.asarray([row_dn[7] for row_dn in csv.reader(dn, delimiter = '\t')])

detection_dict = {}
species_dn_unique = np.unique(species_dn)
for i in range(species_dn_unique.shape[0]):
  print(species_dn_unique)