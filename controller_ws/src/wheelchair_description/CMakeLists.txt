cmake_minimum_required(VERSION 3.5)
project(wheelchair_description)
find_package(ament_cmake REQUIRED)




# Install launch files.
install(DIRECTORY
  launch config meshes urdf src
  DESTINATION share/${PROJECT_NAME}/
)
ament_package()
