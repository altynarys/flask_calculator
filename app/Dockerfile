FROM python:3-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY calc_app.py calc_app.py
CMD python /app/calc_app.py