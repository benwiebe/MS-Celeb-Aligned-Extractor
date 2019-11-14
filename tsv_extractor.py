# Script to extract a MS-Celeb TSV file
# Forked from: https://github.com/modanesh/MS-Celeb-Aligned-Extractor
# 
# Fork Author: Ben Wiebe (https://github.com/benwiebe)
# Tested on Python 3.7.4

############### IMPORTS ###############
import os
import base64
import struct
import argparse

############### GLOBALS ###############
inputTSV = ''
outputFolder = ''

############### SETUP METHOD ###############
def setup():
  global inputTSV
  global outputFolder

  parser = argparse.ArgumentParser(description='Process MS Celeb TSV file')
  parser.add_argument('inputTSV', help='MS Celeb TSV to extract')
  parser.add_argument('outputFolder', help='Path to extract images to')
  args = parser.parse_args()

  inputTSV = os.path.normpath(args.inputTSV)
  outputFolder = os.path.normpath(args.outputFolder)

############### MAIN METHOD ###############
def main():
  fid = open(inputTSV, "r")
  if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

  with open(inputTSV, "r", encoding='utf-8') as fid:
    with open(outputFolder + '/bboxes.txt', 'w') as bbox_file:
      img_num = 1
      while True:
        line = fid.readline()
        if line:
          data_info = line.split('\t')
          # 0: Freebase MID (unique key for each entity)
          # 1: ImageSearchRank
          # 4: FaceID
          # 5: bbox
          # 6: img_data
          filename = data_info[0] + os.path.sep + data_info[1] + "_" + data_info[4] + ".jpg"
          bbox = struct.unpack('ffff', base64.b64decode(data_info[5]))
          bbox_file.write(filename + " "+ (" ".join(str(bbox_value) for bbox_value  in bbox)) + "\n")

          img_data = base64.b64decode(data_info[6])
          output_file_path = outputFolder + os.path.sep + filename 
          if os.path.exists(output_file_path):
            print(output_file_path + " exists")

          output_path = os.path.dirname(output_file_path)
          if not os.path.exists(output_path):
            os.mkdir(output_path)

          img_file = open(output_file_path, 'wb')
          img_file.write(img_data)
          img_file.close()

          # Print progress every 100 images to show we're still going
          if img_num % 100 == 0:
            print("%d images done" % img_num)

          img_num = img_num + 1

        else:
          break
  
  print("Done!")
############### DEFAULT ENTRYPOINT ###############
if __name__ == '__main__':
  setup()
  main()