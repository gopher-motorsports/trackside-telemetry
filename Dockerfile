FROM library/python:3.9-alpine

WORKDIR /src

RUN apk --no-cache add curl
RUN curl -LJO https://github.com/gopher-motorsports/trackside-telemetry/releases/download/cli/trackside-0.9.1-py3-none-any.whl

CMD [ "pip3", "install", "*.whl" ]

ENTRYPOINT ["trackside"]
