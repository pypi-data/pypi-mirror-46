cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(pybind11-download NONE)

include(ExternalProject)

ExternalProject_Add(
        pybind11
        SOURCE_DIR "/Users/akhvorov/code/mlimlab/vgram/vgram/cmake-build-debug/binding/src/main/pybind11/pybind11-src"
        BINARY_DIR "/Users/akhvorov/code/mlimlab/vgram/vgram/cmake-build-debug/binding/src/main/pybind11/pybind11-build"
        GIT_REPOSITORY
        https://github.com/pybind/pybind11.git
        GIT_TAG
        v2.2.4
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ""
        INSTALL_COMMAND ""
        TEST_COMMAND ""
)
