import nltk.data
import nltk.tokenize.punkt
import pickle
import codecs
from os import path

from core.fileformat import save_json,create_segments
from core.utils import get_pickle_path
from core.jobs import init_job


def nltk_pre(jsonObject,operation,filepath,which):
    pickle_path = get_pickle_path(path.dirname(filepath))
    print('pickle_path: {}'.format(pickle_path))
    if pickle_path is not None and path.isfile(filepath):
        return True,pickle_path
    else:
        return False,'pickle file not found'

def nltk_exe(app,jsonObject,operation,filepath,which,retVal):
    pickle_path = retVal
    if operation == 'nltk-seg-save':
        g_job = app.task_queue.enqueue(segment_text_job,jsonObject,pickle_path,filepath,which)  
    else:
        g_job = app.task_queue.enqueue(segment_text_job,jsonObject,pickle_path,'',which)      
    return g_job

def segment_text_job(json_dic,pickle_path,filepath,which):
    '''
    split a text in sentences. 
    json_dic: json object
    which: which part of json the text come from.
    '''
    print('Starting task segment')
    job = init_job('nltk-seg')

    result = __segment_text(json_dic[which]['source'],pickle_path)    
    
    # TODO change ! remove save as well?
    json_dic[which]['segments'] = create_segments(result)
    
    if filepath != '':
        save_json(json_dic,filepath)
        job.meta['doSave'] = '1' 
    else:
        job.meta['output'] = json_dic[which]['segments']
        job.meta['type'] = 'onesegment'
        job.meta['which'] = which
    
    job.meta['progress'] = 100
    job.save_meta()
    return result

def __segment_text(text,pickle_path):
    '''
    return a list of sentences
    '''
    #1
    sent_detector = nltk.data.load(pickle_path,'pickle')
    result = sent_detector.tokenize(text.strip())

    #2
    #tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    #result = tokenizer.tokenize(text.strip())
    
    return result


    