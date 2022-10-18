
FROM python:3.10.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /app_grupo2
WORKDIR /app_grupo2
COPY requirements.txt /app_grupo2/
RUN pip install -r requirements.txt
COPY . /app_grupo2/
RUN mkdir -p /app_grupo1/data
RUN python lavaderos_online/manage.py migrate
RUN python lavaderos_online/manage.py rebuild_index --noinput
CMD ["python","lavaderos_online/manage.py","runserver", "0.0.0.0:8000"]