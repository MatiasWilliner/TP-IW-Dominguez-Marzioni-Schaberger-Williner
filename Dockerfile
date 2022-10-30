FROM python:3.10.6
ENV PYTHONUNBUFFERED 1
ENV DOCKER=True
RUN mkdir /app_grupo2
RUN mkdir /data
WORKDIR /app_grupo2
COPY requirements.txt /app_grupo2/
RUN pip install -r requirements.txt
COPY . /app_grupo2/
RUN python lavaderos_online/manage.py makemigrations
RUN python lavaderos_online/manage.py migrate
RUN python lavaderos_online/manage.py rebuild_index --noinput

#CMD ["python","lavaderos_online/manage.py","makemigrations"]
#CMD ["python","lavaderos_online/manage.py","migrate"]
#CMD ["python","lavaderos_online/manage.py","runserver", "0.0.0.0:8000"]
CMD python lavaderos_online/manage.py makemigrations;python lavaderos_online/manage.py migrate;python lavaderos_online/manage.py runserver 0.0.0.0:8000