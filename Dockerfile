FROM library/python:3.9:alpine

WORKDIR /src

COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY /trackside /src

CMD ["python", "reciever.py"]
