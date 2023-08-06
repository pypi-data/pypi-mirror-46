#MIT License

#Copyright (c) 2019 Paul Harwood

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import json, types, sys
from enum import Enum
from datetime import datetime
import logging
from google.cloud import datastore
from google.cloud.datastore.helpers import GeoPoint
import requests
from . import helpers
from attrdict import AttrDict
import threading

__all__ = ["Modal", "Key", "Query", "Client", "ndb", "GeoPt"]

client_store = threading.local()

def get_client():
    if not hasattr(client_store, 'client'):
        client_store.client = Client()
    return client_store.client

          
class GeoPt(datastore.helpers.GeoPoint):
    def __init__(self, lat, long):
        if isinstance(lat, float) and isinstance(long, float):
            return super().__init__(lat, long)
        else:
            try:
                if lat == "" or 0:
                    lat = 0.0
                else:
                    lat = float(lat)
                if long == "" or 0:
                    long = 0.0
                else:
                    long = float(long)
                if isinstance(lat, float) and isinstance(long, float):
                    return super().__init__(lat, long)  
                else:
                    raise TypeError("GeoPt - input paramaters cannot be converted to float")
            except Exception as e:
                raise TypeError("GeoPt - input paramaters cannot be converted to float :  " + str(e))
            

class Client(datastore.Client):
    def query(self, **kwargs):
        if "client" in kwargs:
            raise TypeError("Cannot pass client")
        if "project" in kwargs:
            raise TypeError("Cannot pass project")
        kwargs["project"] = self.project
        if "namespace" not in kwargs:
            kwargs["namespace"] = self.namespace
        return Query(self, **kwargs)

class Key(datastore.Key):
    def __init__(self, *args, **kwargs):
        self._class_object = kwargs['class_obj']
        project = get_client().project
        kwargs['project'] = project
        super().__init__(*args, **kwargs)
    
    def get(self, **kwargs):
        item = get_client().get(self, **kwargs)
        if item:
            item.__class__ = self._class_object
            item.schema()
        return item
    
    def delete(self):
        return get_client().delete(self)

class Query(datastore.Query):
    _class_object = object
    
    def fetch(self, *args, **kwargs):
        item_list = super().fetch(*args, **kwargs)
        response = []
        for item in item_list:
            item.__class__ = self._class_object
            item.schema()
            response.append(item)
        return response
    
    def get(self, *args, **kwargs):
        #TODO make this more eficient by not calling the entire iterator
        list = self.fetch(*args, **kwargs)
        if len(list) > 0:
            return list[0]
        else:
            return None
        
class ndb(Enum):
    IntegerProperty = (0, True, int)
    FloatProperty = (1, False, float)
    StringProperty = (2, True, str)
    TextProperty = (3, False, str)
    BooleanProperty = (4, True, bool)
    DateTimeProperty = (5, True, datetime)
    GeoPtProperty = (6, True, GeoPt)
    KeyProperty = (7, True, Key)
    JsonProperty = (8, False, str)
    EnumProperty = (9, True, int)


