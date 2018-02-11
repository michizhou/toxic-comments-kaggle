import math
import re

class Model:
    tassignSuffix = ".tassign.gz"	 # suffix for topic assignment file
    thetaSuffix   = ".theta.gz"    # suffix for theta (topic - document distribution) file
    phiSuffix     = ".phi.gz"      # suffix for phi file (topic - word distribution) file
    othersSuffix  = ".others.gz" 	 # suffix for containing other parameters
    twordsSuffix  = ".twords.gz"	 # suffix for file containing words-per-topics
    wordMapSuffix  = ".wordmap.gz" # suffix for file containing word to id map

    dir = "./"
    dfile = "trndocs.dat"
    unlabeled = False
    modelName = "model"

    m = 0          # dataset size (i.e., number of docs)
    v = 0          # vocabulary size
    k = 100        # number of topics
    alpha = 0       # LDA hyperparameters
    beta = 0.01     # LDA hyperparameters
    niters = 1000  # number of Gibbs sampling iteration
    nburnin = 500  # number of Gibbs sampling burn-in iterations
    samplingLag = 5 # Gibbs sampling sample lag
    numSamples = 1  # number of samples taken
    liter = 0      # the iteration at which the model was saved
    twords = 20    # print out top words per each topic

    # Estimated/Inferenced parameters
    theta = [[]] # theta: document - topic distributions, size M x K
    phi = [[]]   # phi: topic-word distributions, size K x V

    # Temp variables while sampling
    z = []      # topic assignments for words, size M x doc.size()
    nw = [[]]       # nw[i][j]: number of instances of word/term i assigned to topic j, size V x K
    nd = [[]]        # nd[i][j]: number of words in document i assigned to topic j, size M x K
    nwsum = []      # nwsum[j]: total number of words assigned to topic j, size K
    ndsum = []     # ndsum[i]: total number of words in document i, size M

    nw_inf = []       # nw[m][i][j]: number of instances of word/term i assigned to topic j in doc m, size M x V x K
    nwsum_inf = [[]]      # nwsum[m][j]: total number of words assigned to topic j in doc m, size M x K

    # temp variables for sampling
    p = []

    def __init__(self, option, trnModel=None):
        self.modelName = option.modelName
        self.k = option.k
        self.alpha = option.alpha
        if self.alpha < 0.0:
            self.alpha = 50.0 / k
        if option.beta >= 0:
            self.beta = option.beta
        self.niters = option.niters
        self.nburnin = option.nburnin
        self.samplingLag = option.samplingLag

        self.dir = option.dir
        if self.dir.endswith(File.separator):
            self.dir = self.dir.substring(0, dir.length - 1)

        self.dfile = option.dfile
        self.unlabeled = option.unlabeled
        self.twords = option.twords

        self.data = LDADataset()

        if trnModel is not None:
            self.data.setDictionary(trnModel.data.localDict)
            self.k = trnModel.k

            if option.alpha < 0.0:
                self.alpha = trnModel.alpha
            if option.beta < 0.0:
                self.beta = trnModel.beta

        data.readDataSet(self.dir + File.separator + self.dfile, self.unlabeled)

    def init(self, random):
        if random:
            self.m = data.m
            self.v = data.v
            self.z = [0 * self.m]
        else:
            if loadModel() is False:
                print("Fail to load word-topic assignment file of the model!")
                return False
            print("Model loaded:")
            print("\talpha:" + self.alpha)
            print("\tbeta:" + self.beta)
            print("\tK:" + self.k)
            print("\tM:" + self.m)
            print("\tV:" + self.v)

        self.p = [0.0 * self.k]

        initSS()

        for m in range(self.data.m):
            if random:
                self.z[m] = []
            n = len(self.data.docs[m])
            for j in range(n):
                w = self.data.docs[m].words[j]
                topic = 0
                if random:
                    topic = floor(random() * k)
                    self.z[m].append(topic)
                else:
                    topic = self.z[m][n]

                self.nw[w][topic] += 1
                self.nd[m][topic] += 1
                self.nwsum[topic] += 1
            self.ndsum[m] = n

        self.theta = [[0.0 for i in range(self.k)] for j in range(self.m)]
        self.phi = [[0.0 for i in range(self.v)] for j in range(self.k)]

        return True

    def init_inf(self, random):
        self.nw_inf = []
        self.nwsum_inf = [[0 for i in range(self.k)] for j in range(self.m)]

        for m in range(self.m):
            self.nw_inf[m] = []
            n = len(self.data.docs[m])
            for i in range(n):
                w = self.data.docs[m]
                topic = self.z[m][i]

                if w not in self.nw_inf[m]:
                    nw_inf_m_w = [0 * self.k]
                    self.nw_inf[m][w] = nw_inf_m_w

                self.nw_inf[m][w][topic] += 1
                self.nwsum_inf[m][topic] += 1

        return True

    def initSS(self):
        self.nw = [[0 for i in range(self.k)] for j in range(self.v)]
        self.nd = [[0 for i in range(self.k)] for j in range(self.m)]
        self.nwsum = [0 * self.k]
        self.ndsum = [o * self.m]

    def updateParams(self, trnModel=None):
        self.updateTheta()
        if trnModel is None:
            self.updatePhi()
        else:
            self.updatePhi(trnModel)
        self.numSamples += 1

    def updateTheta(self):
        k_alpha = self.k * self.alpha
        for m in range(self.m):
            for k in range(self.k):
                if self.numSamples > 1:
                    self.theta[m][k] *= self.numSamples - 1
                self.theta[m][k] += (self.nd[m][k] + self.alpha) / (self.ndsum[m] + k_alpha)
                if self.numSamples > 1:
                    self.theta[m][k] /= self.numSamples

    def updatePhi(self, trnModel=None):
        if trnModel is None:
            v_beta = self.v * self.beta
        else:
            v_beta = trnModel.v * self.beta
        for k in range(self.k):
            for w in range(self.v):
                if trnModel is None:
                    if self.numSamples > 1:
                        self.phi[k][w] *= self.numSamples - 1
                    self.phi[k][w] += (self.nw[w][k] + self.beta) / (self.nwsum[k] + v_beta)
                    if self.numSamples > 1:
                        self.phi[k][w] /= self.numSamples
                else:
                    if self.data.lid2gid[w] is not None:
                        id = self.data.lid2gid[w]
                        if self.numSamples > 1:
                            self.phi[k][w] *= self.numSamples - 1
                        self.phi[k][w] += (trnModel.nw[id][k] + self.nw[w][k] + self.beta) / (trnModel.nwsum[k] + self.nwsum[k] + v_beta)
                        if self.numSamples > 1:
                            self.phi[k][w] /= self.numSamples

    def saveModel(self, modelPrefix=""):
        if saveModelTAssign(self.dir + File.separator + modelPrefix + self.modelName + self.tassignSuffix) is None:
            return False
        elif saveModelOthers(self.dir + File.separator + modelPrefix + self.modelName + self.othersSuffix) is None:
            return False
        elif saveModelTheta(self.dir + File.separator + modelPrefix + self.modelName + self.thetaSuffix) is None:
            return False
        elif saveModelPhi(self.dir + File.separator + modelPrefix + self.modelName + self.phiSuffix) is None:
            return False
        elif self.twords > 0:
            if saveModelTwords(self.dir + File.separator + modelPrefix + self.modelName + self.twordsSuffix) is None:
                return False
        elif self.data.localDict.writeWordMap(self.dir + File.separator + modelPrefix + self.modelName + self.wordMapSuffix) is None:
            return False
        else:
            return True

    def saveModelTAssign(self, filename):
        try:
            for i in range(self.data.m):
                for j in range(len(self.data.docs[i])):
                    write(self.data.docs[i].words[j] + ":" + self.z[i][j] + " ")
                write("\n")
        except IOError:
            print("Error while saving model tassign: " + filename)
            return False
        return True

    def saveModelTheta(self, filename):
        try:
            for i in range(self.m):
                for j in range(self.k):
                    if self.theta[i][j] > 0:
                        write(j + ":" + self.theta[i][j] + " ")
                write("\n")
        except IOError:
            print("Error while saving topic distribution file for this model: " + filename)
            return False
        return True

    def saveModelPhi(self, filename):
        try:
            for i in range(self.k):
                for j in range(self.v):
                    if self.phi[i][j] > 0:
                        write(j + ":" + self.phi[i][j] + " ")
                write("\n")
        except IOError:
            print("Error while saving word-topic distribution: " + filename)
            return False
        return True

    def saveModelOthers(self, filename):
        try:
            write("alpha=" + self.alpha + "\n")
            write("beta=" + self.beta + "\n")
            write("ntopics=" + self.k + "\n")
            write("ndocs=" + self.m + "\n")
            write("nwords=" + self.v + "\n")
            write("liters=" + self.liter + "\n")
        except IOError:
            print("Error while saving model others: " + filename)
            return False
        return True

    def saveModelTwords(self, filename):
        try:
            if (self.twords > self.v):
                self.twords = self.v
            for k in range(self.k):
                wordsProbsList = []
                for w in range(self.v):
                    p = Pair(w, self.phi[k][w], False)
                    wordsProbsList.append(p)
                write("Topic " + k + ":\n")
                wordsProbsList.sort()

                for i in range(self.twords):
                    if wordsProbsList[i].first in self.data.localDict:
                        word = data.localDict.getWord(wordsProbsList[i].first)
                        write("\t" + word + "\t" + wordsProbsList[i].second + "\n")
        except IOError:
            print("Error while saving model twords: " + filename)
            return False
        return True

    def loadModel(self):
        if readOthersFile(self.dir + File.separator + self.modelName + self.othersSuffix) is None:
            return False

        elif readTAssignFile(self.dir + File.separator + self.modelName + self.tassignSuffix) is None:
            return False

        dict = Dictionary()
        if dict.readWordMap(self.dir + File.separator + self.modelName + self.wordMapSuffix) is None:
            return False
        self.data.localDict = dict

        return True

    def readOthersFile(self, otherFile):
        try:
            line = otherFile.readline()
            while line is not None:
                tokens = re.split(r'( +|\t+|\r+|\n+)', line)
                if len(tokens) != 2:
                    continue
                optstr = tokens[0]
                optval = tokens[1]

                if optstr.lower() == "alpha".lower():
                    self.alpha = optval
                elif optstr.lower() == "beta".lower():
                    self.beta = optval
                elif optstr.lower() == "ntopics".lower():
                    self.k = optval
                elif optstr.lower() == "liter".lower():
                    self.liter = optval
                elif optstr.lower() == "nwords".lower():
                    self.v = optval
                elif optstr.lower() == "ndocs".lower():
                    self.m = optval
                line = otherFile.readline()
        except IOError:
            print("Error while reading other file: " + otherFile)
            return False
        return True


    def readTAssignFile(self, tassignFile):
        try:
            self.z = [0 * self.m]
            self.data = LDADataset()
            self.data.setM(self.m)
            self.data.v = self.v
            for i in range(self.m):
                line = tassignFile.readline()
                tokens = re.split(r'( +|\t+|\r+|\n+)', line)
                length = len(tokens)

                words = []
                topics = []
                for j in range(length):
                    token = tokens[j]
                    tokens2 = token.split(":")
                    if (len(tokens2) != 2):
                        print("Invalid word-topic assignment line\n")
                        return False
                    words.append(tokens2[0])
                    topics.append(tokens2[1])


                doc = Document(words)
                self.data.setDoc(doc, i)

                self.z[i] = []
                for j in range(len(topics)):
                    self.z[i].append(topics[j])
        except IOError:
            print("Error while loading model: " + tassignFile)
            return False
        return True

