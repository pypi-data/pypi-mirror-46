from glove_pybind import *


class Glove:
    def __init__(self):
        self.inputFile = "small_text"
        self.logdir = "log/"
        self.coFileName = "cooccur.bin"
        self.vocabFileName = "vocab.txt"
        self.tempFileName = "temp.bin_"
        self.embdFile = "wordvec.txt"
        self.vocab_size = 0
        self.max_size = 1e7
        self.min_count = 1
        self.window = 10
        self.embed_size = 80
        self.epoch = 1
        self.threshold = 1000000
        self.threads = 40
        self.seed = 20
        self.init_epoch = 0
        self.lr = 0.05
        self.keep_case = 0
        self.symmetric = 1

    def train(self, file):
        self.model = glove()
        self.model.train(file)


if __name__ == "__main__":
    model = Glove()
    model.train("small_text")
