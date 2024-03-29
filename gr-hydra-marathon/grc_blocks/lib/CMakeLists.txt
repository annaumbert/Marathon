# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR} ../../include)
link_directories(${Boost_LIBRARY_DIRS})

list(APPEND hydra_sources
    ../../lib/util/udp.cc
    ../../lib/hydra_fft.cc
    ../../lib/hydra_virtual_radio.cc
    ../../lib/hydra_hypervisor.cc
    ../../lib/hydra_buffer.cc
    ../../lib/hydra_socket.cc
    ../../lib/hydra_stats.cc
    ../../lib/hydra_resource.cc
    ../../lib/hydra_server.cc
    ../../lib/hydra_client.cc
    ../../lib/hydra_core.cc
    ../../lib/hydra_main.cc
    ../../lib/hydra_uhd_interface.cc
    hydra_gr_client_sink_impl.cc
    hydra_gr_client_source_impl.cc
    hydra_gr_server_impl.cc
)

set(hydra_sources "${hydra_sources}" PARENT_SCOPE)
if(NOT hydra_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT hydra_sources)

add_library(gnuradio-hydra STATIC ${hydra_sources})
target_link_libraries(gnuradio-hydra
  ${Boost_LIBRARIES}
  ${GNURADIO_ALL_LIBRARIES}
  ${UHD_LIBRARIES}
  ${OpenCV_LIBRARIES}
  ${OpenCV_LIBRARY}
  ${ZMQ_LIBRARY}
  ${FFTW_LIBRARIES}
  fftw3f
  fftw3l
  gnuradio-zeromq
)
set_target_properties(gnuradio-hydra PROPERTIES DEFINE_SYMBOL "gnuradio_hydra_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-hydra PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
install(TARGETS gnuradio-hydra
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)
