from core.fileformat import read_json
from core.jobs import example
from jobs.nltk_helper import segment_text_job
from jobs.maligna_helper import maligna_seg_job,maligna_align_job
from jobs.maligna_helper import maligna_pre,maligna_exe,maligna_exe2
from jobs.nltk_helper import nltk_pre,nltk_exe

def get_jobs_configuration():
    global my_jobs
    return my_jobs

def load_jobs_definitions(filepath):
    global my_jobs
    print("load jobs definitions")
    conf = read_json(filepath)
    if conf is None:
        print("configuration wrong or it doesn't exists")
        return
    my_jobs = conf['jobs']
    

from importlib import import_module

def start_job(app,jsonObject,operation,filepath,which):
    
    global g_job,my_jobs
        
    result = {}
    result['operation'] = operation
    result['name'] = my_jobs[operation]['name']
    if operation in my_jobs:
        mod = import_module('jobs.'+my_jobs[operation]['module'])
        pre = getattr(mod,my_jobs[operation]['pre'])
        execute = getattr(mod,my_jobs[operation]['execute'])
        opResult,resVal = pre(jsonObject,operation,filepath,which)
        if opResult:
            g_job = execute(app,jsonObject,operation,filepath,which,resVal)
            job_id = g_job.get_id()
        else:
            result['error'] = resVal
            job_id = -1
    else:
        result['error'] = 'operation {} not found'.format(operation)

    result['j_id'] = job_id
    return result

def get_job_status():
    global g_job 
    result = {}
    if 'g_job' in globals():
        g_job.refresh()
        result['is_finished'] = g_job.is_finished
        result['is_failed'] = g_job.is_failed
        result['j_id']= g_job.get_id()
        result.update(g_job.meta)
    else:
        result['is_failed'] = True
        result['is_finished'] = False
        result['j_id']= -1
    
    return result

def get_result():
    return g_job.result