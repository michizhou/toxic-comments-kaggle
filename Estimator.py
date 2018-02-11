import math

class Estimator:
    def __init__(self, option):
        self.option = option
        self.trnModel = Model(option)
        if option.est:
            self.trnModel.init(True)
        elif option.estc:
            self.trnModel.init(False)

    def estimate(self):
        print("Sampling " + self.trnModel.niters + " iterations!")
        print("Iteration")
        startIter = self.trnModel.liter + 1
        while self.trnModel.liter <= startIter - 1 + self.trnModel.niters:
            '{:>6}'.format(self.trnModel.liter)

            for m in range(self.trnModel.m):
                for n in range(len(self.trnModel.data.docs[m])):
                    topic = sampling(m, n)
                    self.trnModel.z[m][n] = topic

            if (self.trnModel.liter == startIter - 1 + self.trnModel.niters) or (self.trnModel.liter > self.trnModel.nburnin and self.trnModel.liter % self.trnModel.samplingLag == 0):
                self.trnModel.updateParams()

            print("\b\b\b\b\b\b")
            self.trnModel.liter += 1
        self.trnModel.liter -= 1

        print("\nSaving the final model!")
        self.trnModel.saveModel()


    def sampling(self, m, n):
        topic = self.trnModel.z[m][n]
        w = self.trnModel.data.docs[m].words[n]

        self.trnModel.nw[w][topic] -= 1
        self.trnModel.nd[m][topic] -= 1
        self.trnModel.nwsum[topic] -= 1
        self.trnModel.ndsum[m] -= 1

        v_beta = self.trnModel.v * self.trnModel.beta

        labels = trnModel.data.docs[m].labels

        k_m = self.trnModel.k if labels is None else len(labels)

        p = self.trnModel.p
        for k in range(k_m):
            topic = k if labels is None else labels[k]

            p[k] = (self.trnModel.nd[m][topic] + self.trnModel.alpha) * (self.trnModel.nw[w][topic] + self.trnModel.beta) / (self.trnModel.nwsum[topic] + v_beta)

        for k in range(k_m):
            p[k] += p[k - 1]

        u = Math.random() * p[k_m - 1]

        for topic in range(k_m):
            if p[topic] > u:
                break

        if labels is not None:
            topic = labels[topic]


        self.trnModel.nw[w][topic] += 1
        self.trnModel.nd[m][topic] += 1
        self.trnModel.nwsum[topic] += 1
        self.trnModel.ndsum[m] += 1

        return topic;
    }
