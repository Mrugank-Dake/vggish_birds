
def make_annotation_file(save_path, day_label, time_stamp, species):
  text_file_name = open(save_path, 'w+')
  text_file.write("Selection\t View\t	Channel\t	Begin Time (S)\t End Time (S)\t	Low Freq (Hz)\t	High Freq (Hz)\n"
  row_count = species.shape[0]
  for row in row_count:
    begin_time = 0.960 * row
    end_time = begin_time + 0.960
    low_freq = 200
    high_freq = 8000
    row_input = "{}\t Spectrogram 1\t 1\t {}\t {}\t {}\t {}\n".format(row, begin_time, end_time, low_freq, high_freq)
    text_file.write("{row_input}")
  return text_file