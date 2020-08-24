
def make_annotation_file(save_path, day_label, time_stamp, species):
  text_file = open(save_path, 'w+')
  text_file.write("Selection\t View	Channel	Begin Time (S)\t End Time (S)	Low Freq (Hz)	High Freq (Hz)\t Species\n")
  row_count = species.shape[0]
  for row in range(row_count):
    if species[row][0] != 'NOISE':
      begin_time = round(0.960 * row, 3)
      end_time = round(begin_time + 0.960, 3)
      low_freq = 200
      high_freq = 8000
      row_input = "{}\t Spectrogram 1\t 1\t {}\t {}\t {}\t {}\t {}\n".format(row + 1, begin_time, end_time, low_freq, high_freq, species[row][0])
      text_file.write(row_input)
  return text_file