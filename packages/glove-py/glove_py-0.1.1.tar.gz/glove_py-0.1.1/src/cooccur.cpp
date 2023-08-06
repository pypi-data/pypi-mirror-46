#include "cooccur.h"
#include <deque>
#include <fstream>
#include <iostream>
#include <cassert>
#include<algorithm>
#include "utils.h"

//生成共现三元组的主程序
//如果使用二维矩阵储存共现矩阵,则二维矩阵的左上角稠密(高频词共现次数较多),而右下角稀疏(低频词共现次数较少),二维矩阵总体来说太过稀疏
//如果使用三元组(id1,id2,value)来储存,左上角的共现三元组次数又太多,重复更新左上角的三元组效率也太低了
//因此采用混合储存然后合并的方式进行储存,左上角的高频词使用二维数组储存,其余的低频词使用三元组储存,全部语料处理完成后,二维数组转化为三元组,合并高频三元组和低频三元组即得共现矩阵

typedef struct cooccur_rec_id {
    uint32_t i;
    uint32_t j;
    double val;
    int id;
} CRECID;

typedef struct cooccur_rec {
    uint32_t word1;
    uint32_t word2;
    double val;
} CREC;

/* Check if two cooccurrence records are for the same two words */
int compare_crecid(CRECID a, CRECID b) {
    int c;
    if ((c = a.i - b.i) != 0) return c;
    else return a.j - b.j;
}

/* Swap two entries of priority queue */
void swap_entry(vector<CRECID> &pq, int i, int j) {
    CRECID temp = pq[i];
    pq[i] = pq[j];
    pq[j] = temp;
}

/* Insert entry into priority queue */
void insert(vector<CRECID> &pq, CRECID &_new, int size) {
    int j = size - 1, p;
    pq[j] = _new;
    while ((p = (j - 1) / 2) >= 0) {
        if (compare_crecid(pq[p], pq[j]) > 0) {
            swap_entry(pq, p, j);
            j = p;
        } else break;
    }
}

/* Delete entry from priority queue */
void remove(vector<CRECID> &pq, int size) {
    int j, p = 0;
    pq[p] = pq[size - 1];
    while ((j = 2 * p + 1) < size - 1) {
        if (j == size - 2) {
            if (compare_crecid(pq[p], pq[j]) > 0) swap_entry(pq, p, j);
            return;
        } else {
            if (compare_crecid(pq[j], pq[j + 1]) < 0) {
                if (compare_crecid(pq[p], pq[j]) > 0) {
                    swap_entry(pq, p, j);
                    p = j;
                } else return;
            } else {
                if (compare_crecid(pq[p], pq[j + 1]) > 0) {
                    swap_entry(pq, p, j + 1);
                    p = j + 1;
                } else return;
            }
        }
    }
}


/* Write top node of priority queue to file, accumulating duplicate entries */
int merge_write(CRECID _new, CRECID &old, std::ofstream &fout) {
    if (_new.i == old.i && _new.j == old.j) {
        old.val += _new.val;
        return 0; // Indicates duplicate entry
    }
    fout.write((char *) &old, sizeof(CREC));
    old = _new;
    return 1; // Actually wrote to file
}

void CoMat::build(const Vocabulary &vocab) {

    file::open(input, inputFile);
    // Put the first word of the first line into context
    input >> context;

    exists = lookup(center, id, vocab);
    ids.push_back(exists ? id : 0);
    flags.push_back(exists);

    std::ofstream foverflow(logdir + tempFileName + std::to_string(fidCounter));
    while (!input.eof()) {
        if (ind >= 100000) { // If overflow buffer is (almost) full, sort it and write it to temporary file
            std::ofstream foverflow(logdir + tempFileName + std::to_string(fidCounter), std::ios::out | std::ios::binary);
            write_chunk(low_cooccur, foverflow);
            fidCounter++;
            ind = 0;
        }

        input >> center;
        // If this line has only 1 word, skip
        if (center.empty()) {
            continue;
        }
//        此处id在looup时已经被修改过了,id是中心词的词id
        exists = lookup(center, id, vocab);
        if (exists) {
            for (uint32_t i = 0; i != ids.size(); ++i) {
                // If context word is OOV, skip
                if (!flags[i]) {
                    continue;
                }
                double weight = 1.0 / (ids.size() - i);
//                threshold的默认值是 5000* 5000   id是中心词的词序,ids[i]是当前词的词序
//                如果当前词的id比较小,则前一项大,则flag返回true,此时id对应的词的词频也越高
                bool isHigh = (threshold / (id + 1) >= (ids[i] + 1));
//                std::cout << "threshold :" << threshold / (id + 1) << "ids[i] + 1"<<ids[i] + 1<<std::endl;
//                如果为共现次数较多的三元组
                if (isHigh) {
//                    std::cout<<"index: "<<index[id] + ids[i]<<std::endl;
                    bigram_table[index[id] + ids[i]] += weight;
//                如果为共现次数较少的三元组
                } else {
                    low_cooccur.emplace_back(id, ids[i], weight);
                    ind++;
                }

                if (symmetric) {
                    if (isHigh) {
                        bigram_table[index[ids[i]] + id + 1] += weight;
                    } else {
                        low_cooccur.emplace_back(ids[i], id, weight);
                        ind++;
                    }
                }
            }
        }
        sliding_window(vocab, window);
    }

    write_chunk(low_cooccur, foverflow);

    write_high_cooccur(tempFileName, bigram_table);

    merge_files(fidCounter + 1, coFileName, tempFileName);

    return;
}

