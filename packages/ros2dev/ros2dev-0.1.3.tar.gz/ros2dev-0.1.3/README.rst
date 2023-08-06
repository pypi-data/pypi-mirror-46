ros2dev
==========================

This project builds a ROS 2.0 development environment in Docker. The user can
then step into the ROS 2.0 environment to perform additional ROS 2.0 actions
(build, rostopic list, etc.).

Basic Setup
-----------

Generate the Dockerfiles to build the base ROS 2.0 environment: ::

  $ ros2dev generate

The generated files are placed in the ``./generated`` directory by
default. Along with the generated ``Dockerfile`` and ``docker-compose.yml``
files is a ``config.json`` file, which contains cached variables from the
``generate`` step.

Build the Docker image for the base ROS 2.0 environment: ::

  $ ros2dev build

Step into the base ROS 2.0 environment: ::

  $ ros2dev env

Run a single command in the ROS 2.0 environment: ::

  $ ros2dev run -c "ros2 topic list"

Install Additional Dependencies
-------------------------------

Since jinja2 is used to generate the Dockerfiles, a developer can extend the
base Dockerfile by overriding the "third_party" block. An example is provided
in this package at: ./src/ros2dev/templates/third_party.example. To generate a
Dockerfile with an override, use the following command: ::

  $ ros2dev generate -o ./src/ros2dev/templates/third_party.example

Then build the docker image: ::

  $ ros2dev build

Build a ROS 2.0 Workspace
-------------------------

To build a ROS 2.0 development environment for a ROS workspace, navigate to the
workspace root directory and run the following command: ::

  $ ros2dev generate -w ./src -o ./third_party.dockerfile

By convention, there should be a ``src`` directory in the root of a ROS
workspace, so we pass the path to the ``src`` directory to the ``-w``
(``--ws_copy_dir``) option. In this example, we are also using the override
option (``-o``) to install additional dependencies before building the ROS
workspace.

Now you can build the docker image for the ROS environment and step into the
ROS environment: ::

  $ ros2dev build
  $ ros2dev env
