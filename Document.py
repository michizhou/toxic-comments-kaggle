class Document:
    def __init__(self, doc, rawStr="", tlabels=None):
        self.length = len(doc)
        self.words = []
        for i in range(self.length):
            self.words[i] = doc.get(i)
        self.rawStr = rawStr
        self.labels = tlabels.toArray if tlabels is not None else None

