#ifndef _SRC_COOCCUR_H_
#define _SRC_COOCCUR_H_

#include <list>
#include <memory>
#include <fstream>
#include <deque>
#include "vocabulary.h"
#include "args.h"

struct CoRec {
    uint32_t i;
    uint32_t j;
    double weight;

    CoRec() = delete;

    CoRec(uint32_t i, uint32_t j, double weight) : i(i), j(j), weight(weight) {}

    CoRec(const CoRec &o) : i(o.i), j(o.j), weight(o.weight) {}

    CoRec(CoRec &&o) : i(o.i), j(o.j), weight(o.weight) {}


    CoRec &operator=(const CoRec &x) {
        if (this == &x) {
            return *this;
        }
        i = x.i;
        j = x.j;
        weight = x.weight;
        return *this;
    }

    CoRec &operator+=(const CoRec &x) {
        if (i == x.i && j == x.j) {
            weight += x.weight;
        }
        return *this;
    }

    bool operator==(const CoRec &x) const {
        return i == x.i && j == x.j;
    }

    bool operator!=(const CoRec &x) const {
        return !((*this) == x);
    }

    bool operator<(const CoRec &x) const {
        return i < x.i ? true : (i == x.i && j < x.j);
    }

    bool operator<=(const CoRec &x) const {
        return (*this < x) || (*this == x);
    }
};

using CoRecs = std::list<CoRec>;

class CoMat {
private:
    std::deque<unsigned long> ids;
    std::deque<bool> flags;
    std::string word;
    std::string center;
    std::string context;
    uint32_t vocab_size;
    int threshold;
    bool exists;
    unsigned long id;
    std::list<CoRec> low_cooccur;
    std::ifstream input;
    std::list<CoRec> high_cooccur;

    std::vector<unsigned long> index;
    std::vector<double> bigram_table;//    bigram_table存储高频的共现矩阵，用一维数组模拟二维数组
    int ind = 0;
    int fidCounter = 0;
    int memory_limit;

    std::string tempFileName;
    std::string logdir;

    std::string inputFile;
    std::string coFileName;

    unsigned long window = 10;
    bool symmetric = true;

    long long max_product;
    long long overflow_length;


public:
    CoMat(unsigned long long vocab_size, unsigned long long threshold, std::string inputFile,
          std::string coFileName, unsigned long long window, bool symmetric,int memory_limit,string logdir,std::string tempFileName);

    void write_chunk(std::list<CoRec> &co, std::ofstream &out);

    void merge_files(int fidCounter, std::string cooccurFileName, std::string tempFileName);

    void build(const Vocabulary &vocab);

    bool lookup(const std::string &key, unsigned long &id, const Vocabulary &vocab);

    void sliding_window(const Vocabulary &vocab, unsigned long &window);

    void write_high_cooccur(std::string &tempFileName, std::vector<double> &bigram_table);

    void initParas();

};

#endif /* _SRC_COOCCUR_H_ */
