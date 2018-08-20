FROM revolutionsystems/python:3.6.3-wee-optimized-lto
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt