from utils import getlogger
from db.model import session, FieldMeta, Reference, Field, Value, Entity, Schema
import logging
import math

logger = getlogger(__name__, './{}.log'.format(__name__))

def get_schema_by_name(name:str, deleted=0):
    query = session.query(Schema).filter(Schema.name==name.strip())
    if not deleted:
        query = query.filter(Schema.deleted==deleted)
    return query.first()

def add_schema(name:str, desc:str=None):
    schema = Schema()
    schema.name = name.strip()
    schema.desc = desc
    session.add(schema)
    try:
        session.commit()
        return schema
    except Exception as e:
        session.rollback()
        logger.error('fail to add a schema id={} Error={}'.format(id,e))

def deleted_schema(id:int, deleted=1):
    try:
        schema = session.query(Schema).filter((Schema.id == id) & (Schema.deleted == 0))
        if schema:
            schema.deleted = deleted
            session.add(schema)
            try:
                session.commit()
                return schema
            except Exception as e:
                session.rollback()
                raise e
        else:
            raise ValueError('wrong ID {}'.format(id))
    except Exception as e:
        logger.error('fail to deleted a schema id={} Error={}'.format(id,e))

def list_schema(page:int, size:int, deleted=0):
    try:
        query = session.query(Schema)
        if not deleted:
            query = query.filter(Schema.deleted==0)
        page = page if page > 0 else 1
        size = size if size<100 and size >0 else 20
        count = query.count()
        pages = math.ceil(count/size)
        result = query.limit(size).offset(size*(page-1)).all()

        return result, (page,pages,count,size)
    except Exception as e:
        logger.error(e)

def get_field(schema_name, field_name, deleted=0):
    schema = get_schema_by_name(schema_name)
    if not schema:
        raise ValueError('{} is not a table name'.format(schema_name))

    query = session.query(Field).filter((Field.schema_id == schema.id) & (Field.name==field_name))
    if not deleted:
        query = query.filter(Field.deleted==deleted)
    return query.first()

def table_used(schema_id, deleted=0):
    query = session.query(Entity).filter(Entity.schema_id==schema_id)
    if not deleted:
        query = query.filter(Entity.deleted==deleted)
    return query.first() is not None

def _add_field(field:Field):
    session.add(Field)
    try:
        session.commit()
        return field
    except Exception as e:
        session.rollback()
        logger.error('fail to add field {}  Error :{}'.format(field,e))

def add_field(schema_name,field_name,meta):
    schema = get_schema_by_name(schema_name)
    if not schema:
        raise ValueError('{} is not a tablename'.format(schema_name))
    meta_date = FieldMeta(meta)
    field = Field()
    field.name = field_name.strip()
    field.meta = meta
    if meta_date.reference:
        ref = get_field(meta_date.reference.schema, meta_date.reference.field)
        if not ref:
            raise ValueError('wrong reference {}.{}'\
                             .format(meta_date.reference.schema, meta_date.reference.field))
        field.ref_id = ref.id
    if not table_used(schema.id):
        return _add_field(field)

    if meta_date.nullable():
        return _add_field(field)

    if not meta_date.default:
        raise ValueError('this field requires a default value.')

    else:

        for entity in iter_entities(schema.id):
            value = Value()
            value.entity_id = entity.id
            value.field = field
            value.value = meta_date.default
            session.add(value)
        return _add_field(field)


def iter_entities(schema_id,patch=100):
    page =1
    while True:
        query = session.query(Entity).filter((Entity.schema_id==schema_id) & (Entity.deleted==0))
        result = query.limit(patch).offset((page-1)*patch).all()
        if not result:
            return None
        yield from result
        page += 1








