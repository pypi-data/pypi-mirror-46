/**
 * Copyright (c) 2016-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include "densematrix.h"

#include <exception>
#include <random>
#include <stdexcept>
#include <utility>
#include <iostream>

#include "vector.h"


DenseMatrix::DenseMatrix() : DenseMatrix(0, 0) {}

DenseMatrix::DenseMatrix(int64_t m, int64_t n) : Matrix(m, n), data_(m * n) {}

DenseMatrix::DenseMatrix(int64_t m, int64_t n, double scale) : Matrix(m, n), data_(m * n) {
    uniform(scale);
}

DenseMatrix::DenseMatrix(DenseMatrix &&other) noexcept
        : Matrix(other.m_, other.n_), data_(std::move(other.data_)) {}

void DenseMatrix::zero() {
    std::fill(data_.begin(), data_.end(), 0.0);
}

void DenseMatrix::uniform(double a) {
    std::random_device r;
    std::mt19937 generator(r());
    std::normal_distribution<double> uniform(0, a);//均值0 方差a
    for (int64_t i = 0; i < (m_ * n_); i++) {
        data_[i] = uniform(generator);
    }
}

void DenseMatrix::multiplyRow(const Vector &nums, int64_t ib, int64_t ie) {
    if (ie == -1) {
        ie = m_;
    }
    assert(ie <= nums.size());
    for (auto i = ib; i < ie; i++) {
        double n = nums[i - ib];
        if (n != 0) {
            for (auto j = 0; j < n_; j++) {
                at(i, j) *= n;
            }
        }
    }
}

void DenseMatrix::divideRow(const Vector &denoms, int64_t ib, int64_t ie) {
    if (ie == -1) {
        ie = m_;
    }
    assert(ie <= denoms.size());
    for (auto i = ib; i < ie; i++) {
        double n = denoms[i - ib];
        if (n != 0) {
            for (auto j = 0; j < n_; j++) {
                at(i, j) /= n;
            }
        }
    }
}

double DenseMatrix::l2NormRow(int64_t i) const {
    auto norm = 0.0;
    for (auto j = 0; j < n_; j++) {
        norm += at(i, j) * at(i, j);
    }
    if (std::isnan(norm)) {
        throw std::runtime_error("Encountered NaN.");
    }
    return std::sqrt(norm);
}

void DenseMatrix::l2NormRow(Vector &norms) const {
    assert(norms.size() == m_);
    for (auto i = 0; i < m_; i++) {
        norms[i] = l2NormRow(i);
    }
}

double DenseMatrix::dotRow(const Vector &vec, int64_t i) const {
    assert(i >= 0);
    assert(i < m_);
    assert(vec.size() == n_);
    double d = 0.0;
    for (int64_t j = 0; j < n_; j++) {
        d += at(i, j) * vec[j];
    }
    if (std::isnan(d)) {
        throw std::runtime_error("Encountered NaN.");
    }
    return d;
}

void DenseMatrix::addVectorToRow(const Vector &vec, int64_t i, double a) {
    assert(i >= 0);
    assert(i < m_);
    assert(vec.size() == n_);
    for (int64_t j = 0; j < n_; j++) {
        data_[i * n_ + j] += a * vec[j];
    }
}

void DenseMatrix::addRowToVector(Vector &x, int32_t i) const {
    assert(i >= 0);
    assert(i < this->size(0));
    assert(x.size() == this->size(1));
    for (int64_t j = 0; j < this->size(1); j++) {
        x[j] += at(i, j);
    }
}

void DenseMatrix::addRowToVector(Vector &x, int32_t i, double a) const {
    assert(i >= 0);
    assert(i < this->size(0));
    assert(x.size() == this->size(1));
    for (int64_t j = 0; j < this->size(1); j++) {
        x[j] += a * at(i, j);
    }
}

void DenseMatrix::addSingleNumToRow(int32_t i, double a) {
    assert(i >= 0);
    assert(i < this->size(0));
    for (int64_t j = 0; j < this->size(1); j++) {
        data_[i * n_ + j] += a;
    }
}

void DenseMatrix::save(std::ostream &out) const {
    out.write((char *) &m_, sizeof(int64_t));
    out.write((char *) &n_, sizeof(int64_t));
    out.write((char *) data_.data(), m_ * n_ * sizeof(double));
}

void DenseMatrix::load(std::istream &in) {
    in.read((char *) &m_, sizeof(int64_t));
    in.read((char *) &n_, sizeof(int64_t));
    data_ = std::vector<double>(m_ * n_);
    in.read((char *) data_.data(), m_ * n_ * sizeof(double));
}

void DenseMatrix::dump(std::ostream &out) const {
    out << m_ << " " << n_ << std::endl;
    for (int64_t i = 0; i < m_; i++) {
        for (int64_t j = 0; j < n_; j++) {
            if (j > 0) {
                out << " ";
            }
            out << at(i, j);
        }
        out << std::endl;
    }
}

double DenseMatrix::dotIds(uint32_t id1, uint32_t id2, DenseMatrix &mat2) const {
    assert(id1 >= 0);
    assert(id2 >= 0);
    double res = 0;
    for (int64_t _n = 0; _n < this->size(1); _n++) {
        res += at(id1, _n) * mat2.at(id2, _n);
    }
    return res;
}

Vector DenseMatrix::getVector(uint32_t id1) const {
    assert(id1 >= 0);
    assert(id1 <= this->size(0));
    Vector res(this->size(1));
    for (int64_t _n = 0; _n < this->size(1); _n++) {
        res[_n] = at(id1, _n);
    }
    return res;
};


void DenseMatrix::toTxt(std::ostream &out) const {
    for (int64_t i = 0; i < m_; i++) {
        for (int64_t j = 0; j < n_; j++) {
            if (j > 0) {
                out << " ";
            }
            out << at(i, j);
        }
        out << std::endl;
    }
}


//矩阵乘上向量转置  MN*N1
Vector DenseMatrix::operator*(Vector &vec) {
    assert(vec.size() == this->size(1));
    Vector res(m_);
    std::cout << "cal..." << std::endl;

    for (int64_t i = 0; i < m_; i++) {
        for (int64_t j = 0; j < n_; j++) {
            res[i] += at(i, j) * vec[j];
        }
    }
    return res;
};

