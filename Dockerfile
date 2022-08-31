FROM python:3.8-slim
ENV DEBUG_MODE False
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn==20.0.4
COPY vtescards/ /usr/local/app/
WORKDIR /usr/local/app/
CMD sleep 10s && python3 manage.py migrate && gunicorn -w 1 -b 0.0.0.0:8000 vtescards.wsgi