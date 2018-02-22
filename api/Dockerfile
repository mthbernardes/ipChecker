FROM alpine

WORKDIR /opt/SMA-API/
ADD . $WORKDIR
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
        rm -r /usr/lib/python*/ensurepip && \
            pip3 install --upgrade pip setuptools && \
                if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
                        if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
                            rm -r /root/.cache
RUN apk add --no-cache python3-dev build-base linux-headers pcre-dev
RUN pip3 install -r dependencies.txt
EXPOSE 8080
RUN addgroup  www-data && adduser -S -G www-data www-data
CMD uwsgi --http 0.0.0.0:8080 --master --thunder-lock --workers 15 --process 15  --enable-threads --uid www-data --gid www-data --wsgi-file index.py --callable __hug_wsgi__
