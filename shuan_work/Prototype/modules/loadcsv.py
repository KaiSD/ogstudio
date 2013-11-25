#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Shuan gameplay prototype CSV loader

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

import csv, codecs

NUMBS = ('0', '1', '2', '3', '4', '5', '6', '7', '8','9')

class LoadCSV:
    '''
    Class for reading CSV files.
    '''
    class Reader:
        class Recoder:
            def __init__(self, f, encoding):
                self.reader = codecs.getreader(encoding)(f)
        
            def __iter__(self):
                return self
        
            def next(self):
                return self.reader.next().encode("utf-8")
        
        def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
            f = self.Recoder(f, encoding)
            self.reader = csv.reader(f, dialect=dialect, **kwds)
    
        def next(self):
            row = self.reader.next()
            return [unicode(s, "utf-8") for s in row]
    
        def __iter__(self):
            return self
    
    def __init__(self, filename, encoding='utf-8', delimiter=';', quotechar='"', **kwargs):
        csvfile = self.Reader(open(filename), encoding=encoding, delimiter=delimiter, quotechar=quotechar)
        sourceData = []
        sourcekeys = None
        
        if kwargs.get('transpose', False):
            sourcekeys = []
            rowData = []
            for i in csvfile:
                sourcekeys.append(i[0])
                for k in xrange(1, len(i)):
                        sourceData.append([])
                        try:
                            i[k] = int(i[k])
                        except:
                            try:
                                i[k] = float(i[k])
                            except:
                                i[k] = i[k]
                rowData.append(i[1:])
            sourceData = list(map(lambda *x:x, *rowData))
        else:
            for i in csvfile:
                if sourcekeys is None:
                    sourcekeys = i
                else:
                    for k in xrange(0, len(i)):
                            try:
                                i[k] = int(i[k])
                            except:
                                try:
                                    i[k] = float(i[k])
                                except:
                                    i[k] = i[k]
                    sourceData.append(i)
        self.keys = sourcekeys
        self.rows = sourceData
    
    def __getitem__(self, pair):
        '''
        Returns a value for given key and row. 
        '''
        key = pair[0]
        row = pair[1]
        
        keys = self.keys
        rows = self.rows
        if key in keys:
            if len(rows) > row:
                return rows[row][keys.index(key)]
            else:
                raise BaseException('Row %i not found in data' % (row))
        else:
            raise BaseException('Named value %s not found in data' % (key))
    
    def __setitem__(self, pair, value):
        '''
        Sets a value for given key and row.  
        '''
        key = pair[0]
        row = pair[1]
        
        keys = self.keys
        rows = self.rows
        if key in keys:
            if len(rows) > row:
                rows[row][keys.index(key)] = value
            else:
                raise BaseException('Row %i not found in data' % (row))
        else:
            raise BaseException('Named value %s not found in data' % (key))
    
    def __str__(self):
        '''
        Returns data as string.
        '''
        return str((self.keys, self.rows))
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.rows)
    
    def has_key(self, key):
        '''
        Returns True if given key exists in data
        '''
        return key in self.keys
    
    def getDictByIndex(self, index):
        '''
        Returns the dict for given index
        '''
        
        out = {}
        keylist = self.keys
        
        for k in keylist:
            val = self[k, index]
            if val == 'True':
                val = True
            elif val == 'False':
                val = False
            elif val == 'None':
                val = None
            kv = k
            mult = False
            while kv[-1] in NUMBS and len(kv) > 0:
                kv = kv[:-1]
                mult = True
            if not kv:
                kv = k
            if mult:
                out[kv] = out.get(kv, [])
                if not val == '':
                    out[kv].append(val)
            else:
                if not val == '':
                    out[kv] = val
                else:
                    out[kv] = None
        return out