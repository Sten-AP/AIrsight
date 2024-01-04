# start by pulling the python image
FROM python:3.12.0-bullseye

WORKDIR /FastAPI/

# copy the requirements file into the image
COPY ./requirements.txt /FastAPI/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir --upgrade -r /FastAPI/requirements.txt

# copy every content from the local file to the image
COPY . /FastAPI/
COPY /home/airsight/application/model/saved_models /FastAPI/

CMD ["python3", "-u", "main.py"]
