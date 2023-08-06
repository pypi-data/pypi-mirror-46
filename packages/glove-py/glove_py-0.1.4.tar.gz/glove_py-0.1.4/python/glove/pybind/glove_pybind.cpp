#include<iostream>
#include<vector>
#include<string>
#include<memory>
#include<pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <Python.h>
#include "train.h"
#include "glove.h"
//#include "utils.h"

namespace py = pybind11;

PYBIND11_MODULE(glove_pybind, m) {

//    py::class_<Vocabulary>(m, "vocabulary")
//            .def(py::init<unsigned long, unsigned long long, bool, std::string>());
//            .def(py::init<>());

    py::class_<Glove>(m, "glove")
            .def(py::init<>())
            .def(py::init<std::string, std::string, std::string, std::string, std::string, std::string, unsigned long long, unsigned long long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, int, int, unsigned long, double, bool, bool>())
            .def("train", [](Glove &m, string inputFile) { m.train(inputFile); })
            .def("most_similary", [](Glove &m, string word, int num) {
                return m.most_similary(word, num);
            })
            .def("load", [](Glove &m, std::string vocabFile, std::string wordvecFile, std::string metaFilel) {
                m.load(vocabFile, wordvecFile, metaFilel);
            });


//    py::class_<Glove>(m, "Glove")
//            .def(py::init<unsigned long, unsigned long long, int, unsigned long, unsigned long, std::string, double>())
//            .def("build", &CoMat::build);

}



