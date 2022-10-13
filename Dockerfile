FROM python:3.6-alpine

RUN apk --no-cache add curl

RUN apk add build-base linux-headers
RUN python -m pip install psutil

#RUN curl -LJO https://github.com/gopher-motorsports/trackside-telemetry/releases/download/cli/trackside-0.9.1-py3-none-any.whl

RUN mkdir /src

WORKDIR /src

ADD requirements.txt /src/

#CMD [ "pip3", "install", "*.whl" ]

RUN pip install -r requirements.txt

#ENTRYPOINT ["trackside"]
ADD ./trackside /src/

RUN python3 reciever.py
