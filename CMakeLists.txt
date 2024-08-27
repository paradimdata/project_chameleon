cmake_minimum_required(VERSION 3.10)
project(chameleon)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find Boost and HDF5
find_package(Boost REQUIRED)
find_package(HDF5 REQUIRED)

# Define the source files for your project
# Adjust the paths according to your project structure
set(SOURCES
    src/main.cpp
    src/other_source_file.cpp
)

# Add the executable
add_executable(chameleon ${SOURCES})

# Link libraries with consistent style
target_link_libraries(chameleon
    Boost::boost
    HDF5::hdf5
)

# Optionally add include directories
target_include_directories(chameleon PRIVATE ${Boost_INCLUDE_DIRS} ${HDF5_INCLUDE_DIRS})