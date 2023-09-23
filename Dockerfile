FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV IS_PRODUCTION=1

CMD ["python", "run.py"]
