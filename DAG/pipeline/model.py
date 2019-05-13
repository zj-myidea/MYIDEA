from sqlalchemy import Column,Integer,TEXT, String, Text,ForeignKey, create_engine, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import URL, DATABASE_DEBUG
import functools

STATE_WATTING = 0
STATE_PENDING =1
STATE_RUNNING = 2
STATE_SUCCEED = 3
STATE_FAILED = 4
STATE_FINISH = 5


Base = declarative_base()

class Graph(Base):
    __tablename__ = 'graph'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False, unique=True)
    desc = Column(String(200), nullable=True)
    checked = Column(Boolean, nullable=False,default=0)
    sealed = Column(Boolean, nullable=False,default=0)

    # vertexes = relationship('Vertex')
    # edges = relationship('Edge')
    def __repr__(self):
        return f'<graph {self.id} {self.name}>'
    __str__ = __repr__

class Vertex(Base):
    __tablename__ = 'vertex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    script = Column(TEXT, nullable=True)
    input = Column(TEXT,nullable=True)

    g_id = Column(Integer, ForeignKey('graph.id'),nullable=False)

    graph = relationship('Graph')
    # tail = relationship('Edge', foreign_keys='[Edge.tail]')
    # head = relationship('Edge', foreign_keys='[Edge.head]')
    def __repr__(self):
        return f'<vertex {self.id} {self.name}>'
    __str__ = __repr__

class Edge(Base):
    __tablename__ = 'edge'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tail = Column(Integer,ForeignKey('vertex.id'), nullable=False)
    head = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)
    def __repr__(self):
        return f'<edge {self.id} {self.tail} -> {self.head}>'
    __str__ = __repr__

class Pipeline(Base):

    __tablename__ = 'pipeline'
    id = Column(Integer, primary_key=True, autoincrement=True)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)
    name = Column(String(48), nullable=True)
    state = Column(Integer, nullable=False, default=STATE_WATTING)
    desc = Column(String(200))

    # vertex = relationship('Vertex')
    graph = relationship('Graph')

    def __repr__(self):
        return f'<pipeline {self.id} {self.name}>'
    __str__ = __repr__

class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True, autoincrement=True)
    p_id = Column(Integer, ForeignKey('pipeline.id'), nullable=False)
    v_id = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    state = Column(Integer, nullable=False, default=STATE_WATTING,index=True)
    input = Column(TEXT, nullable=True)
    script= Column(TEXT, nullable=True)
    output = Column(TEXT, nullable=True)

    vertex = relationship('Vertex')
    pipeline = relationship('Pipeline')

    def __repr__(self):
        return f'<track {self.id} {self.state}>'
    __str__ = __repr__

def singleton(cls):
    instance = None
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal instance
        if not instance:
            instance = cls(*args,**kwargs)
        return instance
    return wrapper

@singleton
class Database:
    def __init__(self,url,**kwargs):
        self._engine = create_engine(url, **kwargs)
        self._session = sessionmaker(bind=self._engine)()

    @property
    def session(self):
        return self._session

    def create_all(self):
        Base.metadata.create_all(self._engine)

    def drop_all(self):
        Base.metadata.drop_all(self._engine)

db = Database(URL, echo=DATABASE_DEBUG)
# db.drop_all()
# db.create_all()






