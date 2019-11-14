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
cleanedList = ''

cleanedDict = dict()

############### SETUP METHOD ###############
def setup():
  global inputTSV
  global outputFolder
  global cleanedList

  parser = argparse.ArgumentParser(description='Process MS Celeb TSV file')
  parser.add_argument('inputTSV', help='MS Celeb TSV to extract')
  parser.add_argument('outputFolder', help='Path to extract images to')
  parser.add_argument('-c', '--cleaned-list', help='Path to file with cleaned classifications', dest='cleanedList')
  args = parser.parse_args()

  inputTSV = os.path.normpath(args.inputTSV)
  outputFolder = os.path.normpath(args.outputFolder)
  cleanedList = os.path.normpath(args.cleanedList)

############### METHOD TO LOAD CLEANED DATA ###############
def loadCleanedData():
  with open(cleanedList) as file:
    line = file.readline()
    while line:
      parts = line.split(' ')
      parts[1].replace('/', os.path.sep)
      cleanedDict[parts[1]] = parts[0]

      line = file.readline()

def genFilename(entity, searchRank, faceId):
  return entity + os.path.sep + searchRank + "_" + faceId + ".jpg"

############### MAIN METHOD ###############
def main():

  if cleanedList != '' and cleanedList != None:
    print("Loading cleaned data list (this make take a LONG TIME)")
    loadCleanedData()
    print("Cleaned data list loaded!")

  fid = open(inputTSV, "r")
  if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

  with open(inputTSV, "r", encoding='utf-8') as fid:
    with open(outputFolder + os.path.sep + 'bboxes.txt', 'w') as bbox_file:
      while True:
        line = fid.readline()
        if line:
          data_info = line.split('\t')
          # 0: Freebase MID (unique key for each entity)
          # 1: ImageSearchRank
          # 4: FaceID
          # 5: bbox
          # 6: img_data
          filename = genFilename(data_info[0], data_info[1], data_info[4])
          bbox = struct.unpack('ffff', base64.b64decode(data_info[5]))
          bbox_file.write(filename + " "+ (" ".join(str(bbox_value) for bbox_value  in bbox)) + "\n")

          img_data = base64.b64decode(data_info[6])
          output_file_path = outputFolder + os.path.sep + filename

          if output_file_path in cleanedDict:
            orig_path = output_file_path
            output_file_path = outputFolder + os.path.sep + genFilename(cleanedDict[orig_path], data_info[1], data_info[4])
            del cleanedDict[orig_path]

          if os.path.exists(output_file_path):
            print(output_file_path + " exists")

          output_path = os.path.dirname(output_file_path)
          if not os.path.exists(output_path):
            os.mkdir(output_path)

          img_file = open(output_file_path, 'wb')
          img_file.write(img_data)
          img_file.close()
        else:
          break

############### DEFAULT ENTRYPOINT ###############
if __name__ == '__main__':
  setup()
  main()