#ifndef Train_WH_Train_H
#define Train_WH_Train_H

#include <iostream>
#include <thread>
#include <vector>
#include <memory>
#include <random>
#include <stdexcept>
#include <utility>
#include <memory>
#include "vector.h"
#include "args.h"
#include "densematrix.h"
#include "cooccur.h"
#include "vocabulary.h"


using AnalogyPair = std::pair<std::string, double>;
using AnalogyPairs = std::vector<std::pair<std::string, double>>;

class Train {
public:


    Train() = default;

    std::chrono::steady_clock::time_point start_;

    Train(unsigned long embed_size, unsigned long long vocab_size, int threads, unsigned long init_epoch,
          unsigned long epoch, std::string coFileName, double lr);

    void train();


    inline double weighted(double cooccur) const;


    inline double difference(double dotValue, double b1, double b2, double gold) const;

    void to_txt(const Vocabulary &v) const;

    double single_thread(const std::string &coFileName, uint32_t i, double &loss, double lr);

    void threadCount();

    AnalogyPairs most_similary(const std::string &word, unsigned long num, const Vocabulary &vocab);

    std::vector<int> getTop(Vector vec, uint32_t num);

    void load_model(std::string wordvecFile,std::string metaFile, Vocabulary &v);

private:


    uint32_t vocab_size;
    unsigned long embed_size;
    double alpha;
    double threshold;
    std::shared_ptr<DenseMatrix> W1;
    std::shared_ptr<DenseMatrix> W2;
    std::shared_ptr<Vector> b1;
    std::shared_ptr<Vector> b2;
    std::shared_ptr<DenseMatrix> GW1;
    std::shared_ptr<DenseMatrix> GW2;
    std::shared_ptr<Vector> Gb1;
    std::shared_ptr<Vector> Gb2;


    std::vector<int> threadInfo;


    int threads;
    unsigned long init_epoch;
    unsigned long epoch;
    std::string coFileName;
    double lr;

    std::string logdir = "log/";
    std::string vocabFileName = "vocab.txt";
    std::string embdFile = "wordvec.txt";
};


#endif //Train_WH_Train_H
