from glove_pybind import *

model = glove()
# model.epochs = 3
# model.train("small_text")

# vocabFile, std::string wordvecFile, std::string metaFilel

model.load("log/vocab.txt", "log/wordvec.txt", "log/wordvec.txt.meta")
words = model.most_similary("one", 10)
print(words)
