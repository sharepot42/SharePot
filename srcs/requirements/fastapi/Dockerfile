FROM python:alpine3.18

COPY tools /tmp/tools

RUN mkdir -p /app \
	&& pip install --no-cache-dir --upgrade -r /tmp/tools/requirements.txt

#WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
