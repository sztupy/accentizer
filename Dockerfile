FROM ubuntu:19.10
RUN apt-get update && \
    apt-get install -y --no-install-recommends libglib2.0-dev gettext ca-certificates git libjpeg-dev libtiff5-dev libpng-dev libfreetype6-dev libgif-dev libxml2-dev libgtk-3-dev libpango1.0-dev libcairo2-dev libspiro-dev libuninameslist-dev python3-dev ninja-build cmake build-essential && \
      #apt-get install -y --no-install-recommends git ca-certificates libuninameslist-dev packaging-dev pkg-config python-dev libglib2.0-dev libxml2-dev libgif-dev libjpeg-dev libtiff-dev build-essential automake flex bison && \
    apt-get clean

WORKDIR /usr/src/app

RUN git clone https://github.com/fontforge/fontforge.git && \
    cd fontforge && \
    #git checkout 20190801 && \
    #./bootstrap && \
    #./configure && \
    #make && \
    #make install && \
    #ldconfig
    git checkout 20200314 && \
    mkdir build && \
    cd build && \
    cmake -GNinja .. && \
    ninja && \
    ninja install

COPY . /usr/src/app

ENTRYPOINT ["fontforge", "accentizer.py"]
