from os import path,walk,listdir,rename
from core.fileformat import create_json
import glob

def get_pickle_path(workspace_folder):
    ''' return pickle file, None if 0 or more than 1 exists  '''
    mypath = path.join(workspace_folder,"*.pickle")
    files = glob.glob(mypath)
    if len(files) != 1:
        return None
    else:
        return files[0]

def get_txtfiles_in_workspace(root_folder,workspace,types=''):
    if types == '':
        types = ('*.txt', '*.xml','*.json')
    else:
        types = types.split(',')
    
    files_grabbed = []
    for ft in types:
        mypath = path.join(root_folder,workspace,ft)
        files_grabbed.extend(glob.glob(mypath))
    
    result = []
    for x in files_grabbed:
        filename = path.basename(x)
        _,ext = path.splitext(filename)
        r = {}
        r['name'] = filename
        r['ext'] = ext
        result.append(r)
    return result

def get_workspace_content(root_folder,workspace):
    files = []
    dirs = []
    dirpath = path.join(root_folder,workspace)
    for x in listdir(dirpath):
        if path.isfile(path.join(dirpath,x)):
            files.append(x)
        else:
            dirs.append(x)
    dirs = sorted(dirs)
    files = sorted(files)
    return dirs,files

def __move_existing_file_for_backup(dirpath,filename=None):
    ''' return the filename used for the backup '''
    if filename is None:
        #dirpath is the full path
        filename = path.basename(dirpath)
        dirpath = path.dirname(dirpath)
    
    filename_final = filename
    i = 1
    while(path.isfile(path.join(dirpath,filename_final))):
        file_part, ext_part = path.splitext(filename_final)
        file_part, _ = path.splitext(file_part)
        filename_final = file_part + '.' + str(i) + ext_part
        i+=1
        
    if filename_final == filename:
        return filename

    orig = path.join(dirpath,filename)
    dest = path.join(dirpath,filename_final)
    #move old file on new name
    if path.isfile(orig):
        print('file moved {} {}'.format(orig,dest))
        rename(orig,dest)
    
    return filename_final

def get_workspaces(root_folder):
    '''
    get a list of directories
    '''
    print('get workspaces')
    if not path.exists(root_folder):
        print("root path doesn't exist.")
        return []
    res = next(walk(root_folder))
    names = [path.basename(x) for x in res[1] ]
    return names

