from  glove import *

model = glove()
# model.epochs = 3
model.train("/home/wh/Documents/C/wh_glove_study/wh_glove_2/python/glove/small_text")

# vocabFile, std::string wordvecFile, std::string metaFilel

# model.load("log/vocab.txt", "log/wordvec.txt", "log/wordvec.txt.meta")
model.to_txt()
words = model.most_similary("one", 10)
print(words)
