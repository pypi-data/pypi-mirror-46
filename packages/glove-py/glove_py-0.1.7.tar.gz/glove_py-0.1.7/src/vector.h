/**
 * Copyright (c) 2016-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

#include <cstdint>
#include <ostream>
#include <vector>
#include "matrix.h"
#include "densematrix.h"



class Vector {

public:
    std::vector<double> data_;


    Vector();

    ~Vector();

    Vector(const Vector &) = default;

    Vector(uint32_t dim);

    Vector(Vector &&) noexcept = default;

    Vector &operator=(const Vector &) = default;

    Vector &operator=(Vector &&) = default;

    inline double *data() {
        return data_.data();
    }

    inline const double *data() const {
        return data_.data();
    }

    inline double &operator[](uint32_t i) {
        return data_[i];
    }

    inline const double &operator[](uint32_t i) const {
        return data_[i];
    }

    inline uint32_t size() const {
        return data_.size();
    }

    void zero();

    void mul(double);

    double norm() const;

    void addVector(const Vector &source);

    void addVector(const Vector &, double);

    void addRow(const Matrix &, uint32_t);

    void addRow(const Matrix &, uint32_t, double);

    void mul(const Matrix &, const Vector &);

    uint32_t argmax();

    void mulNum(double x);

    Vector square();

    void add(double a);

    Vector sqrt();

    void div();

    Vector operator+(double a);

    Vector operator/(const Vector &source);

    Vector operator*(const Vector &source);

    Vector operator*(double a);

};

std::ostream &operator<<(std::ostream &, const Vector &);

