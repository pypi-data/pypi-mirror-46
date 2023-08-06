//
// Created by root on 19-5-15.
//

#include "glove.h"

Glove::Glove() {

};

Glove::Glove(std::vector<std::string> args_cmd) {

    parseArgs(args_cmd);
    std::cout << "load cmd ..." << std::endl;
};

void Glove::train(string inputFile) {
    this->inputFile=inputFile;

    std::cout << "Building vocabulary..." << std::endl;
    voca =Vocabulary(min_count, max_size, keep_case, inputFile);
//    std::cout << "Vocab size: " << v.size() << std::endl;
    vocab_size = voca.size();

    CoMat builder(vocab_size, threshold, inputFile, coFileName, window, symmetric);
    builder.build(voca);

    std::cout << "Training..." << std::endl;
    model = Train(embed_size, vocab_size, threads, init_epoch, epoch, coFileName, lr);
    model.train();
    std::cout << "Training down..." << std::endl;

    std::cout << "save wordvec..." << std::endl;
    model.to_txt(voca);
    std::cout << "save wordvec down..." << std::endl;

};


AnalogyPairs Glove::most_similary(const std::string &word, unsigned long num) {

    return model.most_similary(word,num,voca);
}


void Glove::load(std::string vocabFile,std::string wordvecFile,std::string metaFile) {

    voca.load(vocabFile);

    vocab_size = voca.atoi.size();
    model = Train(embed_size, vocab_size, threads, init_epoch, epoch, coFileName, lr);
    model.load_model(wordvecFile, metaFile,voca);

}



