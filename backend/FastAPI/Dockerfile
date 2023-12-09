# start by pulling the python image
FROM python:3.12.0-bullseye

WORKDIR /FastAPI/

# copy the requirements file into the image
COPY ./requirements.txt /FastAPI/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir --upgrade -r /FastAPI/requirements.txt

# copy every content from the local file to the image
COPY . /FastAPI/

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["main.py" ]
