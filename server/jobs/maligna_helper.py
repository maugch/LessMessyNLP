from os import path
from lxml import etree

from core.jobs import init_job,execute_short_double,execute_short_single

MALIGNA_BAT_PATH = path.join('../','redis','maligna-3.0.0','bin','maligna.bat')    

def maligna_pre(jsonObject,operation,filepath,which):
    if 'first' in jsonObject and 'second' in jsonObject and 'source' in jsonObject['first'] and 'source' in jsonObject['second']:
        return True,''
    else:
        return False,'Text not present'
    
def maligna_exe(app,jsonObject,operation,filepath,which,retVal):
    text1 = jsonObject['first']['source']
    text2 = jsonObject['second']['source']
    job = app.task_queue.enqueue(maligna_seg_job,text1,text2)
    return job

def maligna_exe2(app,jsonObject,operation,filepath,which,retVal):
    job = app.task_queue.enqueue(maligna_align_job,jsonObject)
    return job


def maligna_seg_job(text1,text2):
    job = init_job('maligna-seg')
    
    cmd,cmd2 = cmd_2_split_in_sentences()
    result = execute_short_double(cmd,cmd2,text2xmlstring(text1,text2))
    job.meta['output'] = results2segment_lists(result)
    job.meta['type'] = 'twosegments'
    job.save_meta()
    print('Task completed')

def maligna_align_job(jsonData):
    job = init_job('maligna-align')
    
    cmd = cmd_2_align_sentences()
    result = execute_short_single(cmd,json2xmlstring(jsonData))
    #job.meta['output'] = results2segment_lists(result)
    res = compare_results(jsonData,result)
    job.meta['output'] = res
    job.meta['type'] = 'align'
    job.save_meta()
    print('Task completed')

def compare_results(json,xmldata):
    root = etree.fromstring(xmldata.encode('utf8'))
    #<?xml <alignmentlist <alignment <sourcelist <segment
    alignments = root.xpath('//alignment')
    result = []
    for alignment in alignments:
        source_segments = alignment.xpath('sourcelist/segment/text()')
        target_segments = alignment.xpath('targetlist/segment/text()')
        source_idx = []
        target_idx = []
        for seg in source_segments:
            for jseg in json['first']['segments']:
                if seg == jseg['text']:
                    source_idx.append(jseg['idx'])
        for seg in target_segments:
            for jseg in json['second']['segments']:
                if seg == jseg['text']:
                    target_idx.append(jseg['idx'])
    
        result.append((tuple(source_idx),tuple(target_idx)))
    return result

def cmd_2_split_in_sentences():
    # commands to split a text in sentences
    cmd1= (MALIGNA_BAT_PATH,'modify','-c','split-sentence')
    cmd2 = (MALIGNA_BAT_PATH,'modify','-c','trim')
    return cmd1,cmd2

def cmd_2_align_sentences():
    #command to align sentences    
    cmd1= (MALIGNA_BAT_PATH,'align','-c','viterbi','-a','poisson','-n','word','-s','iterative-band')
    return cmd1


def results2segment_lists(xmldata):
    '''
    return two lists of segments.
    '''
    root = etree.fromstring(xmldata.encode('utf8'))
    #<?xml <alignmentlist <alignment <sourcelist <segment
    result1 = root.xpath('//sourcelist/segment/text()')
    result2 = root.xpath('//targetlist/segment/text()')
    r1 = []
    r2 = []
    for i in range(0,len(result1)):
        r1.append( { 'idx': i , 'text' : result1[i] })
    for i in range(0,len(result2)):
        r2.append( { 'idx': i , 'text' : result2[i] })
    return r1,r2


def json2xmlstring(json):
    ''' transform my json to xml for maligna '''
    #jsonData.first/second.segments
    if 'first' in json and 'second' in json:
        root = etree.Element('alignmentlist')
        #<?xml <alignmentlist <alignment <sourcelist <segment
        lev1 = etree.Element('alignment',score='0.0')
        sl = etree.Element('sourcelist')
        sl2 = etree.Element('targetlist')
        root.append(lev1)
        lev1.append(sl)
        lev1.append(sl2)
        for txt in json['first']['segments']:
            se = etree.Element('segment')
            se.text = txt['text']
            sl.append(se)
        for txt in json['second']['segments']:
            se = etree.Element('segment')
            se.text = txt['text']
            sl2.append(se)

        result = etree.tostring(root, pretty_print=True).decode('utf-8')
        #print(result)
        return result
    else:
        return ''

def text2xmlstring(text1,text2):
    ''' Transform two text in an xml compliant with maligna format.    '''
    root = etree.Element('alignmentlist')
    #<?xml <alignmentlist <alignment <sourcelist <segment
    lev1 = etree.Element('alignment',score='0.0')
    sl = etree.Element('sourcelist')
    sl2 = etree.Element('targetlist')
    root.append(lev1)
    lev1.append(sl)
    lev1.append(sl2)
    se = etree.Element('segment')
    se.text = text1
    se2 = etree.Element('segment')
    se2.text = text2
    sl.append(se)
    sl2.append(se2)

    result = etree.tostring(root, pretty_print=True).decode('utf-8')
    #print(result)
    return result
    

