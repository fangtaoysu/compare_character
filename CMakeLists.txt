cmake_minimum_required(VERSION 3.0)
project(compare-character)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(head_dir)

file (
    GLOB MAIN
    "compare_text.cpp"
)

add_executable(executable ${MAIN})