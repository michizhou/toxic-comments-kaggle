class LDACmdOption:

    @Option(name="-est", usage="Specify whether we want to estimate model from scratch")
        est = False

    @Option(name="-estc", usage="Specify whether we want to continue the last estimation")
        estc = False

    @Option(name="-inf", usage="Specify whether we want to do inference")
        inf = True

    @Option(name="-infseparately", usage="Do inference for each document separately")
        infSeparately = False

    @Option(name="-unlabeled", usage="Ignore document labels")
        unlabeled = False

    @Option(name="-dir", usage="Specify directory")
        dir = ""

    @Option(name="-dfile", usage="Specify data file (*.gz)")
        dfile = ""

    @Option(name="-model", usage="Specify the model name")
        modelName = ""

    @Option(name="-alpha", usage="Specify alpha")
        alpha = -1

    @Option(name="-beta", usage="Specify beta")
        beta = -1

    @Option(name="-ntopics", usage="Specify the number of topics")
        K = 100

    @Option(name="-niters", usage="Specify the number of iterations")
        niters = 1000

    @Option(name="-nburnin", usage="Specify the number of burn-in iterations")
        nburnin = 500

    @Option(name="-samplinglag", usage="Specify the sampling lag")
        samplingLag = 5

    @Option(name="-twords", usage="Specify the number of most likely words to be printed for each topic")
        twords = 100
