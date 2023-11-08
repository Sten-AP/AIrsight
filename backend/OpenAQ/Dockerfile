# start by pulling the python image
FROM python:3.10.12

# copy the requirements file into the image
COPY ./requirements.txt /poab/backend/requirements.txt

# switch working directory
WORKDIR /poab/backend

# install the dependencies and packages in the requirements file
RUN pip install -r /poab/backend/requirements.txt

# copy every content from the local file to the image
COPY . /poab/backend

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

EXPOSE 6000

CMD ["main.py" ]