class Model(datastore.Entity):
    
    def schema(self):
        try:
            x=self._properties
        except:
            self.update({"_properties":{}})
        return
    
    def __init__(self, **kwargs):
        self.update({"_properties":{}})
        client = get_client()
        self.schema()
        exclude_from_indexes = []
        parent = kwargs.get('parent')
        for name, value in self._properties.items():
            kw = value.get('kwargs')
            prop_type = value.get('type')
            indexed = kw.get('indexed', False)
            default = kw.get('default', False)
            auto_now = kw.get('auto_now', False) or kw.get('auto_now_add', False)
            repeated = kw.get('repeated', False)
            if repeated:
                self[name] = []
            if not (prop_type.value[1] or indexed):
                if name not in self.get('exclude_from_indexes', []):
                    exclude_from_indexes.append(name)
            if default:
                setattr(self, name, default)
            if auto_now and prop_type == ndb.DateTimeProperty:
                setattr(self, name, datetime.now())
        super().__init__(key=client.key(type(self).__name__, parent=parent), exclude_from_indexes= exclude_from_indexes )
        if kwargs:
            self.populate(**kwargs)
        return
    
    def __getattr__(self, name):
        if name == '_properties':
            return self['_properties']
        if name in self._properties:
            try:
                return getattr(self, self._properties[name]['type'].name)(name)
            except:
                return None
        else:
            try:
                return self[name]
            except:
                return None
        
    def __setattr__(self, name, value):
        if name == '_properties':
            self[name] = value
            return
        if name in self._properties:
            return getattr(self, "set_" + self._properties[name]['type'].name)(name, value)
        else:
            try:
                self[name] = value
            except:
                raise AttributeError("No such attribute: " + str(name))
    
    def __getstate__(self):
        dummy = self.__dict__
        dummy.update({'key': self.key})
        for name in self._properties:
            dummy.update({name: self.__getattr__(name)})
        dummy.update({'_properties': self._properties})
        return dummy
    
    def __setstate__(self, dict):
        self._properties = dict.pop('_properties')
        for name, value in dict.items():
            if value is not None:
                self.__setattr__(name, value)
        return

    def items(self):
        dummy = {}
        for key in self._properties:
            value = self.get(key, None)
            if value != None:
                dummy.update({key:value})
        return dummy.items()    
    
    @classmethod
    def query(cls, *args, **kwargs):
        my_class = cls.__name__
        client = Client()
        kwargs.update(kind=my_class)
        response = client.query(*args, **kwargs)
        response.__class__ = Query
        response._class_object = cls
        return response
    
    @classmethod
    def get_by_id(cls, id, **kwargs):

        return cls.Key(id, **kwargs).get()
    
    def put(self):
        client = Client()
        client.put(self)
        return
    
    def populate(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return
    
    def delete(self):
        return self.get_key().delete()
    
    @classmethod
    def Key(cls, id, **kwargs):
        my_class = cls.__name__
        return Key(my_class, id, class_obj=cls, **kwargs )

    def get_key(self):
        key = self.key
        key.__class__ = Key
        return key
    
    def Property(self, name, prop_type, **kwargs):
        details =  {
            'type': prop_type,
            'kwargs': kwargs
        }
        self._properties.update({name:details})
        return
    
    def setter(self, name, value):
        typeof = self._properties[name]['type'].value[2]
        repeated = helpers.to_bool(self._properties[name]['kwargs'].get('repeated', False))
        if repeated:
            if self[name] and (type(self[name]) == list) and type(value) == typeof:
                self[name].append(value)
            elif type(value) == list:
                for item in value:
                    if type(item) != typeof:
                        raise TypeError(name + " takes " + str(typeof) + " but received " + str(type(item)))
                self[name] = value
            elif type(value) == typeof:
                self[name] = [value]
        elif isinstance(value, typeof): 
                self[name] = value
        else:
            raise TypeError(name + " takes " + str(typeof) + " but received " + str(type(value)))
    
    def IntegerProperty(self, name):
        return self[name]
    
    def set_IntegerProperty(self, name, value):
        return self.setter(name, value)
    
    def StringProperty(self, name):
        return self[name]
    
    def set_StringProperty(self, name, value):
        return self.setter(name, value)
    
    def GeoPtProperty(self, name):
        return self[name]
    
    def set_GeoPtProperty(self, name, value):
        return self.setter(name, value)
    
   
    def EnumProperty(self, name):
        enum = self._properties[name]['kwargs']['enum']
        if not enum:
            raise TypeError("EnumProperty must have enum")
        return enum(self[name])
    
    def set_EnumProperty(self, name, value):
        if isinstance(value, Enum):
            return self.setter(name, value.value)
        else:
            raise TypeError("EnumProperty must have enum - received - " + str(type(value)))
    
    def DateTimeProperty(self, name):
        return self[name]
    
    def set_DateTimeProperty(self, name, value):
        return self.setter(name, value) 
    
    def BooleanProperty(self, name):
        return self[name]
    
    def set_BooleanProperty(self, name, value):
        return self.setter(name, value)  
    
    def TextProperty(self, name):
        return self[name]
    
    def set_TextProperty(self, name, value):
        return self.setter(name, value)    

    def JsonProperty(self, name):
        value = self[name]
        if isinstance(value, list):
            response = []
            for item in value:
                response.append(json.loads(item,object_hook=AttrDict))
            return response
        else:
            return json.loads(value,object_hook=AttrDict)
    
    def set_JsonProperty(self, name, value):
        if isinstance(value, dict):
            value = json.dumps(value)
        elif isinstance(value, list):
            repeated = helpers.to_bool(self._properties[name]['kwargs'].get('repeated', False))
            if repeated:
                value = [json.dumps(v) for v in value]
            else:
                value = json.dumps(value)
        return self.setter(name, value)
    
    def KeyProperty(self, name):
        kind = self._properties[name]['kwargs']['kind']
        if not kind:
            raise TypeError("KeyProperty must have kind")
        value = self[name]
        try:
            if isinstance(value, list):
                response = []
                for item in value:
                    item.__class__ = Key
                    item._class_object = kind
                    response.append(item)
                return response
            else:
                value.__class__ = Key
                value._class_object = kind
                return value
        except Exception as e:
            raise TypeError("bad type in KeyProperty" + str(e))         
    
    def set_KeyProperty(self, name, value):
        kind = self._properties[name]['kwargs']['kind']
        if isinstance(value, Key):
            if value.kind == kind.__name__:
                return self.setter(name, value)
            else:
                raise TypeError("Exepected key of kind : " + kind.__name__ + ". Received :" + value.kind())
        elif isinstance(value, list):
            for item in value:
                try:
                    assert item.kind == kind.__name__
                except:
                    raise
            return self.setter(name, value)
        else:
            raise TypeError("KeyProperty must be a ndb.Key - received - " + str(type(value)))        
