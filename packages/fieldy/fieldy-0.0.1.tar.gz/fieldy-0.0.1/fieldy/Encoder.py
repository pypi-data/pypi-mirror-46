from fieldy import Util
from fieldy.Ent import Ent

class Encoder:
  def __init__(self, schema_manager):
    self.schema_manager = schema_manager

  def to_object(self, entry, typename):
    schema = self.schema_manager.schemas[typename]
    if type(entry) != dict:
      raise Exception('Not a dict')
    for field_name in entry.keys():
      field = entry[field_name]
      if field_name not in schema['fields'].keys():
        raise Exception('Field {} not defined in schema'.format(field_name))
    for field_name in schema['fields'].keys():
      field = schema['fields'][field_name]
      if field_name not in entry.keys():
        if field["required"]:
          raise Exception('Missing required field: {}'.field_name)
        continue
      field_type = field["type"]
      obj = Ent()
      if field_type in Util.get_base_types():
        if field_type == "string":
          try:
            setattr(obj, field_name, str(entry[field_name]))
          except:
            raise Exception('Field {} should be a string'.format(field_name))
        if field_type == "integer":
          try:
            setattr(obj, field_name, int(entry[field_name]))
          except:
            raise Exception('Field {} should be a integer'.format(field_name))
        if field_type == "float":
          try:
            setattr(obj, field_name, float(entry[field_name]))
          except:
            raise Exception('Field {} should be a float'.format(field_name))
        if field_type == "boolean":
          try:
            setattr(obj, field_name, bool(entry[field_name]))
          except:
            raise Exception('Field {} should be a boolean'.format(field_name))
      else:
        try:
          setattr(obj, field_name, self.to_object(entry[field_name], schema['fields'][field_name]['type']))
        except Exception as exc:
          raise Exception('Error on field {}: ({})'.format(field_name, str(exc)))
    return obj