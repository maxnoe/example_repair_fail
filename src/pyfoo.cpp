#include <pybind11/pybind11.h>
#include <png.h>

#include "foo.h"

namespace py = pybind11;


PYBIND11_MODULE(pyfoo, m) {
    m.def("foo", &foo, "Multiply bar by 2.", py::arg("bar"));
    m.attr("png_version") = py::int_(PNG_LIBPNG_VER);
}
