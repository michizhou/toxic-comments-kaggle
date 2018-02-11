import math

class Inferencer:
    def __init__(self, option):
        self.option = option
        self.trnModel = Model(option)
        self.trnModel.init(False)
        self.globalDict = self.trnModel.data.localDict

    def inference(self):
        self.newModel = Model(self.option, self.trnModel)
        self.newModel.init(True)
        self.newModel.initInf()

        print("Sampling " + self.newModel.niters + " iterations for inference!")
        print("Iteration")

        for self.newModel.liter in range(1, self.newModel.niters + 1):
            '{:>6}'.format(self.newModel.liter)
            for m in range(self.newModel.m):
                for n in range(len(self.newModel.data.docs[m])):
                    topic = self.infSampling(m, n)
                    self.newModel.z[m][n] = topic

            if (self.newModel.liter == self.newModel.niters) or (self.newModel.liter > self.newModel.nburnin and self.newModel.liter % self.newModel.samplingLag == 0):
                self.newModel.updateParams(self.trnModel)

            print("\b\b\b\b\b\b")
        self.newModel.liter -= 1

        print("\nSaving the inference outputs!")
        outputPrefix = self.newModel.dfile
        if outputPrefix.endswith(".gz"):
            outputPrefix = outputPrefix.substring(0, outputPrefix.length() - 3)
        self.newModel.saveModel(outputPrefix + ".")

        return self.newModel


    def infSampling(self, m, n):
        topic = self.newModel.z[m][n]
        _w = self.newModel.data.docs[m].words[n]
        w = self.newModel.data.lid2gid[_w]

        self.newModel.nw[_w][topic] -= 1
        self.newModel.nd[m][topic] -= 1
        self.newModel.nwsum[topic] -= 1
        self.newModel.ndsum[m] -= 1

        nw_inf_m__w = []
        if self.option.infSeparately:
            nw_inf_m__w = self.newModel.nw_inf[m][_w]
            nw_inf_m__w[topic] -= 1
            self.newModel.nwsum_inf[m][topic] -= 1

        v_beta = self.trnModel.v * self.newModel.beta

        labels = self.newModel.data.docs[m].labels

        k_m = self.newModel.k if labels is None else len(labels)

        p = self.newModel.p
        for k in range(k_m):
            topic = k if labels is None else labels[k]

            if option.infSeparately:
                nw_k = nw_inf_m__w[topic]
                nwsum_k = self.newModel.nwsum_inf[m][topic]
            else:
                nw_k = self.newModel.nw[_w][topic]
                nwsum_k = self.newModel.nwsum[topic]

            p[k] = (self.newModel.nd[m][topic] + self.newModel.alpha) * (self.trnModel.nw[w][topic] + nw_k + self.newModel.beta) / (self.trnModel.nwsum[topic] + nwsum_k + v_beta)

        for k in range(k_m):
            p[k] += p[k - 1]

        u = Math.random() * p[k_m - 1]

        for topic in range(k_m):
            if p[topic] > u:
                break

        if labels is not None:
            topic = labels[topic]

        self.newModel.nw[_w][topic] += 1
        self.newModel.nd[m][topic] += 1
        self.newModel.nwsum[topic] += 1
        self.newModel.ndsum[m] += 1

        if option.infSeparately:
            nw_inf_m__w[topic] += 1
            self.newModel.nwsum_inf[m][topic] += 1

        return topic
