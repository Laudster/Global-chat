FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install flask
RUN pip install flask_socketio
RUN pip install requests
RUN pip install python-dotenv


EXPOSE 5000

CMD ["python", "app.py"]