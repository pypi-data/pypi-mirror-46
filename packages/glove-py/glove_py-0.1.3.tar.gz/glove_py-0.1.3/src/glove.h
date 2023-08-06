
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

    Glove(std::vector<std::string> args_cmd);

    void train(string inputFile);

    void load(std::string vocabFile, std::string wordvecFile, std::string metaFile);

    AnalogyPairs most_similary(const std::string &word, unsigned long num);
};


#endif //GLOVE_GLOVE_H
