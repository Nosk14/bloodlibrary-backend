FROM python:3.8-slim
ENV DEBUG_MODE False
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn==20.1.0
COPY vtescards/ /usr/local/app/
WORKDIR /usr/local/app/
CMD echo "Waiting to start" && sleep 15 && echo "Starting..." && python3 manage.py migrate && gunicorn -w 1 -b 0.0.0.0:8000 vtescards.wsgi