void CoMat::write_chunk(std::list<CoRec> &co, std::ofstream &out) {
    co.sort();
    while (!co.empty()) {
        CoRec current = std::move(co.front());
        co.pop_front();
        if (current == co.back()) {
            co.back() += current;
        } else {
            out.write((char *) &(current.i), sizeof(uint32_t));
            out.write((char *) &(current.j), sizeof(uint32_t));
            out.write((char *) &(current.weight), sizeof(double));
        }
    }
    co.clear();
    out.close();
}

void CoMat::write_high_cooccur(std::string &tempFileName, std::vector<double> &bigram_table) {
    //如果是共现矩阵左上角高频共现词
    for (uint32_t i = 0; i != vocab_size; ++i) {
        for (uint32_t j = 0; j != index[i + 1] - index[i]; ++j) {
//            std::cout << "bigram_table..." << bigram_table.size() << std::endl;
            double weight = bigram_table[index[i] + j];
            if (weight > 0) {
                high_cooccur.emplace_back(i, j, weight);
            }
        }
    }

    std::cout << "bigram_table  is :" << bigram_table.size() << std::endl;
    std::ofstream out(logdir+tempFileName + std::to_string(fidCounter), std::ios::out | std::ios::binary);
    assert(out);
    for (const CoRec &co:high_cooccur) {
        out.write((char *) &(co.i), sizeof(uint32_t));
        out.write((char *) &(co.j), sizeof(uint32_t));
        out.write((char *) &(co.weight), sizeof(double));
    }
    out.close();
    high_cooccur.clear();
}

void CoMat::merge_files(int num, std::string coFileName, std::string tempFileName) {
    std::cout << "merge.... file nums is :  " << num << std::endl;
    int i, size;
    long long counter = 0;
    CRECID _new, old;
    vector<CRECID> pq(num);
//    std::vector<std::ifstream> fid;
    std::ofstream fout(logdir + coFileName, std::ios::out | std::ios::binary);

    /* Open all files and add first entry of each to priority queue */

    std::ifstream fid[num];
    for (i = 0; i < num; i++) {
        fid[i].open(logdir + tempFileName + std::to_string(i), std::ios::out | std::ios::binary);
    }

    for (i = 0; i < num; i++) {
        fid[i].read((char *) &(_new), sizeof(CREC));
        _new.id = i;
        insert(pq, _new, i + 1);
    }

    /* Pop top node, save it in old to see if the next entry is a duplicate */
    size = num;
    old = pq[0];
    i = pq[0].id;
    remove(pq, size);
    fid[i].read((char *) &(_new), sizeof(CREC));
    if (!(fid[i])) size--;
    else {
        _new.id = i;
        insert(pq, _new, size);
    }

    /* Repeatedly pop top node and fill priority queue until files have reached EOF */
    while (size > 0) {
        counter += merge_write(pq[0], old, fout); // Only count the lines written to file, not duplicates
        i = pq[0].id;
        remove(pq, size);
        fid[i].read((char *) &(_new), sizeof(CREC));
        if (!(fid[i])) size--;
        else {
            _new.id = i;
            insert(pq, _new, size);
        }
    }
    fout.write((char *) &(old), sizeof(CREC));
    std::cout << "down...." << old.i << std::endl;
    for (i = 0; i < num; i++) {
        fid[i].close();
    }
    fout.close();

    std::cout << "merge....down" << std::endl;

    return;
}


CoMat::CoMat(unsigned long long vocab_size, unsigned long long threshold, std::string inputFile,
             std::string coFileName,
             unsigned long long window, bool symmetric
) :
        vocab_size(vocab_size),
        index(vocab_size + 1, 0),
        threshold(threshold),
        inputFile(inputFile),
        coFileName(coFileName),
        window(window),
        symmetric(symmetric) {
    initParas();
    std::cout << " vocab_size " << vocab_size << std::endl;
    std::cout << " index.size() " << index.size() << std::endl;

};

//CoMat::CoMat(unsigned long long vocab_size, unsigned long threshold) : vocab_size(vocab_size),
//                                                                                           index(vocab_size + 1, 0),
//                                                                                           threshold(threshold) {
//    initParas();
//    std::cout << " vocab_size " << vocab_size << std::endl;
//    std::cout << " index.size() " << index.size() << std::endl;
//
//}


bool CoMat::lookup(const std::string &key, unsigned long &id, const Vocabulary &vocab) {
    try {
        id = vocab[key];
    } catch (const std::out_of_range &e) {
        return 0;
    }
    return 1;
};

void CoMat::sliding_window(const Vocabulary &vocab, unsigned long &window) {
    // If line breaks, separate context between paragraphs
    //这一行结束,清空ids和flags,重新读取一个词到ids里面
//        peek函数用于读取并返回下一个字符，但并不移动流指针
    if (input.peek() == '\n') {
        ids.clear();
        flags.clear();
        input >> context;
        exists = lookup(center, id, vocab);
        ids.push_back(exists ? id : 0);
        flags.push_back(exists);
        center = "";
    } else {
        // Remove the oldest history
//            如果超出滑动窗口的上限 window 则移除顶部数据
        if (ids.size() >= window) {
            ids.pop_front();
            flags.pop_front();
        }
        // Current center word becomes history
//            如果没有到换行,也没有达到滑动窗口的上限,则将id压如ids中;
        ids.push_back(id);
        flags.push_back(exists);
    }
}


void CoMat::initParas() {
    std::cout << "index.size(): " << index.size() << std::endl;

    index[0] = 0;
    for (uint32_t i = 1; i != vocab_size + 1; ++i) {
        index[i] = index[i - 1] + std::min(threshold / i, vocab_size);
    }

    bigram_table = std::vector<double>(index[vocab_size], 0);
    std::cout << "bigram_table..." << bigram_table.size() << std::endl;
    return;
};