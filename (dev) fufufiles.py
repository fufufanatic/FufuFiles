'''
Created by fufufanatic
fufufiles recursively searches through any Windows directory for duplicate files (results are printed to 'duplicates.txt')
'''

import subprocess
import os

# function to recursively compute hash of all files in a given Windows directory
def powershell_hash_to_file(target_directory):
    
    # output file is created in current working directory
    output_file = os.getcwd() + r'\hashes.txt'

    print('\n + Running Powershell subprocess (please, wait) ... \n')
    
    # runs powershell command to compute hash of all files in target directory and saves results to hashes.txt
    proc = subprocess.Popen(['powershell',
                  'Get-ChildItem -Recurse ' + target_directory
                  + '| Get-FileHash -Algorithm MD5' 
                  + '| Format-List -Property Path, Hash' 
                  + '| Out-File ' + output_file + ' -Encoding UTF8 -Width 9000'])
    
    proc.communicate() # waits for powershell command to finish

# function to parse previously created file-hash output document to a list (and return said list)    
def file_hash_to_list():
    
    file_hash_list = []    
    file_hash_doc = os.getcwd() + r'\hashes.txt'
    
    # opens file-hash document, then places file and hash pairs, as a dictionary item, in the final list ('file_hash_list')
    with open(file_hash_doc, 'r') as file:
        while True:
            line = file.readline()
            if line.startswith('Path'):
                file_hash = {}
                file_hash['path'] = line[7:-1]
                file_hash['hash'] = file.readline()[7:-1]
                file_hash_list.append(file_hash)
            if not line: #End-Of-File (EOF)
                break
    
    return file_hash_list

# function to search file-hash list for duplicate files (results are placed in 'duplicates.txt')
def duplicates_to_file(file_hash_list):
    
    duplicates_list = []
    duplicates_file = os.getcwd() + r'\duplicates.txt'
    
    with open(duplicates_file, 'w') as file:    
        for file_hash in file_hash_list:
            # if the file is already marked as a duplicate, then move on to the next file-hash pair in the list
            if file_hash['path'] in duplicates_list:
                continue
            print('+ Checking: ' + file_hash['path'] + '\n')
            # compare the current file-hash pair to every other pair in the list
            for other_file_hash in file_hash_list:
                # if the hashes are the same, but the file paths are different, we have a duplicate!
                if file_hash['hash'] == other_file_hash['hash'] and file_hash['path'] != other_file_hash['path']:
                    file.write('+ Checking: ' + file_hash['path'] + '\n')
                    file.write('- Duplicate Found!: ' + other_file_hash['path'] + '\n\n')
                    # duplicate file is added to a list to avoid checking file again (eliminates some redundancy)
                    duplicates_list.append(other_file_hash['path'])
        file.write('- CHECK DONE -\n')

def main():
    
    # 'C:\Users\username\Pictures'
    target_directory = r'C:\Users\fufufanatic\Pictures'
        
    powershell_hash_to_file(target_directory)
    file_hash_list = file_hash_to_list()
    duplicates_to_file(file_hash_list)
    
if __name__ == '__main__':
    main()