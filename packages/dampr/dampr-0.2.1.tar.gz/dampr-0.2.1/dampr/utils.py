import sqlite3
import os
import glob

def create_table(c):
    c.execute("PRAGMA synchronous = OFF")
    c.execute("PRAGMA journal_mode = MEMORY")
    c.execute("create table if not exists offsets (hash integer, offset integer)")
    c.execute("delete from offsets");

def merge_offsets(paths, out_path):
    out = sqlite3.connect(out_path)
    c = out.cursor()
    create_table(c)

    for path in paths:
        c.execute("attach '{}' as toMerge".format(path))
        c.execute('insert into offsets select * from toMerge.offsets')
        c.execute('detach toMerge')

    create_index(c) 
   
def create_index(c):
    c.execute("CREATE INDEX 'hash_idx' on 'offsets' ('hash')")

def index_file(c, fname, batch_size):
    with open(fname) as f:
        batches = []
        offset = 0 
        for line in f:
            data = json.loads(line)
            for l in (data['listing1'], data['listing2']):
                batches.append((hash((data['query'], l['listingId'])), offset))

            if len(batches) > batch_size:
                c.executemany('INSERT INTO offsets VALUES (?,?)', batches)
                batches = []

            offset += len(line)

    c.commit()

class Indexer(object):
    def __init__(self, path, store):
        self.path = path
        self.store = store

    def index(self, name, key):
        pass
