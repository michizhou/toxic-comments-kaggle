import io.IOBase

class Dictionary:
    def __init__(self):
        self.word2id = {}
        self.id2word = {}

    def get_word(self, id):
        return self.id2word.get(id)

    def get_id(self, word):
        return self.word2id.get(word)

    def contains_word(self, item):
        return True if item in self.word2id else False

    def contains_id(self, item):
        return True if item in self.id2word else False

    def add_word(self, word):
        if self.contains_word(word):
            id = len(word2id)
            word2id.setdefault(word, id)
            id2word.setdefault(id, word)
            return id
        else:
            return self.get_id(word)

    def read_word_map(self, wordMapFile):
        try:
            count = 0
            while wordMapFile.readline() is not None:
                line = wordMapFile.readline()
                word = line.trim()
                self.id2word.setdefault(count, word)
                self.word2id.setdefault(word, count)
                count += 1
            return True
        except IOError:
            print("Error while reading dictionary: " + wordMapFile)
            return False

    def write_word_map(self, wordMapFile):
        try:
            for i in range(len(self.id2word)):
                write(self.id2word.get(i) + "\n")
            return True
        except IOError:
            print("Error while writing word map: " + wordMapFile)
            return False
