from .service import db, Graph, Vertex, Edge, Pipeline, Track, transactional,getlogger
from .model import STATE_WATTING, STATE_FAILED, STATE_SUCCEED, STATE_PENDING, STATE_RUNNING, STATE_FINISH
import logging
import simplejson
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = getlogger(__name__,'./executor.log')


def start(g_id, name:str, desc=None):
    g:Graph = db.session.query(Graph).filter((Graph.id == g_id) & (Graph.checked==1)).first()
    if not g:
        return
    query = db.session.query(Vertex).filter(Vertex.g_id == g.id)
    vertexs = query.all()
    if not vertexs:
        return
    query = query.filter(Vertex.id.notin_(db.session.query(Edge.head).filter(Edge.g_id == g_id)))

    zds = {zd.id for zd in query}

    p = Pipeline()
    p.g_id = g_id
    p.name = name
    p.state = STATE_RUNNING
    p.desc = desc
    db.session.add(p)

    for v in vertexs:
        t = Track()
        t.pipeline = p
        t.v_id = v.id
        t.state = STATE_WATTING if v.id not in zds else STATE_PENDING
        db.session.add(t)

    if g.sealed == 0:
        g.sealed = 1
        db.session.add(g)

    try:
        db.session.commit()
        print('status OK')
        pass
    except Exception as e:
        db.session.rollback()
        logger.error(e)



def show_pipeline(id, state=[STATE_PENDING], exclude=[STATE_FAILED]):
    p = db.session.query(Pipeline.id, Pipeline.name, Pipeline.state ,Track.id,
        Track.v_id, Track.state, Vertex.input, Vertex.script)\
        .join(Track, Pipeline.id == Track.p_id)\
        .join(Vertex, Vertex.id == Track.v_id)\
        .filter((Pipeline.state.notin_(exclude)) & (Pipeline.id == id))\
        .filter(Track.state.in_(state))\
        # .filter(Track.p_id == id, )
    return p.all()

TYPES={'str':str, 'int':int}
def finish_params(v_id, dic:dict):
    inp = db.session.query(Vertex.input,Vertex.script).filter(Vertex.id == v_id).first()
    script = ''
    if inp:
        try:
            script = simplejson.loads(inp[1])
            inp = simplejson.loads(inp[0])

            if not isinstance(inp, dict):
                inp = {}
        except:
            inp = {}

        d = {}
        for k, v in inp.items():
            if v.get('required',False):
                i = input('{} = '.format(k))
                d[k] = i
            else:
                try:
                    d[k] = v['default']
                except:
                    raise TypeError('参数错误')
        return  d,script
@transactional
def finish_script(t_id, params:dict, script):
    newline = ''
    if script:
        line = script.get('script','')
        # newline = line.format(**params)
        start = 0
        regex = re.compile(r'{([^{}]+)}')
        for match in regex.finditer(line):
            newline += line[start:start+match.start()]
            key = match.group(1)
            tmp = params.get(key,'')
            newline += str(tmp)
            start = match.end()
        else:
            newline += line[start:]
        t:Track = db.session.query(Track).filter(Track.id == t_id).first()
        if t:
            t.input = simplejson.dumps(params)
            t.script = newline
            db.session.add(t)
        return newline

from subprocess import Popen
from tempfile import  TemporaryFile
import uuid
import threading
import queue
from collections import  defaultdict

class Executor():
    def __init__(self,worker=5):
        self._executor = ThreadPoolExecutor(max_workers=worker)
        self._tasks = {}
        self.event = threading.Event()
        self._queue = queue.Queue()
        threading.Thread(target=self._run,daemon=True).start()
        threading.Thread(target=self._save_track).start()

    def _execute(self,script):
        codes = 0
        with TemporaryFile('a+') as tf:
            for line in script.splitlines():
                p = Popen(line, shell=True, stdout=tf)
                code = p.wait()
                codes += code
            tf.flush()
            tf.seek(0)
            text = tf.read()
            return  codes, text

    def executor(self,t_id,script):
        try:
            t = db.session.query(Track).filter(Track.id == t_id).one()
            key = uuid.uuid4().hex
            self._tasks[self._executor.submit(self._execute,script)] = key, t_id
            t.state = STATE_RUNNING
            db.session.add(t)
            db.session.commit()
        except Exception as e:
            db.rollback()
            logging.error(e)

    def _run(self):
        while not self.event.is_set():
            self.event.wait(5)
            for future in as_completed(self._tasks):
                key, t_id = self._tasks[future]
                try:
                    code, text = future.result()
                    self._queue.put((t_id, code, text))
                except Exception as e:
                    print(e)
                    print(key, 'failed')
                finally:
                    del self._tasks[future]

    def _save_track(self):
        while True:
            t_id, code, text = self._queue.get()
            print(text,'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            t = db.session.query(Track).filter(Track.id == t_id).first()
            t. state = STATE_SUCCEED if code == 0 else STATE_FAILED
            t.output = text
            if code != 0:
                t.pipeline.state = STATE_FAILED
            else:
                tracks = db.session.query(Track).filter((Track.p_id == t.p_id) & (Track.id != t_id)).all()
                states = {STATE_WATTING:0,STATE_PENDING:0,STATE_RUNNING:0, STATE_FAILED:0, STATE_SUCCEED:0}
                ts = {}
                for track in tracks:
                    states[track.state] += 1
                if states[STATE_FAILED] > 0:
                    t.pipeline.state = STATE_FAILED
                elif len(tracks) == states[STATE_SUCCEED]:
                    t.pipeline.state = STATE_FINISH
                else:
                    query = db.session.query(Edge).filter(Edge.g_id==t.pipeline.g_id).all()
                    t2h = defaultdict(list)
                    h2t = defaultdict(list)
                    for edge in query:
                        h2t[edge.head].append(edge.tail)
                        t2h[edge.tail].append(edge.head)
                    if t.v_id in t2h.keys():
                        nexts = t2h[t.v_id]
                        for nex in nexts:
                            tails = h2t[nex]
                            s_count = db.session.query(Track).filter((Track.p_id == t.p_id)
                                                                     &(Track.v_id.in_(tails))
                                                                     & (Track.state==STATE_SUCCEED)).count()


                            if s_count == len(tails):
                                print('enter')
                                head = db.session.query(Track).filter(Track.v_id == nex).one()
                                head.state = STATE_PENDING
                                db.session.add(head)

            db.session.add(t)
            try:
                db.session.commit()
                # TODO
            except Exception as e :
                db.session.rollback()
                logger.error(e)

EXECUTOR = Executor()





