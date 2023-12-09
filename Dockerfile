FROM alpine:3.19.0

LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>"
LABEL site.local.program.version="1.0.13"

# LOGLEVEL can be one of debug, info, warning , error
ENV LOGLEVEL info

COPY --chown=root:root /requirements.txt /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       libcurl=8.5.0-r0 \
       python3=3.11.6-r1 \
       py3-beautifulsoup4=4.12.2-r1 \
       py3-curl=7.45.2-r1 \
       py3-numpy=1.25.2-r0 \
       py3-packaging=23.2-r0 \
       py3-pandas=2.0.3-r0 \
       py3-pillow=10.1.0-r1 \
       py3-pip=23.3.1-r0 \
       py3-requests=2.31.0-r1 \
    && pip3 install --no-cache-dir --break-system-packages -r /requirements.txt

COPY --chown=root:root /src /

USER 3182:3182

# Start Server
ENTRYPOINT ["python3"]
CMD ["-u", "/app/dsb2pushover.py"]
