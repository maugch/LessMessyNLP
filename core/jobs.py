from rq import get_current_job

#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs

def init_job(name):
    print('Starting task',name)
    job = get_current_job()
    # TODO: remove name=name confusion
    job.meta['name'] = name
    job.meta['progress'] = 0
    job.meta['output'] = []
    job.save_meta()
    return job


from subprocess import Popen,PIPE,CalledProcessError
from subprocess import check_output,run


def execute_short_single(cmd,input_str):
    #todo: add try/catch
    print('execute short single')
    #print(input_str)
    #print(cmd)
    p = run(cmd, stdout=PIPE,input=input_str, encoding='utf-8',timeout=5)
    print('returncode',p.returncode)
    #print(p.stdout)
    print('stderr',p.stderr)
    return p.stdout

def execute_short_double(cmd1,cmd2,input_str):
    '''
    execute two short commands, the first with an input string.
    '''
    #todo: add try/catch
    p = run(cmd1, stdout=PIPE,input=input_str, encoding='utf-8')
    p2 = run(cmd2, stdout=PIPE,input=p.stdout, encoding='utf-8')
    print(p2.returncode)
    #print(p.stdout)
    return p2.stdout

##################################################
##################################################
##################################################
from time import sleep
def example(seconds):
    
    job = init_job('example')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.meta['name'] = 'example'
        job.save_meta()
        print(i)
        sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')
    return 'example ret'
##################################################



#################################################
#################################################
#################################################
def xxxexecute_short(cmd1, cmd2) :
    ps = Popen(cmd1, stdout=PIPE)
    try:
        output = check_output(cmd2, stdin=ps.stdout)
        ps.wait()
        return output
    except CalledProcessError as e:
        print('CalledProcessError')
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))    

def XXXexample2(text):
    lines = []
    job = get_current_job()
    print('Starting task example2')
    job.meta['progress'] = 100
    job.meta['name'] = 'maligna-seg'
    job.meta['output'] = []
    job.save_meta()
    cmdlist = ["ls", "-ltr"]
    cmdlist = cmd_split_sentence()
    execute_test()
    return '1'
    for path in xxexecute(cmdlist):
        job.save_meta()
        job.meta['output'].append(path)
        lines.append(path)
        print(path, end="")
    print('Task completed')
    return lines 

def xxexecute(cmd):
    popen = Popen(cmd, stdout=PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise CalledProcessError(return_code, cmd)

