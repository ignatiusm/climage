# ----------------------------------------------------------------------------
# `base` stage.
FROM python:3.10.7-slim-bullseye as base

# Python settings that get copied with "FROM base as xxxx"
ENV PYTHONDONTWRITEBYTECODE=1 \
  VENV_PATH="/app/.venv"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# ----------------------------------------------------------------------------
# `builder` stage is used to build deps + create our virtual environment
FROM base as builder

# Poetry settings
# Poetry puts its virtualenv under .venv (which $VENV_PATH).
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.5.1 \
		POETRY_VIRTUALENVS_IN_PROJECT=true

# Install security updates
RUN export DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get -y clean && \
  rm -rf /var/lib/apt/lists/*

# Install poetry in system. Our code will be in a venv, so no need for isolation.
RUN pip install "poetry==$POETRY_VERSION"

# Copy and cache these files
WORKDIR /app
COPY python/ .

# Install python libraries
RUN poetry install

# ----------------------------------------------------------------------------
# `final` stage. Install extra tools and copy the app + venv across.
# We need the /app folder where we copied imadj, because poetry
# does a "editable" install, pointing the imadj package to the folder.
FROM base as final

# Install security updates, plus tini and mafft
RUN export DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y --no-install-recommends tini && \
  apt-get -y clean && \
  rm -rf /var/lib/apt/lists/*

# Copy in the venv and app we built in the last stage.
COPY --from=builder /app /app

# Ensure we use the venv.
ENV PATH="$VENV_PATH/bin:$PATH"

# When Docker image is stopped, send a SIGINT (KeyboardInterrupt exception by
# default in Python) instead of SIGTERM. Really you should listen for SIGTERM,
# but not all programs do (see https://hynek.me/articles/docker-signals/).
STOPSIGNAL SIGINT

# Let someone else be PID 1
# https://hynek.me/articles/docker-signals/
ENTRYPOINT ["tini", "--"]
