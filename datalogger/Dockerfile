FROM python:3

WORKDIR /scripts

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .

CMD [ "python3", "pi_reciever.py" ]