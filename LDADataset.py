class LDADataset:
    localDict = Dictionary()			# local dictionary
    docs = {} 		                    # a list of documents
    m, v = 0, 0 			 		    # number of documents and words
    lid2gid = {}

    globalDict = Dictionary()


    def setM(self, m):
        self.m = m

    def setDictionary(self, globalDict):
        self.lid2gid = {}
        self.globalDict = globalDict

    def setDoc(self, doc, idx):
        if idx < len(docs):
            docs.update({idx: doc})
        else:
            docs.setdefault(idx, doc)


    def addDoc(self, str, unlabeled):
        labels = []
        if str.startswith("["):
            labelsBoundary = str[1:].split("]", 1)
            labelStrs = labelsBoundary[0].strip().split("[ \\t]")
            str = labelsBoundary[1].strip()

            if unlabeled is None:
                label_set = []
                for labelStr in labelStrs:
                    try:
                        label_set.append(int(labelStr.strip()))
                    except ValueError:
                        print("Unknown document label ( " + labelStr + " ) for document " + len(docs) + ".")
                labels.extend(label_set)
                labels.sort()

        words = str.split("[ \\t\\n]")
        ids = []
        for word in words:
            if word.strip() == "":
                continue

            _id = len(self.localDict.word2id)

            if self.localDict.contains_word(word):
                _id = localDict.get_id(word)

            if self.globalDict is not None:
                if self.globalDict.contains_word(word):
                    self.localDict.add_word(word)
                    self.lid2gid.update({_id: self.globalDict.get_id(word)})
                    ids.append(_id)
            else:
                self.localDict.add_word(word)
                ids.append(_id)

        self.setDoc(Document(ids, str, labels), len(docs))
        self.v = len(self.localDict.word2id)

    def readDataSet(self, filename, unlabeled):
        try:
            line = filename.readline()
            while line is not None:
                self.addDoc(line, unlabeled)
                line = filename.readline()
            self.setM(len(docs))

            print("Dataset loaded...")
            print("\tM:" + self.m)
            print("\tV:" + self.v)

            return True
        finally:
            return
