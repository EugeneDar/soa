FROM python:3.8

WORKDIR /app

COPY .. .

# TODO use versions in requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Make port available to the world outside this container
#EXPOSE 5000

CMD [ "python", "./app/main.py" ]
