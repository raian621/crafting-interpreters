cmake_minimum_required(VERSION 3.27)

target_sources(
  ${PROJECT_NAME} PRIVATE
  main.c
  chunk.c
  memory.c
  debug.c
  value.c
  vm.c
)