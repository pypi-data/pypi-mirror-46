
#ifndef GLOVE_GLOVE_H
#define GLOVE_GLOVE_H

#include <iostream>
#include <vector>
#include "utils.h"
#include "vocabulary.h"
#include "cooccur.h"
#include "train.h"
#include "args.h"

class Glove : public Args {
public:

    Vocabulary voca;
    Train model;

    Glove();

    Glove(std::string inputFile, std::string logdir, std::string coFileName, std::string vocabFileName,
          std::string tempFileName, std::string embdFile, unsigned long long vocab_size, unsigned long long max_size,
          unsigned long min_count, unsigned long window, unsigned long embed_size, unsigned long epoch,
          unsigned long threshold, int threads, int seed, unsigned long init_epoch, double lr, bool keep_case,
          bool symmetric);

    Glove(std::vector<std::string> args_cmd);

    void train(string inputFile);

    void load(std::string vocabFile, std::string wordvecFile, std::string metaFile);
    void to_txt();

    AnalogyPairs most_similary(const std::string &word, unsigned long num);
};


#endif //GLOVE_GLOVE_H
