# Created by fufufanatic

import subprocess
import os

def powershellHashToFile(target_directory):
    
    output_file = os.getcwd() + r'\hashes.txt'
    
    proc = subprocess.Popen(['powershell',
                  'Get-ChildItem -Recurse ' + target_directory
                  + '| Get-FileHash -Algorithm MD5' 
                  + '| Format-List -Property Path, Hash' 
                  + '| Out-File ' + output_file + ' -Encoding UTF8 -Width 9000'])
    
    proc.communicate() # Waits for powershell command to finish

def hashFileToList():
    
    path_hash_list = []    
    path_hash_file = os.getcwd() + r'\hashes.txt'
    
    with open(path_hash_file, 'r') as file:
        while True:
            line = file.readline()
            if line.startswith('Path'):
                path_hash = {}
                path_hash['path'] = line[7:-1]
                path_hash['hash'] = file.readline()[7:-1]
                path_hash_list.append(path_hash)
            if not line: #End-Of-File (EOF)
                break
    
    return path_hash_list

def duplicatesToFile(path_hash_list):
    
    duplicates_list = []    
    duplicates_file = os.getcwd() + r'\duplicates.txt'
    
    file = open(duplicates_file, 'w')    
    for path_hash in path_hash_list:
        if path_hash['path'] in duplicates_list:
            continue
        file.write('+ Checking: ' + path_hash['path'] + '\n')
        for other_path_hash in path_hash_list:
            if path_hash['hash'] == other_path_hash['hash'] and path_hash['path'] != other_path_hash['path']:
                file.write('- Duplicate Found!: ' + other_path_hash['path'] + '\n')
                duplicates_list.append(other_path_hash['path'])
        file.write('- CHECK DONE -\n\n')
    file.close()

def main():
    
    target_directory = r'C:\Users\fufufanatic\Music'
        
    powershellHashToFile(target_directory)
    path_hash_list = hashFileToList()
    duplicatesToFile(path_hash_list)
    
if __name__ == '__main__':
    main()