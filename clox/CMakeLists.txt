cmake_minimum_required(VERSION 3.27)

project(clox)

include_directories(include)
add_executable(${PROJECT_NAME})
add_subdirectory(src)
