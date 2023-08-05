from python:2

WORKDIR /usr/src/app
COPY . .
RUN mkdir /etc/pacifica-archiveinterface
COPY server.conf /etc/pacifica-archiveinterface/cpconfig.ini
COPY tests/config.cfg /etc/pacifica-archiveinterface/config.ini
ENV ARCHIVEINTERFACE_CONFIG /etc/pacifica-archiveinterface/config.ini
ENV ARCHIVEINTERFACE_CPCONFIG /etc/pacifica-archiveinterface/cpconfig.ini
RUN pip install --no-cache-dir . uwsgi
ENV PAI_BACKEND_TYPE posix
ENV PACIFICA_AAPI_ADDRESS 0.0.0.0
ENV PACIFICA_AAPI_PORT 8080
ENV PAI_PREFIX /srv
RUN chown daemon:daemon /srv
USER daemon
WORKDIR /
ENTRYPOINT [ "/bin/bash", "/usr/src/app/entrypoint.sh" ]
