FROM python:3-alpine
WORKDIR /app
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app/calc.py calc.py
CMD python /app/calc.py
