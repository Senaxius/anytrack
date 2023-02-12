FROM osrf/ros:humble-desktop-full

RUN apt-get update && apt-get install -y --no-install-recommends v4l-utils python3-pip ros-humble-turtlesim zsh net-tools ros-humble-rosbridge-suite vim git ros-humble-camera-calibration ros-humble-camera-calibration-parsers ros-humble-camera-info-manager 
RUN pip3 install imutils opencv-python setuptools==58.2.0

ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 ~/.ssh/id_rsa

RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN mkdir /home/ALEX

RUN cd /home/ALEX && git clone git@github.com:Senaxius/dotfiles.git
RUN cd /home/ALEX/dotfiles && ./install.sh -z 1 -v 1 -f 1 -g 1 -o 0 -k 0

RUN chsh -s /bin/zsh
RUN ln -s ~/.rc-temp/ros-setup.sh ~/.rc/ 
RUN rm -rf ~/.zsh_history && cp /home/ALEX/dotfiles/config/.zsh_history ~ && chown root:root ~/.zsh_history

