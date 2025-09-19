FROM alpine AS builder
ARG V2BX_VERSION=v0.3.8
RUN echo https://github.com/wyx2685/V2bX/releases/download/$V2BX_VERSION/V2bX-linux-64.zip &&\
wget https://github.com/wyx2685/V2bX/releases/download/$V2BX_VERSION/V2bX-linux-64.zip &&\
unzip V2bX-linux-64.zip -d /etc/V2bX

FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --from=builder /etc/V2bX /etc/V2bX
ADD . /app
WORKDIR /app
RUN uv sync
CMD ["/entrypoint.sh"]