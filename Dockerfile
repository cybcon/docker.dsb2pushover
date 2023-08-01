FROM alpine:3.18.2

LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>" \
      de.dsb2pushover.version="1.0.9"

# LOGLEVEL can be one of debug, info, warning , error
ENV LOGLEVEL info

COPY --chown=root:root /requirements.txt /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       libcurl=8.2.0-r1 \
       python3=3.11.4-r0 \
       py3-beautifulsoup4=4.12.2-r1 \
       py3-curl=7.45.2-r1 \
       py3-numpy=1.24.4-r0 \
       py3-packaging=23.1-r1 \
       py3-pandas=1.5.3-r1 \
       py3-pillow=9.5.0-r1 \
       py3-pip=23.1.2-r0 \
       py3-requests=2.31.0-r0 \
    && pip3 install --no-cache-dir -r /requirements.txt

COPY --chown=root:root /src /

USER 3182:3182

# Start Server
ENTRYPOINT ["python3"]
CMD ["-u", "/app/dsb2pushover.py"]
