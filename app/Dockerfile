FROM python:3.8

RUN mkdir /usr/src/app/
COPY . /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 8000

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt-get update
CMD ["uvicorn", "main:app", "--reload", "--workers=4", "--host=0.0.0.0", "--port=8000"]