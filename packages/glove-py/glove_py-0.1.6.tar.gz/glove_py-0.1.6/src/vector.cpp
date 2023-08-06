/**
 * Copyright (c) 2016-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include <assert.h>
#include <cmath>
#include <iomanip>
#include <utility>
#include <iostream>
#include "matrix.h"
#include "vector.h"


Vector::Vector(uint32_t m) : data_(m) {}

Vector::Vector() = default;

//    Vector::Vector(const int dim) {
//        data_ = std::vector<double>(dim);
//    };

Vector::~Vector() {
//        std::cout << "Vector 已经被析构" << std::endl;
};

void Vector::zero() {
    std::fill(data_.begin(), data_.end(), 0.0);
}


double Vector::norm() const {
    double sum = 0;
    for (uint32_t i = 0; i < size(); i++) {
        sum += data_[i] * data_[i];
    }
    return std::sqrt(sum);
}

void Vector::mul(double a) {
    for (uint32_t i = 0; i < size(); i++) {
        data_[i] *= a;
    }
}

void Vector::add(double a) {
    for (uint32_t i = 0; i < size(); i++) {
        data_[i] += a;
    }
}

void Vector::addVector(const Vector &source) {
    assert(size() == source.size());
    for (uint32_t i = 0; i < size(); i++) {
        data_[i] += source.data_[i];
    }
}

void Vector::addVector(const Vector &source, double s) {
    assert(size() == source.size());
    for (uint32_t i = 0; i < size(); i++) {
        data_[i] += s * source.data_[i];
    }
}

void Vector::addRow(const Matrix &A, uint32_t i, double a) {
    assert(i >= 0);
    assert(i < A.size(0));
    assert(size() == A.size(1));
    A.addRowToVector(*this, i, a);
}

void Vector::addRow(const Matrix &A, uint32_t i) {
    assert(i >= 0);
    assert(i < A.size(0));
    assert(size() == A.size(1));
    A.addRowToVector(*this, i);
}

void Vector::mul(const Matrix &A, const Vector &vec) {
    assert(A.size(0) == size());
    assert(A.size(1) == vec.size());
    for (uint32_t i = 0; i < size(); i++) {
        data_[i] = A.dotRow(vec, i);
    }
}

void Vector::mulNum(double x) {
    for (uint32_t i = 0; i < size(); i++) {
        data_[i] *= x;
    }
}

uint32_t Vector::argmax() {
    double max = data_[0];
    uint32_t argmax = 0;
    for (uint32_t i = 1; i < size(); i++) {
        if (data_[i] > max) {
            max = data_[i];
            argmax = i;
        }
    }
    return argmax;
}


Vector Vector::sqrt() {
    for (uint32_t i = 0; i < size(); i++) {
        data_[i] = std::sqrt(data_[i]);
    }
    return *this;
}

void Vector::div() {
    for (uint32_t i = 0; i < size(); i++) {
        data_[i] = std::sqrt(data_[i]);
    }

}


Vector Vector::square() {
    Vector res(size());
    for (uint32_t i = 0; i < size(); i++) {
        res[i] = std::pow(data_[i], 2);
    }
    return res;
}

std::ostream &operator<<(std::ostream &os, const Vector &v) {
    os << std::setprecision(5);
    for (uint32_t j = 0; j < v.size(); j++) {
        os << v[j] << ' ';
    }
    return os;
}


Vector Vector::operator+(double a) {
    Vector vec = *this;
    for (uint32_t i = 0; i < size(); i++) {
        vec[i] += a;
    }
    return vec;
}


Vector Vector::operator/(const Vector &source) {
    Vector vec = *this;
    for (uint32_t i = 0; i < size(); i++) {
        vec[i] = data_[i] / source[i];
    }
    return vec;
}


Vector Vector::operator*(const Vector &source) {
    Vector vec = *this;
    for (uint32_t i = 0; i < size(); i++) {
        vec[i] = data_[i] * source[i];
    }
    return vec;
}


Vector Vector::operator*(double a) {
    Vector vec = *this;
    for (uint32_t i = 0; i < size(); i++) {
        vec[i] = data_[i] * a;
    }
    return vec;
}


