
def make_annotation_file(save_path, day_label, audio_feats, time_stamp, species):
  text_file_name = open(save_path, 'w+')
  text_file.write("Selection\t View\t	Channel\t	Begin Time (S)\t End Time (S)\t	Low Freq (Hz)\t	High Freq (Hz)"
  row_count = 