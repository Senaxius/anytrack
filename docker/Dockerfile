FROM osrf/ros:humble-desktop-full

RUN apt-get update && apt-get install -y --no-install-recommends zsh net-tools vim git

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

