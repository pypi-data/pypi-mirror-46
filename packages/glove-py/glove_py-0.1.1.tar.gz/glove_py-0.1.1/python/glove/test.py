# import pybind
from pybind import *

para = {"inputFile": "small_text",
        "logdir": "log/",
        "coFileName": "cooccur.bin",
        "vocabFileName": "vocab.txt",
        "tempFileName": "temp.bin_",
        "embdFile": "wordvec.txt",
        "vocab_size": 0,
        "max_size": 1e7,
        "min_count": 1,
        "window": 10,
        "embed_size": 80,
        "epoch": 5,
        "threshold": 1000000,
        "threads": 40,
        "seed": 20,
        "init_epoch": 0,
        "lr": 0.05,
        "keep_case": False,
        "symmetric": True,
        }

# a = args()

voc = glove()

voc.train("small_text")
# voc = Glove()
# print(dir(Glove))
# co.build()

# print(dir(pybind))
# print(pybind.__dict__)
