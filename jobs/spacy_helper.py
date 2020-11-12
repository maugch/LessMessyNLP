from spacy.lang.en import English

from core.jobs import init_job
from core.fileformat import create_segments

def pre(jsonObject,operation,filepath,which):
    return True,''

def exe(app,jsonObject,operation,filepath,which,retVal):
    g_job = app.task_queue.enqueue(split_in_sentences,jsonObject,which)      
    return g_job

def split_in_sentences(json_dic,which):
    print('Starting')
    job = init_job('spacy-seg')

    raw_text = json_dic[which]['source']
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    doc = nlp(raw_text)
    sentences = [sent.string.strip() for sent in doc.sents]    
    
    json_dic[which]['segments'] = create_segments(sentences)
    
    job.meta['output'] = json_dic[which]['segments']
    job.meta['type'] = 'onesegment'
    job.meta['which'] = which
    job.meta['progress'] = 100
    job.save_meta()
    return sentences # why?


import spacy
def exe_mod(app,jsonObject,operation,filepath,which,retVal):
    g_job = app.task_queue.enqueue(split_in_sentences_with_model,jsonObject,which,'en')      
    return g_job

def split_in_sentences_with_model(json_dic,which,language):
    print('Starting')
    job = init_job('spacy-seg')

    raw_text = json_dic[which]['source']
    nlp = __load_spacy(language)
    doc = nlp(raw_text)
    sentences = [sent.string.strip() for sent in doc.sents]

    json_dic[which]['segments'] = create_segments(sentences)
    
    job.meta['output'] = json_dic[which]['segments']
    job.meta['type'] = 'onesegment'
    job.meta['which'] = which
    job.meta['progress'] = 100
    job.save_meta()
    return sentences # why?

def __load_spacy(language):
    return spacy.load('en_core_web_sm') 