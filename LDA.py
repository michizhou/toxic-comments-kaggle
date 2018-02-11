import math
import argparse
import sys

class LDA:

    def main(self, argv):
        option = LDACmdOption()
        parser = argparse.ArgumentParser(option)

        try:
            if len(args) == 0:
                showHelp(parser)
                return
            parser.parse_args(argv)

            if option.est or option.estc:
                estimator = Estimator(option)
                estimator.estimate()
            elif option.inf:
                inferencer = Inferencer(option)
                newModel = inferencer.inference()
        except SyntaxError:
            print("Command line error")
            showHelp(parser)
            return
        except FileNotFoundError:
            return
        except RuntimeError:
            print("Error in main")
            return

    def showHelp(self, parser):
        print("LDA [options ...] [arguments...]")
        parser.print_help()

if __name__ == '__main__':
    main(sys.argv[1:])
