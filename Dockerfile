# Base image as Fedora
FROM fedora:33

LABEL maintainer="t.xheva@gmail.com"

###################### BEGIN INSTALLATION #########################

######################### Set up environment ######################
RUN sudo dnf update -y
RUN sudo dnf groupinstall -y "Development Tools" "Development Libraries"
RUN sudo dnf install -y nasm \
                        libtool \
                        autoconf \
                        automake \
                        cmake \
                        git-core \
                        libass-devel \
                        libva-devel \
                        libvdpau-devel \
                        libvorbis-devel \
                        meson \
                        ninja-build \
                        pkg-config \
                        texinfo \
                        wget \
                        yasm \
                        curl \
                        unzip \
                        bzip2
RUN sudo pip install ropgadget

# Install the ffmpeg library for lavf support
RUN sudo dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
RUN sudo dnf -y install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
RUN sudo dnf -y install ffmpeg
RUN sudo dnf -y install ffmpeg-devel
RUN whereis ffmpeg

# Install the ffms2 library for ffms support
WORKDIR /usr/lib/
RUN git clone -b 2.23 https://github.com/FFMS/ffms2.git
RUN cd ffms2
WORKDIR /usr/lib/ffms2
RUN ./configure
RUN make install

# Install the lsmash library for mp4 support
WORKDIR /usr/lib
RUN git clone https://github.com/l-smash/l-smash
RUN cd l-smash
WORKDIR /usr/lib/l-smash
RUN ./configure
RUN make install


# Add local files to the image then compile the x264
WORKDIR /usr/apps/x264
ADD . .
#RUN ./configure
#RUN make

# Run the scripts to calculate the binary size 
# depending from the compil-time options
CMD ["python3", "./measures/exe_size.py"]

# Run a container from the build image to show the results
#CMD ["cat", "/x264/measures/exesize.txt"]
