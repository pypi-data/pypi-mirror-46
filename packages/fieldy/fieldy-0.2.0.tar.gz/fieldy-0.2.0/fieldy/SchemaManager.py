import json
from fieldy import Util

class SchemaManager:
  def __init__(self, base_path = None):
    self.base_path = base_path
    self.schemas = {}
  
  def load(self, name):
    file = open(self.base_path + name + '.json', 'r')
    txt = file.read()
    file.close()
    schema = json.loads(txt)
    if name != schema['typename']:
      raise Exception('File {} doesn\'t match typename {}'.format(name, schema['typename']))
    self.schemas[name] = schema
    for field_name in schema['fields']:
      field = schema['fields'][field_name]
      field_type = field["type"]
      while field_type[0] == "[" and field_type[-1] == "]":
        field_type = field_type[1:-1]
      if field_type in Util.get_base_types():
        continue
      if field_type not in self.schemas.keys():
        self.load(field_type)