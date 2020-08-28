
def make_annotation_file(save_path, species):
  low_freq_dict = {'FINI': 3000, 'CUCE': 2500, 'MOFA': 500, 'POHO': 500, 'PHMA': 3000, 'GASO': 500, 'HYGA': 2000}
  high_freq_dict = {'FINI': 8000, 'CUCE': 6000, 'MOFA': 3500, 'POHO': 2500, 'PHMA': 7000, 'GASO': 2000, 'HYGA': 6500}
  row_count = species.shape[0]
  text_file = open(save_path, 'w+')
  text_file.write("Selection\t View	Channel	Begin Time (S)\t End Time (S)	Low Freq (Hz)	High Freq (Hz)\t Species\n")
  for row in range(row_count):
    species_name = species[row][0]
    if species_name != 'NOISE':
      begin_time = round(0.960 * row, 3)
      end_time = round(begin_time + 0.960, 3)
      low_freq = low_freq_dict[species_name]
      high_freq = high_freq_dict[species_name]
      row_input = "{}\t Spectrogram 1\t 1\t {}\t {}\t {}\t {}\t {}\n".format(row + 1, begin_time, end_time, low_freq, high_freq, species_name)
      text_file.write(row_input)
  return text_file

def make_day_annotation_file(save_path, species, duration):
  low_freq_dict = {'FINI': 3000, 'CUCE': 2500, 'MOFA': 500, 'POHO': 500, 'PHMA': 3000, 'GASO': 500, 'HYGA': 2000}
  high_freq_dict = {'FINI': 8000, 'CUCE': 6000, 'MOFA': 3500, 'POHO': 2500, 'PHMA': 7000, 'GASO': 2000, 'HYGA': 6500}
  row_count = species.shape[0]
  text_file = open(save_path, 'w+')
  text_file.write("Selection\t View	Channel	Begin Time (S)\t End Time (S)	Low Freq (Hz)	High Freq (Hz)\t Species\n")
  for row in range(row_count):
    species_name = species[row][0]
    if species_name != 'NOISE':
      begin_time = round(0.960 * row, 3)
      end_time = round(begin_time + 0.960, 3)
      low_freq = low_freq_dict[species_name]
      high_freq = high_freq_dict[species_name]
      row_input = "{}\t Spectrogram 1\t 1\t {}\t {}\t {}\t {}\t {}\n".format(row + 1, begin_time, end_time, low_freq, high_freq, species_name)
      text_file.write(row_input)
  return text_file