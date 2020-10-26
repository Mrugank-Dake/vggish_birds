import numpy as np

def make_annotation_file(save_path, species):
  low_freq_dict = {'FINI': 3000, 'CUCE': 2500, 'MOFA': 500, 'POHO': 500, 'PHMA': 3000, 'GASO': 500, 'HYGA': 2000, 'PYJO': 1500}
  high_freq_dict = {'FINI': 8000, 'CUCE': 6000, 'MOFA': 3500, 'POHO': 2500, 'PHMA': 7000, 'GASO': 2000, 'HYGA': 6500, 'PYJO': 5500}
  row_count = species.shape[0]
  #max_time_dict = {'FINI': 1.5, 'CUCE': 1.5, 'MOFA': 2.5, 'POHO': 2, 'PHMA': 1.5, 'NOISE': row_count}
  #min_time_dict = {'FINI': 0.2, 'CUCE': 0.2, 'MOFA': 0.2, 'POHO': 0.2, 'PHMA': 0.2, 'NOISE': 0}
  max_annotation_dict = {'FINI': 0, 'CUCE': 0, 'MOFA': 0, 'POHO': 0, 'PHMA': 0, 'GASO': 0, 'HYGA': 0, 'NOISE': row_count, 'PYJO': 0}
  
  #max_annotation_dict = {'FINI': 1, 'CUCE': 1, 'MOFA': 3, 'POHO': 2, 'PHMA': 1, 'GASO': 2, 'HYGA': 2, 'NOISE': row_count, 'PYJO': 1}
  text_file = open(save_path, 'w+')
  text_file.write("Selection\t View\t Channel\t Begin Time (S)\t End Time (S)\t Low Freq (Hz)\t High Freq (Hz)\t Species\n")
  annotation_count = 0
  row = 0
  while row < row_count:
    species_name = species[row][0]
    max_annotation_count = max_annotation_dict[species_name]
    #max_annotation_count = int(np.ceil(max_time_dict[species_name]/0.096))
    #min_annotation_count = int(np.ceil(min_time_dict[species_name]/0.096))
    skip = True
    skip_annotation_count = 1
    while skip == True:
      if row + skip_annotation_count < row_count and skip_annotation_count <= max_annotation_count:
        if species[row] ==  species[row + skip_annotation_count]:
            skip_annotation_count += 1
        else:
          skip = False
      else:
        skip = False
    #if skip_annotation_count <= min_annotation_count:
    #  species_name = 'NOISE'
    if species_name != 'NOISE':
      annotation_count += 1
      begin_time = round(0.0960 * row, 5)
      end_time = round(begin_time + skip_annotation_count * 0.0960, 5)
      low_freq = low_freq_dict[species_name]
      high_freq = high_freq_dict[species_name]
      row_input = "{}\t Spectrogram 1\t 1\t {}\t {}\t {}\t {}\t {}\n".format(annotation_count, begin_time, end_time, low_freq, high_freq, species_name)
      text_file.write(row_input)
    row += skip_annotation_count
  return text_file

def make_day_annotation_file(save_path, species, num_preds_file, duration_files):
  low_freq_dict = {'FINI': 3000, 'CUCE': 2500, 'MOFA': 500, 'POHO': 500, 'PHMA': 3000, 'GASO': 500, 'HYGA': 2000, 'PYJO': 1500}
  high_freq_dict = {'FINI': 8000, 'CUCE': 6000, 'MOFA': 3500, 'POHO': 2500, 'PHMA': 7000, 'GASO': 2000, 'HYGA': 6500, 'PYJO': 5000}
  #max_time_dict = {'FINI': 1.5, 'CUCE': 1.5, 'MOFA': 2.5, 'POHO': 2, 'PHMA': 1.5, 'NOISE': 1000000}
  #min_time_dict = {'FINI': 0.2, 'CUCE': 0.2, 'MOFA': 0.2, 'POHO': 0.2, 'PHMA': 0.2, 'NOISE': 0}
  max_annotation_dict = {'FINI': 1, 'CUCE': 1, 'MOFA': 3, 'POHO': 2, 'PHMA': 1, 'GASO': 2, 'HYGA': 3, 'NOISE': 1000000000, 'PYJO': 1}
  text_file = open(save_path, 'w+')
  text_file.write("Selection\t View\t Channel\t Begin Time (S)\t End Time (S)\t Low Freq (Hz)\t High Freq (Hz)\t Species\n")
  annotation_count = 0
  for file_count in range(len(duration_files) - 1):
    file_length = duration_files[file_count]
    species_in_file = species[file_count, 0, :]
    column_count = species_in_file.shape[0]
    column = 0
    while column < column_count:
      species_name = species_in_file[column]
      max_annotation_count = max_annotation_dict[species_name]
      #max_annotation_count = int(np.ceil(max_time_dict[species_name]/0.096))
      #min_annotation_count = int(np.ceil(min_time_dict[species_name]/0.096))
      skip = True
      skip_annotation_count = 1
      while skip == True:
        if column + skip_annotation_count < column_count and skip_annotation_count <= max_annotation_count:
          if species_in_file[column] ==  species_in_file[column + skip_annotation_count]:
              skip_annotation_count += 1
          else:
            skip = False
        else:
          skip = False
      #if skip_annotation_count <= min_annotation_count:
      #  species_name = 'NOISE'
      if species_name != 'NOISE':
        annotation_count += 1
        begin_time = round(0.0960 * column + file_length, 5)
        end_time = round(begin_time + skip_annotation_count * 0.0960, 5)
        low_freq = low_freq_dict[species_name]
        high_freq = high_freq_dict[species_name]
        row_input = "{}\t Spectrogram 1\t 1\t {}\t {}\t {}\t {}\t {}\n".format(annotation_count, begin_time, end_time, low_freq, high_freq, species_name)
        text_file.write(row_input)

      column += skip_annotation_count
  return text_file