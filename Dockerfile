FROM ubuntu:19.10
RUN apt-get update && \
    apt-get install -y --no-install-recommends ruby ruby-dev bundler libglib2.0-dev gettext ca-certificates git libjpeg-dev libtiff5-dev libpng-dev libfreetype6-dev libgif-dev libxml2-dev libgtk-3-dev libpango1.0-dev libcairo2-dev libspiro-dev libuninameslist-dev python3-dev ninja-build cmake build-essential && \
    apt-get clean

WORKDIR /usr/src/app

RUN git clone https://github.com/fontforge/fontforge.git && \
    cd fontforge && \
    git checkout 20200314 && \
    mkdir build && \
    cd build && \
    cmake -GNinja .. && \
    ninja && \
    ninja install

COPY . /usr/src/app

RUN cd server && bundle install

EXPOSE 8080

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

CMD ["server"]
