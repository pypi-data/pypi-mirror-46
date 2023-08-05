class Node(object):
    CNT = 0
    def __init__(self, name):
        self.name = name
        self.cnt = self.CNT
        Node.CNT += 1

class Input(Node):
    def __init__(self, name, inp):
        super(Input, self).__init__(self, name)
        self.inp = inp

    def __unicode__(self):
        return u"Input[name={}]".format(self.name)

    __repr__ = __unicode__

class Map(Node):
    def __init__(self, name, source, output, mapper):
        super(Map, self).__init__(self, name)
        self.source = source
        self.output = output
        self.mapper = mapper

    def __unicode__(self):
        return u"Map[name={}]".format(self.name)

    __repr__ = __unicode__

class GroupByKey(Node):
    def __init__(self, name, source, output, combiner, shuffler, options=None):
        super(GroupByKey, self).__init__(self, name)
        self.source = source
        self.output = output
        self.combiner = combiner
        self.shuffler = shuffler

    def __unicode__(self):
        return u"GroupByKey[name={}]".format(self.name)

class Reduce(Node):
    def __init__(self, name, source, output, reducer):
        super(Reduce, self).__init__(self, name)
        self.output = output
        self.source = source
        self.reducer = reducer

    def __unicode__(self):
        return u"Reducer[name={}]".format(self.name)

    __repr__ = __unicode__

class Sink(Node):
    def __init__(self, name, source, output, mapper, path):
        super(Sink, self).__init__(self, name)
        self.source = source
        self.output = output
        self.mapper = mapper
        self.path = path

    def __unicode__(self):
        return u"Sink[path={}]".format(self.path)

    __repr__ = __unicode__

class Flatten(Node):
    def __init__(self, name, souces, output):
        super(Flatten, self).__init__(self, name)
        self.sources = sources
        self.output = output

