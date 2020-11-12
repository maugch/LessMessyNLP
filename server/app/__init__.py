import itertools
import time
from os import path,walk
import re

from flask import Flask, g, Blueprint
from flask import render_template
from flask import jsonify
from flask import send_from_directory, send_file
from flask import request,Response, redirect, url_for

from flask_cors import CORS

from rq import get_current_job, Queue
from redis import Redis

from core.utils import get_txtfiles_in_workspace,get_workspaces
from core.fileformat import read_json,create_json_from_files,save_json
from core.jobs_utils import start_job,get_job_status,get_result,load_jobs_definitions,get_jobs_configuration
from json import dumps as json_dumps

import logging
import logging.config

logger = logging.getLogger(__name__)
logdir = '.'
logfile = 'log.log'

logging.config.dictConfig( {
    'version': 1,              
    'disable_existing_loggers': False,  # this fixes the problem

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
		'stdout': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',    
            'class':'logging.handlers.RotatingFileHandler',
            "formatter": "standard",
            "filename": path.join(logdir,logfile),
            "maxBytes": 2000000,
            "backupCount": 50,
            "encoding": "utf8"
        }, 
		'stdout': {
            'level':'INFO',    
            'class':'logging.StreamHandler',
            "formatter": "stdout",
			"stream"  : "ext://sys.stdout"
        },  		
    },
    'loggers': {
        '': {                  
            'handlers': ['default','stdout'],        
            'level': 'INFO',  
            'propagate': True  
        }
    }
})
STATIC_FOLDER = '../../client/dist/'
TEMPLATE_FOLDER = '../../client/dist/'

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
CORS(app)

from pathlib import Path
#UPLOAD_FOLDER = '../../../mydata'
tpath= Path(app.root_path).parent.parent.parent
UPLOAD_FOLDER = path.join(tpath,'mydata')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from worker import conn,queue_name,redis_available
app.task_queue = Queue(queue_name,connection=conn)
redis_a = redis_available

jpath = Path(app.root_path).parent
load_jobs_definitions(path.join(jpath,'jobs','jobs.json'))

from flask import current_app
@app.route('/')
def basepage():
    return current_app.send_static_file('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(STATIC_FOLDER + 'js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(STATIC_FOLDER + 'css', path)

## streams #############################
import subprocess

@app.route('/stream')
def straa():
     return render_template('stream.html')

@app.route('/streamf')
def ccc():
    def inner():
        proc = subprocess.Popen(
            ['cat','p1.txt'],             #call something with a lot of output so we can see it
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        for line in proc.stdout:
            #time.sleep(1)                           # Don't need this just shows the text streaming
            yield line.rstrip().decode("utf-8")  + "<br/>\n"

        proc.stdout.close()
        
    return Response(inner(), mimetype='text/html')  # text/html is required for most browsers to show th$

################################################
################################################
################## API #########################
################################################
@app.route('/configuration')
def get_server_configuration():
    my_jobs = get_jobs_configuration()
    return jsonify(my_jobs)

@app.route('/files/<workspace>')
def get_workspace_textfiles(workspace):
    if 'type' in request.args:
        files_in_workspace = get_txtfiles_in_workspace(UPLOAD_FOLDER, workspace, request.args['type'])
    else:
        files_in_workspace = get_txtfiles_in_workspace(UPLOAD_FOLDER, workspace)
    print(files_in_workspace)
    return jsonify(files_in_workspace)

@app.route('/workspaces')
def get_workspaces_list():
    res = get_workspaces(UPLOAD_FOLDER)
    return jsonify(res)

from datetime import datetime

@app.route('/json')
def get_json():
    result = {}
    workspace = request.args.get('workspace')
    filename = request.args.get('filename')
    print('get json:',workspace,filename)
    if workspace and filename:
        if filename.endswith('.json'):
            filepath = path.join(UPLOAD_FOLDER,workspace,filename)
            js = read_json(filepath)
            if js:
                result = {}
                result['json'] = js
                info = path.getmtime(filepath);
                f = datetime.fromtimestamp(info).strftime('%Y-%m-%d %H:%M:%S')
                result['create_dt'] = f
                return jsonify(result)
    else:
        print('no workspace or filename')
    result['error'] ='something went wrong: {} {}'.format(workspace, filename)
    return jsonify(result)

@app.route('/savejson', methods=['GET', 'POST'])
def save_json_route():
    data = request.get_json(silent=True)
    content = data.get('content')
    filename = data.get('filename')
    workspace = data.get('workspace')
    filepath = path.join(UPLOAD_FOLDER,workspace,filename)
    save_json(filepath,content)
    return 'ok'

@app.route('/merge', methods=['GET', 'POST'])
def merge_files_route():
    data = request.get_json(silent=True)
    file1 = data.get('file1')
    file2 = data.get('file2')
    workspace = data.get('workspace')
    
    saved_name = create_json_from_files(UPLOAD_FOLDER,workspace,file1,file2)
    return saved_name

@app.route('/longop', methods=['GET', 'POST'])
def do_long_operation():
    data = request.get_json(silent=True)
    operation = data.get('operation')
    jsonObject = data.get('jsonObject')
    workspace = data.get('workspace')
    filename = data.get('filename')
    which = data.get('which')
    print('dolong',operation,workspace,filename,which,len(jsonObject))

    filepath = path.join(UPLOAD_FOLDER,workspace,filename)
    job_info = start_job(app,jsonObject,operation,filepath,which)
    print('job_info {}'.format(job_info))
    return jsonify(job_info)

#@app.route('/status/<id>')
#def do_long_status(id):
@app.route('/status')
def do_long_status():
    result = get_job_status()
    return jsonify(result)


import re

@app.route('/getLog')
def getLog() :
    result = ''
    #example
    my_r = r'^(\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2}\,\d{3}) ([^\s]+) (\[.+\]) ([^\s]+) ([^\s]+|) ([^\s]+) ([^\s]+) \- ([\s\S]*?)\n*(?=(\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2}\,\d{3})|\Z)'
    
    workspace = request.args.get('workspace')
    filename = request.args.get('filename')
    if workspace and filename:
        filepath = path.join(UPLOAD_FOLDER,workspace,filename)
        print('filepath {}'.format(filepath))
        with open(filepath,'r',encoding='utf-8') as f:
            result = f.read()

    r = re.compile(my_r,re.MULTILINE)
    mylist = r.findall(result)

    result = []
    threads = set()
    hosts = set()
    for log in mylist:
        r = {}
        r['date'] = log[0]
        r['host'] = log[1]
        hosts = set()
        r['thread'] = log[2][1:-1]
        threads.add(log[2][1:-1])
        r['method'] = log[3]
        r['user'] = log[4]

        r['loglevel'] = log[5]
        r['isWarning'] = False
        r['isError'] = False
        if log[5] == 'ERROR':
            r['isError'] = True
        elif log[5] == 'DEBUG':
            r['isWarning'] = True
        
        r['who'] = log[6]
        r['message'] = log[7]
        r['tohide'] = False
        result.append(r)
    rresult = {}
    rresult['lines'] = result
    lst = list(threads)
    lst.sort()
    rresult['threads'] = lst
    rresult['hosts'] = list(hosts)
    return jsonify(rresult)


if __name__ == '__main__':
    app.run(debug=True)