
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

    Glove(std::string input_file, std::string log_dir, std::string cofile, std::string vocab_file,
          std::string temp_file, std::string embd_file, unsigned long long vocab_size, unsigned long long max_size,
          unsigned long min_count, unsigned long window, unsigned long embed_size, unsigned long epoch,
          int threads, double lr, bool keep_case,
          bool symmetric);

    Glove(std::vector<std::string> args_cmd);

    void train(string input_file);

    void load(std::string vocab_file, std::string wordvec_file, std::string meta_file);
    void to_txt();

    AnalogyPairs most_similary(const std::string &word, unsigned long num);
};


#endif //GLOVE_GLOVE_H
