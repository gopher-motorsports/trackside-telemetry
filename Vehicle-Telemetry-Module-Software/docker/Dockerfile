FROM python:3

WORKDIR /docker

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "src/index.py" ]