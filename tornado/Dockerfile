FROM python:3.11

EXPOSE 8888
# Install dependencies
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
env PYTHONPATH=/usr/src/app
# Run the application
ENTRYPOINT ["python", "app.py"]