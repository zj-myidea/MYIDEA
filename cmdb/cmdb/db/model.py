from sqlalchemy import Column, Integer, BigInteger, TEXT, String, SmallInteger,create_engine,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import simplejson
from cmdb.mytypes import get_instance

Base = declarative_base()
class Schema(Base):
    __tablename__ = 'schema'
    __table_args__ = (UniqueConstraint('name'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    desc = Column(String(200), nullable=True)
    deleted = Column(SmallInteger, nullable=False, server_default='0')

    Field = relationship('Field')

class Reference:

    def ___init(self,ref:dict):
        self.schema = ref['schema']
        self.field = ref['field']
        self.on_deleted = ref.get('on_deleted','disable')
        self.on_update = ref.get('on_update','disable')

class FieldMeta:

    def __init__(self,metastr):
        meta = simplejson.loads(metastr)
        if isinstance(meta['type'], str):
            self.instance = get_instance(meta['type'])
        else:
            option = meta['type'].get('option')
            if option:
                self.instance = get_instance(meta['type']['name'],**option)
            else:
                self.instance = get_instance(meta['type']['name'])
        self.nullable = meta.get('nullable',True)
        self.unique = meta.get('unique',False)
        self.default = meta.get('default')
        self.multi = meta.get('multi',False)
        ref = meta.get('reference')
        if ref:
            self.reference = Reference(ref)
        else:
            self.reference = None

class Field(Base):

    __tablename__ = 'field'
    __tale_args__ = (UniqueConstraint('schema_id','name'))

    id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String(48),nullable=False)
    schema_id = Column(Integer,ForeignKey('schema.id'),nullable=False)
    ref_id = Column(Integer, ForeignKey('field.id'), nullable=True)
    meta = Column(TEXT, nullable=False)
    deleted = Column(SmallInteger,nullable=False, server_default='0')

    ref = relationship('Field',uselist=False)
    schema = relationship('Schema')

    @property
    def meta_date(self):
        return FieldMeta(self.meta)

class Entity(Base):
    __tablename__ = 'entity'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String(64), nullable=False, unique=True)
    schema_id = Column(Integer, ForeignKey('schema.id'), nullable=False)
    deleted = Column(SmallInteger, nullable=False, server_default='0')

    schema = relationship('Schema')

class Value(Base):
    __tablename__ = 'value'
    __table_args__ = (UniqueConstraint('entity_id', 'field_id'),)

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    value = Column(TEXT, nullable=False)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    entity_id = Column(BigInteger, ForeignKey('entity.id'), nullable=False)
    deleted = Column(SmallInteger, nullable=False, server_default='0')

    entity = relationship('Entity')
    field = relationship('Field')


engine = create_engine('mysql+pymysql://zhoujing:123@192.168.91.128:3306/cmdb',echo=True)

def create_all():
    Base.metadata.create_all(engine)

def drop_all():
    Base.metadata.drop_all(engine)

Session = sessionmaker(bind=engine)
session = Session()







