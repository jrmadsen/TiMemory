#
# Project settings
#

################################################################################

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type")
    set(CMAKE_BUILD_TYPE Release)
endif()
string(TOUPPER "${CMAKE_BUILD_TYPE}" _CONFIG)

if(WIN32)
    set(CMAKE_CXX_STANDARD 14 CACHE STRING "C++ STL standard")
else(WIN32)
    set(CMAKE_CXX_STANDARD 11 CACHE STRING "C++ STL standard")
endif(WIN32)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(TIMEMORY_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX} CACHE PATH "TiMemory installation prefix")

add_option(SETUP_PY "Python build from setup.py" OFF NO_FEATURE)
add_option(PYTHON_DEVELOPER_INSTALL "Python developer installation from setup.py" OFF NO_FEATURE)
add_feature(CMAKE_BUILD_TYPE "Build type (Debug, Release, RelWithDebInfo, MinSizeRel)")
add_feature(CMAKE_INSTALL_PREFIX "Installation prefix")
add_feature(CMAKE_CXX_FLAGS "C++ compiler flags")
add_feature(CMAKE_CXX_FLAGS_${_CONFIG} "C++ compiler build type flags")
add_feature(CMAKE_CXX_STANDARD "C++11 STL standard")
add_feature(TIMEMORY_INSTALL_PREFIX "TiMemory installation")

################################################################################
#
#   Non-python installation directories
#
################################################################################

if(PYTHON_DEVELOPER_INSTALL)

    set(TIMEMORY_INSTALL_DATAROOTDIR ${CMAKE_INSTALL_DATAROOTDIR})
    if(NOT IS_ABSOLUTE ${TIMEMORY_INSTALL_DATAROOTDIR})
        set(TIMEMORY_INSTALL_DATAROOTDIR "${TIMEMORY_INSTALL_PREFIX}/share"
            CACHE PATH "Installation root directory for data" FORCE)
    endif()

    set(TIMEMORY_INSTALL_CMAKEDIR ${TIMEMORY_INSTALL_DATAROOTDIR}/cmake/${PROJECT_NAME}
        CACHE PATH "Installation for CMake config" FORCE)
    set(TIMEMORY_INSTALL_INCLUDEDIR ${TIMEMORY_INSTALL_PREFIX}/include
        CACHE PATH "Installation for include directories" FORCE)
    set(TIMEMORY_INSTALL_LIBDIR ${TIMEMORY_INSTALL_PREFIX}/${LIBDIR_DEFAULT}
        CACHE PATH "Installation for libraries" FORCE)
    set(TIMEMORY_INSTALL_BINDIR ${TIMEMORY_INSTALL_PREFIX}/bin
        CACHE PATH "Installation for executables" FORCE)
    set(TIMEMORY_INSTALL_MANDIR ${TIMEMORY_INSTALL_DATAROOTDIR}/man
        CACHE PATH "Installation for executables" FORCE)
    set(TIMEMORY_INSTALL_DOCDIR ${TIMEMORY_INSTALL_DATAROOTDIR}/doc
        CACHE PATH "Installation for executables" FORCE)

else(PYTHON_DEVELOPER_INSTALL)

    # cmake installation folder
    set(TIMEMORY_INSTALL_CMAKEDIR  ${CMAKE_INSTALL_DATAROOTDIR}/cmake/${PROJECT_NAME}
        CACHE PATH "Installation directory for CMake package config files")
    # the rest of the installation folders
    foreach(_TYPE in DATAROOT INCLUDE LIB BIN MAN DOC)
        set(TIMEMORY_INSTALL_${_TYPE}DIR ${CMAKE_INSTALL_${_TYPE}DIR})
    endforeach(_TYPE in DATAROOT INCLUDE LIB BIN MAN DOC)

endif(PYTHON_DEVELOPER_INSTALL)

# create the full path version and generic path versions
foreach(_TYPE in DATAROOT CMAKE INCLUDE LIB BIN MAN DOC)
    # set the absolute versions
    if(NOT IS_ABSOLUTE "${TIMEMORY_INSTALL_${_TYPE}DIR}")
        set(TIMEMORY_INSTALL_FULL_${_TYPE}DIR ${CMAKE_INSTALL_PREFIX}/${TIMEMORY_INSTALL_${_TYPE}DIR})
    else(NOT IS_ABSOLUTE "${TIMEMORY_INSTALL_${_TYPE}DIR}")
        set(TIMEMORY_INSTALL_FULL_${_TYPE}DIR ${TIMEMORY_INSTALL_${_TYPE}DIR})
    endif(NOT IS_ABSOLUTE "${TIMEMORY_INSTALL_${_TYPE}DIR}")

    # generic "PROJECT_INSTALL_" variables (used by documentation)"
    set(PROJECT_INSTALL_${_TYPE}DIR ${TIMEMORY_INSTALL_${TYPE}DIR})
    set(PROJECT_INSTALL_FULL_${_TYPE}DIR ${TIMEMORY_INSTALL_FULL_${TYPE}DIR})

endforeach(_TYPE in DATAROOT CMAKE INCLUDE LIB BIN MAN DOC)

################################################################################
#
#   Python installation directories
#
################################################################################
if(SETUP_PY)
    set(TIMEMORY_INSTALL_PYTHONDIR ${CMAKE_INSTALL_PREFIX}/timemory CACHE PATH
        "Installation prefix of python" FORCE)
else(SETUP_PY)
    set(TIMEMORY_INSTALL_PYTHONDIR
        ${CMAKE_INSTALL_LIBDIR}/python${PYBIND11_PYTHON_VERSION}/site-packages/timemory
        CACHE PATH "Installation directory for python")
endif(SETUP_PY)

set(TIMEMORY_INSTALL_FULL_PYTHONDIR ${CMAKE_INSTALL_PREFIX}/${TIMEMORY_INSTALL_PYTHONDIR})