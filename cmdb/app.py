# import simplejson
#
# json_string='''{
#     "type":"cmdb.types.Int",
#     "value":"25",
#     "option":{
#     "min":10,
#     "max":30}
#
# }'''
#
# json_string1 = '''{
#     "type":"cmdb.types.Ip",
#     "value":"127.0.0.1,127.0.0.2"
#     "nullable":false,
#     "unique":false,
#     "option":{"prefix":"127.0.0"},
#     "multi":true,
#     "reference":{
#     "schema":1,
#     "field":1,
#     "on_delete":"cascade|set_null|disable",
#     "on_update":"cascade|disable"
#     }
#
# }'''
#
# obj = simplejson.loads(json_string)
# obj1 = simplejson.loads(json_string1)
# from cmdb.types import BaseType,get_instance
# #
# #
# #
# Int = get_instance(obj.get('type'),**obj.get('option'))
# Ip = get_instance(obj1.get('type'),**obj1.get('option'))
# print(Int.stringfy(obj.get('value')))
# print(Ip.stringfy(obj1.get('value')))
#
# from cmdb.db.model import Schema,Field,Entity,Value,drop_all,create_all,session
#
# drop_all()
# create_all()
from cmdb.db.model import Schema,Field,Entity,Value,drop_all,create_all,session