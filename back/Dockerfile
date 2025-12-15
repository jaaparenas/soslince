FROM python:3.12.3-bullseye

ENV PYTHONBUFFERED 1

RUN cp /usr/share/zoneinfo/America/Mexico_City /etc/localtime && \
  echo "America/Mexico_City" >/etc/timezone

WORKDIR /code

COPY requirements.txt /code

RUN pip install --upgrade pip && \
  pip install --trusted-host pypy.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . /code/

RUN python manage.py collectstatic --noinput --clear
