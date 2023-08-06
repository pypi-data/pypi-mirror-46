//
// Created by root on 19-5-15.
//

#include "glove.h"

Glove::Glove(std::string inputFile, std::string logdir, std::string coFileName, std::string vocabFileName,
             std::string tempFileName, std::string embdFile, unsigned long long vocab_size, unsigned long long max_size,
             unsigned long min_count, unsigned long window, unsigned long embed_size, unsigned long epoch,
             unsigned long threshold, int threads, int seed, unsigned long init_epoch, double lr, bool keep_case,
             bool symmetric) {
    this->inputFile = inputFile;
    this->logdir = logdir;
    this->coFileName = coFileName;
    this->vocabFileName = vocabFileName;
    this->tempFileName = tempFileName;
    this->embdFile = embdFile;
    this->vocabFileName = vocabFileName;
    this->vocab_size = vocab_size;
    this->max_size = max_size;
    this->min_count = min_count;
    this->window = window;
    this->embed_size = embed_size;
    this->epoch = epoch;
    this->threshold = threshold;
    this->threads = threads;
    this->seed = seed;
    this->init_epoch = init_epoch;
    this->lr = lr;
    this->keep_case = keep_case;
    this->symmetric = symmetric;
};

Glove::Glove(std::vector<std::string> args_cmd) {
    parseArgs(args_cmd);
    std::cout << "load cmd ..." << std::endl;
};


Glove::Glove() {

};

void Glove::train(string inputFile) {
    this->inputFile = inputFile;

    std::cout << "Building vocabulary..." << std::endl;
    voca = Vocabulary(min_count, max_size, keep_case, inputFile);
//    std::cout << "Vocab size: " << v.size() << std::endl;
    vocab_size = voca.size();

    CoMat builder(vocab_size, threshold, inputFile, coFileName, window, symmetric, memory_limit, logdir, tempFileName);
    builder.build(voca);

//    std::cout << "Training..." << std::endl;
    model = Train(embed_size, vocab_size, threads, init_epoch, epoch, coFileName, lr, logdir, vocabFileName, embdFile);
    model.train();
//    std::cout << "Training down..." << std::endl;

};


AnalogyPairs Glove::most_similary(const std::string &word, unsigned long num) {
    return model.most_similary(word, num, voca);
}

void Glove::load(std::string vocabFile, std::string wordvecFile, std::string metaFile) {

    voca.load(vocabFile);

    vocab_size = voca.atoi.size();
    model = Train(embed_size, vocab_size, threads, init_epoch, epoch, coFileName, lr, logdir, vocabFileName, embdFile);
    model.load_model(wordvecFile, metaFile, voca);

}

void Glove::to_txt() {
//    std::cout << "save wordvec..." << std::endl;
    model.to_txt(voca);
//    std::cout << "save wordvec down..." << std::endl;
}
