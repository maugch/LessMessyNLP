from os import path
from json import load,dump

def create_json_from_files(root_folder,workspace,file1,file2):
    dirpath = path.join(root_folder,workspace)
    file_part, _ = path.splitext(file1) #I use the first file as starting point.
    dest_filename = file_part+'.json'
    __move_existing_file_for_backup(dirpath,dest_filename)
    create_json(dirpath,file1,file2,dest_filename)    
    return dest_filename

def read_json(filepath):
    if not path.isfile(filepath):
        print('file not found {}'.format(filepath))
        return None
    with open(filepath,'r',encoding='utf8') as f:
        result = load(f)
        return result

def save_json(json,filepath):
    __move_existing_file_for_backup(filepath)
    with open(filepath, 'w',encoding="utf-8") as fp:
        dump(json,fp,indent=2)

def create_json(dirpath,file1,file2,destination_file):
    language1 = 'unk.'
    language2 = 'unk.'
    with open(path.join(dirpath,file1),'r',encoding='utf8') as f:
        content1 = f.read()
    with open(path.join(dirpath,file2),'r',encoding='utf8') as f:
        content2 = f.read()

    destination_file = path.join(dirpath,destination_file)
    
    result = {}
    result['format'] = 'nlpw1'
    result['first'] = {}
    result['second'] = {}
    result['first']['language'] = language1
    result['first']['source'] = content1
    result['second']['language'] = language2
    result['second']['source'] = content2
    with open(destination_file, 'w',encoding="utf-8") as fp:
        dump(result,fp,indent=2)
    
def create_segments(result) :
    '''
    create segments for the segments list.
    '''
    segments = []
    for i in range(0,len(result)):
        segments.append( { 'idx': i , 'text' : result[i] })
    return segments