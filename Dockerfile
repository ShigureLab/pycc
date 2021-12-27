FROM ubuntu:20.04
LABEL maintainer="siguremo" \
      version="0.1" \
      description="ubuntu 20.04 with tools for pycc"

# Install deps
RUN set -x \
    && apt update \
    && apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt install -y curl python3.10-dev python3.10-venv clang-10 make \
    && rm -rf /var/lib/apt/lists/* \

    # Add some alias using hard link
    && ln /usr/bin/clang-10 /usr/bin/clang \
    && ln /usr/bin/clang++-10 /usr/bin/clang++ \
    && rm /usr/bin/python3 || true \
    && rm /usr/bin/python || true \
    && ln /usr/bin/python3.10 /usr/bin/python3 \
    && ln /usr/bin/python3.10 /usr/bin/python

# Install poetry
RUN set -x \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && echo 'export PATH=/root/.local/bin:$PATH' >> ~/.bashrc \

    # Set python build tools to clang++
    && echo 'export CC=/usr/bin/clang++' >> ~/.bashrc

# Start the container from bash
CMD [ "/bin/bash" ]
