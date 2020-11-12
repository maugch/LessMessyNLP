#from blingfire import *

#TODO: understand how blingfire can be used
# 1. doesn't work in cygwin
# 2. doesn't work in virtualenv windows x64
# 3. ...

'''

def pre(jsonObject,operation,filepath,which):
    return True,''

def exe(app,jsonObject,operation,filepath,which):
    job = app.task_queue.enqueue(split_job,jsonObject)
    return job

def split_job(jsonObject,which):
    job = init_job('blingfire')
    txt = jsonObject[which]['source']
    result = text_to_sentences(txt).split('\n')
    segments = create_segments(result)
    job.meta['output'] = segments
    job.meta['type'] = 'onesegment'
    job.meta['which'] = which

    '''