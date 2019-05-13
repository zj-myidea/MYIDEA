import json
import sys
from pipeline.service import db, Graph, Vertex, Edge
from pipeline.service import create_graph,add_edge, add_vertex,check_graph
from pipeline.executor import start,show_pipeline, finish_params,finish_script,EXECUTOR

def test_create_dag():
    try:
        # 创建DAG
        g = create_graph('test1') # 成功则返回一个Graph对象
        # 增加顶点
        input = {
            "ip":{
                "type":"str",
                "required":True,
                "default":'127.0.0.1'
            }
        }
        if sys.platform in ['dos', 'win32', 'win16']:
            script = {
                'script':'echo "test1.A"\nping {ip}',
                'next':'B'
            }
        else:
            script = {
                'script':'echo "test1.A"\nping {ip} -w 4',
                'next':'B'
            }

        # 这里为了让用户方便，next可以接收2种类型，数字表示顶点的id，字符串表示同一个DAG中该名称的节点，不能重复
        a = add_vertex(g, 'A', json.dumps(input), json.dumps(script)) # next顶点验证可以在定义时，也可以在使用时
        b = add_vertex(g, 'B', None, '{"script":"echo B"}')
        c = add_vertex(g, 'C', None, '{"script":"echo C"}')
        d = add_vertex(g, 'D', None, '{"script":"echo D"}')
        # 增加边
        ab = add_edge(g, a, b)
        ac = add_edge(g, a, c)
        cb = add_edge(g, c, b)
        bd = add_edge(g, b, d)

        # 创建环路
        g = create_graph('test2') # 环路
        # 增加顶点
        a = add_vertex(g, 'A', None, '{"script":"echo A"}')
        b = add_vertex(g, 'B', None, '{"script":"echo B"}')
        c = add_vertex(g, 'C', None, '{"script":"echo C"}')
        d = add_vertex(g, 'D', None, '{"script":"echo D"}')
        # 增加边, abc之间的环
        ba = add_edge(g, b, a)
        ac = add_edge(g, a, c)
        cb = add_edge(g, c, b)
        bd = add_edge(g, b, d)

        # 创建DAG
        g = create_graph('test3') # 多个终点
        # 增加顶点
        a = add_vertex(g, 'A', None, '{"script":"echo A"}')
        b = add_vertex(g, 'B', None, '{"script":"echo B"}')
        c = add_vertex(g, 'C', None, '{"script":"echo C"}')
        d = add_vertex(g, 'D', None, '{"script":"echo D"}')
        # 增加边
        ba = add_edge(g, b, a)
        ac = add_edge(g, a, c)
        bc = add_edge(g, b, c)
        bd = add_edge(g, b, d)

        # 创建DAG
        g = create_graph('test4') # 多入口
        # 增加顶点
        a = add_vertex(g, 'A', None, '{"script":"echo A"}')
        b = add_vertex(g, 'B', None, '{"script":"echo B"}')
        c = add_vertex(g, 'C', None, '{"script":"echo C"}')
        d = add_vertex(g, 'D', None, '{"script":"echo D"}')
        # 增加边
        ab = add_edge(g, a, b)
        ac = add_edge(g, a, c)
        cb = add_edge(g, c, b)
        db = add_edge(g, d, b)
    except Exception as e:
        print(e)
# test_create_dag()
# vertexs = db.session.query(Vertex.id).filter(Vertex.g_id == 1)
#
# g = db.session.query(Graph).filter((Graph.id == 1) & (Graph.checked==0)).first()
# print(g)
#
# g = db.session.query(Graph).filter(Graph.id==1).first()
#
# check_graph(g)
#
# start(1,'haha')
#
# print(show_pipeline(2))
ps = show_pipeline(1) # p_id = 1 tracks
print(ps)
pipeline = ps[0]
p_id, p_name, p_state, t_id, v_id, t_state, inp, script = ps[0]
print(p_id, p_name, p_state, t_id, v_id, t_state, inp, script)
d = {
            # "ip": {
            #     "type": "str",
            #     "required": True,
            #     "default": '192.168.0.100'
            # }
        }
params = finish_params(v_id,d)
script = finish_script(t_id,*params)
# print('---------------------')
# from subprocess import Popen, PIPE
# from tempfile import TemporaryFile
# tf = TemporaryFile('w+')
# p = Popen('ping www.baidu.com', shell=True, stdout=tf,encoding='utf-8')
# code = p.wait()
# print(code)
# tf.seek(0)
# text = tf.read()
# print(text)
EXECUTOR.executor(t_id,script)
