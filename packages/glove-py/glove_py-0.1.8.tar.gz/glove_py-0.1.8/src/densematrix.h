/**
 * Copyright (c) 2016-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#ifndef DENSEMATRIX_H
#define DENSEMATRIX_H

#include <cstdint>
#include <istream>
#include <ostream>
#include <vector>
#include <assert.h>
#include "matrix.h"

class Vector;

class DenseMatrix : public Matrix {
protected:
    std::vector<double> data_;

public:
    DenseMatrix();

    explicit DenseMatrix(int64_t, int64_t);

    DenseMatrix(int64_t m, int64_t n, double scale);

    DenseMatrix(const DenseMatrix &) = default;

    DenseMatrix(DenseMatrix &&) noexcept;

    DenseMatrix &operator=(const DenseMatrix &) = delete;

    DenseMatrix &operator=(DenseMatrix &&) = delete;

//        virtual ~DenseMatrix() noexcept override = default;

    inline double *data() {
        return data_.data();
    }

    inline const double *data() const {
        return data_.data();
    }

    inline const double &at(int64_t i, int64_t j) const {
        assert(i * n_ + j < data_.size());
        return data_[i * n_ + j];
    };

    inline double &at(int64_t i, int64_t j) {
        return data_[i * n_ + j];
    };

    inline int64_t rows() const {
        return m_;
    }

    inline int64_t cols() const {
        return n_;
    }

    void zero();

    void uniform(double);

    void multiplyRow(const Vector &nums, int64_t ib = 0, int64_t ie = -1);

    void divideRow(const Vector &denoms, int64_t ib = 0, int64_t ie = -1);

    double l2NormRow(int64_t i) const;

    void l2NormRow(Vector &norms) const;

    double dotRow(const Vector &, int64_t) const override;

    void addVectorToRow(const Vector &, int64_t, double) override;

    void addRowToVector(Vector &x, int32_t i) const override;

    void addRowToVector(Vector &x, int32_t i, double a) const override;

    double dotIds(uint32_t id1, uint32_t id2, DenseMatrix &mat2) const;

    void save(std::ostream &) const override;

    void load(std::istream &) override;

    void dump(std::ostream &) const override;

    Vector getVector(uint32_t i) const;

    void addSingleNumToRow(int32_t i, double a);

    void toTxt(std::ostream &out) const;

    Vector operator*(Vector &vec);


    inline double &operator[](uint32_t i) {
        return data_[i];
    }

};


#endif
