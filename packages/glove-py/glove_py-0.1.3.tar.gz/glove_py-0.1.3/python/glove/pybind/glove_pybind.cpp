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

    m.doc() = "Simple Class";


//    py::class_<Vocabulary>(m, "vocabulary")
//            .def(py::init<unsigned long, unsigned long long, bool, std::string>());
//            .def(py::init<>());

    py::class_<Glove>(m, "glove")
            .def(py::init<>())
            .def("train", [](Glove &m,string inputFile) { m.train(inputFile); });


//    py::class_<Glove>(m, "Glove")
//            .def(py::init<unsigned long, unsigned long long, int, unsigned long, unsigned long, std::string, double>())
//            .def("build", &CoMat::build);

}



