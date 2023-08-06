from .common import check_arg
import ldmud, json

class LPCEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ldmud.Array):
            return list(obj)
        if isinstance(obj, ldmud.Mapping):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)

class LPCDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

        self.orig_parse_array = self.parse_array
        self.orig_parse_object = self.parse_object

        self.parse_array = LPCDecoder.parse_array.__get__(self, LPCDecoder)
        self.parse_object = LPCDecoder.parse_object.__get__(self, LPCDecoder)

        self.scan_once = json.scanner.py_make_scanner(self)

    def parse_array(self, *args, **kwargs):
        (val, end) = self.orig_parse_array(*args, **kwargs)
        return (ldmud.Array(val), end)

    def parse_object(self, *args, **kwargs):
        (val, end) = self.orig_parse_object(*args, **kwargs)
        return (ldmud.Mapping(val), end)

def efun_json_serialize(value):
    return json.dumps(value, cls=LPCEncoder)

def efun_json_parse(text):
    return json.loads(text, cls=LPCDecoder)

def register():
    ldmud.register_efun("json_serialize", efun_json_serialize)
    ldmud.register_efun("json_parse", efun_json_parse)
