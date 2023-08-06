FROM python:3-slim as base

ARG REQUIREMENTS=test
ENV REQUIREMENTS $REQUIREMENTS
ENV PYTHONUNBUFFERED 1

FROM base as build

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  linux-libc-dev \
  libc6-dev

COPY requirements /requirements
RUN mkdir /wheels
RUN pip wheel -w /wheels -r /requirements/${REQUIREMENTS}.txt

FROM base

COPY --from=build /wheels /wheels
COPY requirements /requirements
RUN pip install --no-index --find-links=/wheels -r /requirements/${REQUIREMENTS}.txt

COPY ./scripts /scripts
RUN chmod +x /scripts/*
RUN find /scripts -type f -print0 | xargs -0 sed -i 's/\r//'

COPY . /app

WORKDIR /app
CMD ["/scripts/dev"]
