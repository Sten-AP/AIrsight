# start by pulling the python image
FROM python:3.9.2

WORKDIR /FastAPI/

# copy the requirements file into the image
COPY ./requirements.txt /FastAPI/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install -r /FastAPI/requirements.txt

# copy every content from the local file to the image
COPY . /FastAPI/

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["main.py" ]
