from glove_pybind import *


class Glove:
    def __init__(self, input_file="small_text", log_dir="log/", cofile="cooccur.bin", vocab_file="vocab.txt",
                 temp_file="temp.bin_", embd_file="wordvec.txt", vocab_size=0, max_size=10000000, min_count=1,
                 window=10, embed_size=80, epoch=1,  threads=40, lr=0.05, keep_case=0,
                 symmetric=1):

            self.model = glove()
            self.model.input_file = input_file
            self.model.log_dir = log_dir
            self.model.cofile = cofile
            self.model.vocab_file = vocab_file
            self.model.temp_file = temp_file
            self.model.embd_file = embd_file
            self.model.vocab_size = vocab_size
            self.model.max_size = max_size
            self.model.min_count = min_count
            self.model.window = window
            self.model.epoch = epoch
            self.model.threads = threads
            self.model.lr = lr
            self.model.keep_case = keep_case
            self.model.symmetric = symmetric

    def to_txt(self):
        self.model.to_txt()

    def train(self, file):
        self.model.train(file)

    def most_similary(self, word, num):
        self.model.most_similary(word, num)

    def load(self, vocab_file, wordvec_file, meta_file):
        self.vocab_file = "vocab.txt"
        self.model.load(vocab_file, wordvec_file, meta_file)




if __name__ == "__main__":
    model = Glove()
    model.train("small_text")
