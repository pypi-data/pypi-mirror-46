import base64, json
from datetime import datetime, date, timedelta

class DevlObject(object):

    def __init__(self,**kwarg):
        self.from_json(**kwarg)

    def from_json(self,**kwarg):
        if not kwarg:
            raise Exception("kwarg is None")
        self.__dict__ = {}
        for a,b in kwarg.items():
            if type(b) is dict:
                b = DevlObject(**b)
            elif type(b) is list:
                c = []
                for d in b:
                    if type(d) is dict:
                        d = DevlObject(**d)
                    c.append(d)
                b = c
            self.__dict__[a] = b
        
    def to_json(self):
        d = {}
        for key, value in self.__dict__.items():
            if value != None:
                if type(value) is DevlObject:
                    value = value.to_json()
                elif isinstance(value, (str,int)):
                    value = value
                elif isinstance(value, bytes):
                    value = base64.b64encode(value).decode('ascii')
                elif isinstance(value, datetime):
                    value = value.isoformat()
                elif type(value) is list:
                    a = []
                    for b in value:
                        if type(b) is DevlObject:
                            b = b.to_json()
                        elif isinstance(b, (str,int)):
                            b = b
                        elif isinstance(b, bytes):
                            b = base64.b64encode(b).decode('ascii')
                        elif isinstance(b, datetime):
                            b = b.isoformat()
                        a.append(b)
                    value = a
                else:
                    value = repr(value)
                d[key] = value
        return d

    def stringify(self):
        return json.dumps(self.to_json(),**{"sort_keys":True,"indent":4})

    def __repr__(self):
        return f"{self.stringify()}"

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

if __name__ == '__main__':
    b = {
            "Creator": "Aditya Nugraha",
            "Support": [
                "Ammar Faizi",
                "Lonami",
                "Hibiki"
            ]
        }
    a = DevlObject(**b)
    print(a.stringify())