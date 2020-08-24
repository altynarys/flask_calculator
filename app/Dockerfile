FROM python:3-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY calc.py calc.py
CMD python /app/calc.py
