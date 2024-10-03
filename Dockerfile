FROM python:3.8-slim
ENV DEBUG_MODE False
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn==23.0.0
COPY vtescards/ /usr/local/app/
WORKDIR /usr/local/app/
CMD python3 manage.py migrate && python3 manage.py collectstatic --noinput && gunicorn -w 1 -b 0.0.0.0:8000 vtescards.wsgi:appliction