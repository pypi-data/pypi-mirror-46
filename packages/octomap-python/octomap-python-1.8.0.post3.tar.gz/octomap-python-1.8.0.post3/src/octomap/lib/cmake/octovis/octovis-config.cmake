# - Config file for the OctoMap package
# (example from http://www.vtk.org/Wiki/CMake/Tutorials/How_to_create_a_ProjectConfig.cmake_file)
# It defines the following variables
#  OCTOVIS_INCLUDE_DIRS - include directories for OctoMap viewer
#  OCTOVIS_LIBRARY_DIRS - library directories for OctoMap viewer 
#  OCTOVIS_LIBRARIES    - libraries to link against
 
set(OCTOVIS_INCLUDE_DIRS "/home/wkentaro/Documents/octomap-python/src/octomap/octovis/src/extern/QGLViewer" "/home/wkentaro/Documents/octomap-python/src/octomap/octovis/include")
set(OCTOVIS_LIBRARY_DIRS "" "/home/wkentaro/Documents/octomap-python/src/octomap/lib")


# Set library names as absolute paths:
set(OCTOVIS_LIBRARIES
  "/home/wkentaro/Documents/octomap-python/src/octomap/octovis/src/extern/QGLViewer/libQGLViewer.so"
  "optimized;/usr/lib/x86_64-linux-gnu/libQtOpenGL.so;debug;/usr/lib/x86_64-linux-gnu/libQtOpenGL.so;optimized;/usr/lib/x86_64-linux-gnu/libQtGui.so;debug;/usr/lib/x86_64-linux-gnu/libQtGui.so;optimized;/usr/lib/x86_64-linux-gnu/libQtXml.so;debug;/usr/lib/x86_64-linux-gnu/libQtXml.so;optimized;/usr/lib/x86_64-linux-gnu/libQtCore.so;debug;/usr/lib/x86_64-linux-gnu/libQtCore.so"
  "/home/wkentaro/Documents/octomap-python/src/octomap/lib/liboctovis.so"
)
