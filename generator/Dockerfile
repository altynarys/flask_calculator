FROM python:3-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY generate_events.py generator.py
CMD python /app/generator.py
