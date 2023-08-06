from fieldy import Util
from fieldy.Ent import Ent
from datetime import datetime

class Encoder:
  def __init__(self, schema_manager):
    self.schema_manager = schema_manager

  def parse_field(self, field_value, field_type, field_name):
    if field_type[0] == '[' and field_type[-1] == ']':
      arr = []
      if type(field_value) != list:
        raise Exception('Field {} should be a list'.format(field_name))
      for ind in range(len(field_value)):
        elem = field_value[ind]
        arr.append(self.parse_field(elem, field_type[1:-1], '{}[{}]'.format(field_name, ind)))
      return arr
    if field_type in Util.get_base_types():
      if field_type == "string":
        try:
          return str(field_value)
        except:
          raise Exception('Field {} should be a string'.format(field_name))
      if field_type == "integer":
        try:
          return int(field_value)
        except:
          raise Exception('Field {} should be a integer'.format(field_name))
      if field_type == "float":
        try:
          return float(field_value)
        except:
          raise Exception('Field {} should be a float'.format(field_name))
      if field_type == "boolean":
        try:
          return bool(field_value)
        except:
          raise Exception('Field {} should be a boolean'.format(field_name))
      if field_type == "date":
        try:
          return datetime.strptime(field_value, '%Y-%m-%d')
        except:
          raise Exception('Field {} should be a date'.format(field_name))
    else:
      try:
        return self.to_object(field_value, field_type)
      except Exception as exc:
        raise Exception('Error on field {}: ({})'.format(field_name, str(exc)))

  def to_object(self, entry, typename):
    schema = self.schema_manager.schemas[typename]
    if type(entry) != dict:
      raise Exception('Not a dict')
    for field_name in entry.keys():
      field = entry[field_name]
      if field_name not in schema['fields'].keys():
        raise Exception('Field {} not defined in schema'.format(field_name))
    obj = Ent()
    for field_name in schema['fields'].keys():
      field = schema['fields'][field_name]
      field_value = field["default"]
      if field_name not in entry.keys():
        if field["required"]:
          raise Exception('Missing required field: {}'.field_name)
      else:
        field_value = entry[field_name]
      if field_value == None:
        if field["required"]:
          raise Exception('Missing required field: {}'.field_name)
        setattr(obj, field_name, None)
        continue
      field_type = field["type"]
      setattr(obj, field_name, self.parse_field(field_value, field_type, field_name))
    return obj