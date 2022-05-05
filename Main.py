import os, sys, hashlib,shutil
import exifread
from pathlib import Path
from os import listdir
from os.path import isfile, join

input_files_path = r'C:\Users\kosrd\Desktop\Python Project\Input'
input_files = []
try:
    input_files = [f for f in listdir(input_files_path) if isfile(join(input_files_path, f))]
    input_files = [os.path.join(input_files_path, x) for x in input_files]
except FileNotFoundError:
    print("File Not Found-Please make Input File")
inp_dups = {}
unique_inps = {}
directory = "Prosseced"
parent_dir = "C:/Users/kosrd/Desktop/Python Project"
path = os.path.join(parent_dir, directory)

# main function in this file process inputs
def Processed(input_files):
    all_inps={}
    for file_path in input_files:
        if Path(file_path).exists():
            afile = open(file_path, 'rb')
            hasher = hashlib.md5()
            buf = afile.read()
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read()
            afile.close()
            files_hash=hasher.hexdigest()
            inp_dups[files_hash]=file_path
            all_inps[file_path] = files_hash
        else:
            print('%s is not a valid path, please verify' % file_path)
            sys.exit()

    for key in inp_dups.keys():
        if key not in unique_inps:
            unique_inps[key] = inp_dups[key]

    os.mkdir(path)

  #remove duplicate files  
    for file_name in all_inps:
        if all_inps[file_name] in unique_inps and file_name==unique_inps[all_inps[file_name]]:
            shutil.copy(file_name,path)
  #renamed
    count = 1
    directory = r'C:\Users\kosrd\Desktop\Python Project\Prosseced'
    for file in os.scandir(directory):
        fileName = ''.join(char for char in str(os.path.split(file.path)[-1]) if char.isalnum())
        fileName = ''.join(i for i in fileName if not i.isdigit())
        os.rename(file.path,str(os.path.dirname(file.path))+ '\\' + str(exifread.process_file(open(file.path, 'rb'), details = False)['Image DateTime']).replace(':', '_') + ' _ '+str(str(f'{count:04}')) +"_"+ str(fileName)+".jpg")
        count += 1
print("path of processed : "+path)
h = len([entry for entry in os.listdir(input_files_path) if os.path.isfile(os.path.join(input_files_path, entry))])
print("number of files in Input: ",h)
count_n=0
for root, subdirectories, files in os.walk(input_files_path):
    for file in files:
        count_n += 1
print("number of files in sub folders: ",count_n-h)

if __name__ == '__main__':
    Processed(input_files)