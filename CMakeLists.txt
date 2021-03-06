cmake_minimum_required(VERSION 2.8)

# FIXME: This silences a warning but I'm not sure why its needed.
set(CMAKE_MACOSX_RPATH 1)

project(test_ffig)

if(MSVC)
  add_compile_options("/EHsc")
else()
  add_compile_options("-std=c++14")
endif()

if(NOT WIN32)
  set(CMAKE_CXX_FLAGS_ASAN "-g -fno-omit-frame-pointer -O0 -fsanitize=address")
  set(CMAKE_C_FLAGS_ASAN "-g -fno-omit-frame-pointer -O0 -fsanitize=address")
  set(CMAKE_EXE_LINKER_FLAGS_ASAN "-fsanitize=address")
  set(CMAKE_SHARED_LINKER_FLAGS_ASAN "-fsanitize=address")
endif()

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
include(ffig)

include_directories(externals/catch/include)
include_directories(externals/variant/include)

# Check that the found version of Python==3 on Windows.
# Trust the user if they have supplied their own.
# FIXME: Get to the botton of the libclang/ctypes issues with Python2.
if(NOT PYTHON_EXECUTABLE)
  find_package(PythonInterp REQUIRED)
  if(WIN32)
    execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; assert sys.version_info[0] == 3" RESULT_VARIABLE result OUTPUT_QUIET ERROR_QUIET)
    if(result)
      message(FATAL_ERROR "CMake failed: Python 3 is required for Windows.")
    endif()
  endif()
else()
  execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import this" RESULT_VARIABLE result OUTPUT_QUIET ERROR_QUIET)
  if(result)
    message(FATAL_ERROR "CMake failed: ${PYTHON_EXECUTABLE} cannot execute a simple Python script.")
  endif()
endif()

# Look for Go
execute_process(COMMAND go version RESULT_VARIABLE result OUTPUT_QUIET ERROR_QUIET)
if(result)
  set(Go_FOUND FALSE)
else()
  set(Go_FOUND True)
endif()

# Look for Ruby
find_package(Ruby)

set(all_ffig_bindings "PYTHON;CPP;CPP_MOCKS")
if(Ruby_FOUND)
  list(APPEND all_ffig_bindings "RUBY")
endif()

if(Go_FOUND)
  list(APPEND all_ffig_bindings "GO")
endif()

ffig_add_library(NAME Shape INPUTS tests/input/Shape.h ${all_ffig_bindings})
ffig_add_library(NAME Tree INPUTS tests/input/Tree.h NOEXCEPT PYTHON CPP)
ffig_add_library(NAME Asset INPUTS tests/input/Asset.h PYTHON)
    
add_subdirectory(tests/src)

enable_testing()

add_test(
  NAME test_cppmodel
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_SOURCE_DIR}/tests/cppmodel
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/ffig)

add_test(
  NAME test_python_bindings
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_SOURCE_DIR}/tests
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)
set_property(TEST test_python_bindings PROPERTY LABELS PYTHON)

add_test(
  NAME test_cpp_mocks
  COMMAND ${CMAKE_BINARY_DIR}/tests/src/TestShapeMocks
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)
set_property(TEST test_cpp_mocks PROPERTY LABELS MOCKS)

add_test(
  NAME test_cpp_circle
  COMMAND ${CMAKE_BINARY_DIR}/tests/src/TestCppCircle
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)
set_property(TEST test_cpp_circle PROPERTY LABELS CPP)

add_test(
  NAME test_cpp_tree
  COMMAND ${CMAKE_BINARY_DIR}/tests/src/TestCppTree
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)
set_property(TEST test_cpp_tree PROPERTY LABELS CPP)

if(Ruby_FOUND)
  add_test(
    NAME test_ruby_bindings
    COMMAND ${RUBY_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tests/TestShape.rb ${CMAKE_SOURCE_DIR}/tests/TestShape.rb
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)
  set_property(TEST test_ruby_bindings PROPERTY LABELS RUBY)
endif()

if(Go_FOUND AND NOT WIN32)
  add_subdirectory(tests/go)
endif()
