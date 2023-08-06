FROM ubuntu:bionic as builder

MAINTAINER Kevin DeMarco
ENV DEBIAN_FRONTEND noninteractive
SHELL ["/bin/bash", "-c"]

# setup timezone
RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime

RUN apt-get update && apt-get install -q -y \
    curl \
    gnupg2 \
    lsb-release \
    locales \
    python3-argcomplete \
    sudo \
    libboost-system-dev \
    libboost-filesystem-dev \
    && rm -rf /var/lib/apt/lists/*

# setup LOCAL
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN locale-gen en_US en_US.UTF-8 && \
    update-locale

# Setup ros apt sources
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116
RUN echo "deb http://packages.ros.org/ros2/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros2-latest.list

# Install ROS 2.0
ENV CHOOSE_ROS_DISTRO crystal
RUN apt-get update && apt-get install -q -y \
    ros-$CHOOSE_ROS_DISTRO-ros-base \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Create a simple entry script:
ENV ROS_ROOT /opt/ros/crystal
ENV ENTRYPOINT_SCRIPT /usr/local/bin/ros2-entrypoint.sh
RUN echo '#!/bin/bash' > ${ENTRYPOINT_SCRIPT} && \
    echo "source ${ROS_ROOT}/setup.bash" >> ${ENTRYPOINT_SCRIPT} && \
    echo 'source /home/{{ data.user_name }}/.bashrc' >> ${ENTRYPOINT_SCRIPT} && \
    echo 'exec "$@"' >> ${ENTRYPOINT_SCRIPT} && \
    chmod +x ${ENTRYPOINT_SCRIPT}

# Create user, allow sudo without password
RUN adduser --uid {{ data.USER_ID }} --disabled-password --gecos '' {{ data.user_name }} \
    && adduser {{ data.user_name }} sudo \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
    && usermod -a -G video {{ data.user_name }}

{% block third_party %}
# This can be overwritten by third-party projects
{% endblock %}

USER {{ data.user_name }}
RUN echo "source /opt/ros/crystal/setup.bash" >> ~/.bashrc

# Create ros workspace
ENV ROS2_WS /home/{{ data.user_name }}/ros2_ws
RUN mkdir -p ${ROS2_WS}
WORKDIR ${ROS2_WS}

{% if data.ws_copy_dir is not none %}
{% include 'workspace_copy_dir' %}
{% endif %}

ENTRYPOINT ["ros2-entrypoint.sh"]
CMD ["bash"]
