from .model import Vertex, Graph, Edge,db, Pipeline, Track
from .config import getlogger
from functools import wraps
from collections import defaultdict



logger = getlogger(__name__,'./recode.log')

def transactional(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        ret = fn(*args, **kwargs)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(e)
        return ret
    return wrapper



@transactional
def create_graph(name,desc=None):
    graph = Graph()
    graph.name = name
    graph.desc = desc
    db.session.add(graph)
    return graph

@transactional
def add_vertex(graph:Graph, name:str, input=None, script=None,):
    vertex = Vertex()
    vertex.g_id = graph.id
    vertex.name = name
    vertex.input = input
    vertex.script = script
    db.session.add(vertex)

    return vertex

@transactional
def add_edge(graph:Graph, tail:Vertex, head:Vertex):
    edge = Edge()
    edge.g_id = graph.id
    edge.head = head.id
    edge.tail = tail.id
    db.session.add(edge)

    return  edge

def delete_vertex(id):
    query = db.session.query(Vertex).filter(Vertex.id==id)
    v = query.first()
    if v:
        db.session.query(Edge).filter(Edge.tail == v.id | Edge.head == v.id).delete()
        query.delete()
    return v

def check_graph(graph:Graph):
    query = db.session.query(Vertex).filter(Vertex.g_id==graph.id)
    vertexs = {vertex.id for vertex in query}
    query = db.session.query(Edge).filter(Edge.g_id==graph.id)

    edges = defaultdict(list)
    ids = set()
    for edge in query:
        edges[edge.tail].append((edge.tail, edge.head))
        ids.add(edge.head)

    if len(edges) == 0:
        print('edge')
        return False

    zds = vertexs - ids

    if len(zds):                          # {a:[(a,b),(a,c)],b:[(b,d)]}
        for zd in zds:
            if zd in edges:
                edges.pop(zd)

        while edges:
            print(edges)
            vertexs = ids
            ids = set()
            for lis in edges.values():
                for edge in lis:
                    ids.add(edge[1])
            zds = vertexs - ids
            if not len(zds):
                print('zds')
                break
            else:
                for zd in zds:
                    edges.pop(zd)


        if len(edges) == 0:
            try:
                graph = db.session.query(Graph).filter(Graph.id ==graph.id).first()
                if graph:
                    graph.checked = 1
                    db.session.add(graph)
                    db.session.commit()
                    print('++++++++++++++++++++')
                    return True
            except Exception as e:
                db.session.rollback()
                raise e
        print('~~~~~~~~~~~~')
        return False


















