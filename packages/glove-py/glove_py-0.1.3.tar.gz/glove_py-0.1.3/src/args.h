#ifndef POINT2VEC_UNIT_H
#define POINT2VEC_UNIT_H

#include <iostream>
#include <vector>

using namespace std;

class Args {
public:
    std::string inputFile = "small_text";
    std::string logdir = "log/";
    std::string coFileName = "cooccur.bin";
    std::string vocabFileName = "vocab.txt";
    std::string tempFileName = "temp.bin_";
    std::string embdFile = "wordvec.txt";

    unsigned long long vocab_size = 0;//vocab_size已经在args里面赋值
    unsigned long long max_size = 1e7;//vocab_size已经在args里面赋值
    unsigned long min_count = 1;
    unsigned long window = 10;
    unsigned long embed_size = 80;
    unsigned long epoch = 1;
    unsigned long threshold = 1000000;
    int threads = 40;
    int seed = 20;


    unsigned long init_epoch = 0;
    double lr = 0.05;
    bool keep_case = false;
    bool symmetric = true;


    void printHelp();

    void parseArgs(const std::vector<std::string> &args);
};

#endif //POINT2VEC_UNIT_H
