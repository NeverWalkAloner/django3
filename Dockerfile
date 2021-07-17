FROM python:3.8
WORKDIR /source
COPY . /source
RUN pip install -r requirements.txt
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
ENTRYPOINT ["./docker-entrypoint.sh"]