from . import db3
import psycopg2
from .dbtypes import DB_PGSQL, DB_SQLITE3

class open (db3.open):
    def __init__ (self, dbname, user, password, host = '127.0.0.1', port = 5432, dir = None, auto_reload = False):
        if ":" in host:
            host, port = host.split (":")
            port = int (port)
        self.conn = psycopg2.connect (host=host, dbname=dbname, user=user, password=password, port = port)
        self._init (dir, auto_reload, DB_PGSQL)        
        
    def field_names (self):
        return [x.name for x in self.description]
    
    def set_autocommit (self, flag = True):
        self.conn.autocommit = flag


class open2 (open):
    def __init__ (self, conn, pool, dir = None, auto_reload = False, auto_putback = True):
        self.conn = conn
        self.pool = pool       
        self.auto_putback = auto_putback
        self._within_context = False 
        self._init (dir, auto_reload, DB_PGSQL)        
        
    def __enter__ (self):
        self._within_context = True
        return self

    def __exit__ (self, type, value, tb):    
        self._within_context = False
        self.auto_putback and self.putback ()        

    def __del__ (self):        
        if not self.auto_putback and self.c:
            self.putback ()

    def putback (self):
        self.c.close ()
        self.c = None
        self.pool.putconn (self.conn)        

    def commit (self):
        r = open.commit (self)
        if not self._within_context:
            if not self.auto_putback:
                self.putback ()
            else:                
                raise SystemError ("this connection is in pool")
        return r

    def rollback (self):
        r = open.rollback (self)
        if not self._within_context:
            if not self.auto_putback:
                self.putback ()
            else:                
                raise SystemError ("this connection is in pool")
        return r    
    
    def spendmany (self, limit, as_dict = False):        
        rows = self.fetchmany (limit, as_dict)
        if not rows:
            self.putback ()
        return rows
        
    