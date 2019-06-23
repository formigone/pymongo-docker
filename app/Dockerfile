FROM python:3.6-alpine

WORKDIR /app

COPY ["start_server.sh", "requirements.txt",  "/app/"]
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY api /app

CMD ["/app/start_server.sh"]
