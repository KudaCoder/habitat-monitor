FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ENV PYTHONPATH $PYTHONPATH:/usr/src/app

COPY . /usr/src/app/
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]