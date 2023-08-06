cmake_minimum_required(VERSION 3.0.2)
set(project_name vgram)
project(${project_name})

set(CMAKE_CXX_STANDARD 14)
option(WITH_PYTHON "Build with python interface" ON)

set(PYBIND11_CPP_STANDARD -std=c++14)

set(SOURCE_LIB
        ../main/cpp/test.cc
        ../main/cpp/json.h
        ../main/cpp/vgram_builders/py_int_stream_vgram_builder.h
        ../main/cpp/vgram_builders/py_int_stream_vgram_builder.cc
        ../main/cpp/tokenizers/base_tokenizer.h
        ../main/cpp/tokenizers/base_tokenizer.cc
        ../main/cpp/tokenizers/char_tokenizer.h
        ../main/cpp/tokenizers/char_tokenizer.cc
        ../main/cpp/seq_coder.h
        ../main/cpp/seq_coder.cc
        )

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_library(test_cpp STATIC ${SOURCE_LIB})
