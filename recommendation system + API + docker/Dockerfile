FROM python:latest

WORKDIR /Users/sunshine/PycharmProjects/pythonProject8/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ .

CMD [ "python", "./test.py" ]