'''
# See https://github.com/sarabsethi/audioset_soundscape_feats_sethi2019/tree/master/calc_audioset_feats for installation instructions
'''

from AudiosetAnalysisBirds_ARU import AudiosetAnalysis
import os
import pickle

# Get all mp3 or wav files in our audio directory
#species = input('Species name: ')
#Project_path = input('Project path: ')
Project_path = '/content/drive/My Drive/Sciurid Lab/CNN/VGGish_Birds/'
Folder_name = input('02 or 04: ')
audio_dir = Project_path + 'ARU_Test/' + Folder_name +'/'
spec_dir = os.path.join(Project_path, 'ARU_embeddings/90_overlap', Folder_name)
if not os.path.exists(spec_dir):
  os.mkdir(spec_dir)
all_fs = os.listdir(audio_dir)
audio_fs = [f for f in all_fs if '.wav' in f.lower() or '.mp3' in f.lower()]

# Setup the audioset analysis
an = AudiosetAnalysis()
an.setup()

# Analyse each audio file in turn, and print the shape of the results
for f in audio_fs:
    path = os.path.join(audio_dir, f)
    results = an.analyse_audio(path)
    results['time_stamp'] = f[12:-4]
    results['day'] = Folder_name
    file_name_f = spec_dir + '/' + f[:-4] + '.pickle'
    with open(file_name_f, 'wb') as opo:
        pickle.dump(results, opo)

import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("mrugankdake@gmail.com", "MRUGank19@")
message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""
msg = """ From: Mrugank Colab <mrugank@gmail.com>
To: Mrugank Colab <mrugank@gmail.com>
Subject: SMTP e-mail test

Hi Mrugank, Mrugank here. ARU embeddings are ready."""

server.sendmail("mrugankdake@gmail.com", "mrugankdake@gmail.com", msg)
server.quit()