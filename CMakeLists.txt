cmake_minimum_required (VERSION 3.17.5...3.19 FATAL_ERROR)

project(FOO VERSION 0.1.0 LANGUAGES CXX C)

find_package(PNG)


add_library(foo SHARED src/foo.cpp)
set_target_properties(foo PROPERTIES PUBLIC_HEADER include/foo.h)
target_include_directories(foo PUBLIC include)
target_link_libraries(foo PUBLIC PNG::PNG)

add_subdirectory(pybind11)
pybind11_add_module(pyfoo src/pyfoo.cpp)
target_link_libraries(pyfoo PRIVATE foo)
