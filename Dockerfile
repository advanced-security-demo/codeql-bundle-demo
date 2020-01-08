FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY vAPI.py .
COPY vAPI.db .
EXPOSE 8081
CMD [ "python", "./vAPI.py" ]

