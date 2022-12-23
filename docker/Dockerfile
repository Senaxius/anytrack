FROM osrf/ros:humble-desktop-full

RUN apt-get update && apt-get install -y --no-install-recommends python3-pip ros-humble-turtlesim zsh net-tools ros-humble-rosbridge-suite vim git
RUN pip3 install imutils opencv-python setuptools==58.2.0

ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 ~/.ssh/id_rsa

RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN cd ~ && git clone git@github.com:Senaxius/dotfiles.git
RUN cd ~/dotfiles && ./install.sh
RUN cd ~/dotfiles && ./vim-install.sh
RUN cd ~/dotfiles && ./git-config.sh
RUN chsh -s /bin/zsh
RUN ln -s ~/.rc-temp/ros-setup.sh ~/.rc/ 

RUN mkdir /home/ALEX
