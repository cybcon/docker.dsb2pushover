FROM alpine:3.21.0

LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>"
LABEL site.local.program.version="1.0.14"

# LOGLEVEL can be one of debug, info, warning , error
ENV LOGLEVEL info

COPY --chown=root:root /requirements.txt /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       libcurl=8.11.1-r0 \
       python3=3.12.8-r1 \
       py3-beautifulsoup4=4.12.3-r3 \
       py3-curl=7.45.3-r0 \
       py3-numpy=2.1.3-r0 \
       py3-packaging=24.2-r0 \
       py3-pandas=2.2.3-r0 \
       py3-pillow=11.0.0-r0 \
       py3-pip=24.3.1-r0 \
       py3-requests=2.32.3-r0\
    && pip3 install --no-cache-dir --break-system-packages -r /requirements.txt

COPY --chown=root:root /src /

USER 3182:3182

# Start Server
ENTRYPOINT ["python3"]
CMD ["-u", "/app/dsb2pushover.py"]
