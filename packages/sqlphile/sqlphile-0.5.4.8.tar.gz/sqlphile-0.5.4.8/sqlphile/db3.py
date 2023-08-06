import sqlite3
import json
import zlib
import sqlphile
from . import sql
from .dbtypes import DB_SQLITE3
from .skitai_compat import dispatch

class AttrDict (dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
        
class open:
    def __init__ (self, path, dir = None, auto_reload = False):        
        self.conn = sqlite3.connect (path, check_same_thread = False)
        self._init (dir, auto_reload, DB_SQLITE3)        
    
    def _init (self, dir, auto_reload, engine):    
        self.create_cursor ()        
        self.sqlphile = sqlphile.SQLPhile (dir, auto_reload, engine = engine, conn = self)
    
    def create_cursor (self):    
        self.cursor = self.c = self.conn.cursor ()        
    
    def set_autocommit (self, flag = None):
       # flags: None (autocommit), DEFERRED, IMMEDIATE or EXCLUSIVE
       self.conn.isolation_level = flag
        
    def __enter__ (self):        
        return self
    
    def __exit__ (self, type, value, tb):        
        self.c.close ()
        self.conn.close ()
        
    def __getattr__ (self, name):
        try: 
            return getattr (self.c, name)
        except AttributeError:
            return getattr (self.sqlphile, name)

    def commit (self):    
        return self.conn.commit ()
    
    def rollback (self):    
        return self.conn.rollback ()    

    def serialize (self, obj):
        return zlib.compress (json.dumps (obj).encode ("utf8"))    
    
    def deserialize (self, data):
        return json.loads (zlib.decompress (data).decode ('utf8'))
    
    def blob (self, obj):
        return sqlite3.Binary (obj)
    
    def field_names (self):
        return [x [0] for x in self.description]
        
    def as_dict (self, row, field_names = None):        
        return AttrDict (dict ([(f, row [i]) for i, f in enumerate (field_names or self.field_names ())]))
    
    def execute (self, sql, *args, **kargs):
        self.cursor.execute (str (sql), *args, **kargs)
        return self
    
    def fetchone (self, as_dict = False):
        try: 
            return self.fetchmany (1, as_dict)[0]
        except IndexError: 
            return None    
        
    def fetchall (self, as_dict = False):
        return self.fetchmany (0, as_dict)
    
    def fetchmany (self, limit, as_dict = False):
        rows = limit and self.cursor.fetchmany (limit) or self.cursor.fetchall ()
        if not as_dict:
            return rows        
        field_names = self.field_names ()
        return [self.as_dict (row, field_names) for row in rows]
    
    def dispatch (self, *args, **kargs):
        return dispatch (self.fetchall (True))

    def one (self, *args, **kargs):
        from skitai import exceptions
        row = self.fetchone (True)
        if row is None:        
            raise exceptions.HTTPError ("409 Conflict")
        return row    
    
    def fetch (self, *args, **kargs):
        return self.fetchall (True)
    

class open2 (open):
    def __init__ (self, conn, dir = None, auto_reload = False):
        self.conn = conn        
        self._init (dir, auto_reload, DB_SQLITE3)
    
    def spendmany (self, limit, as_dict = False):
        # special method for automatic putback
        return self.fetchmany (limit, as_dict)        
        
    def putback (self):
        pass
        
