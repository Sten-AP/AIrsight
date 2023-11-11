# start by pulling the python image
FROM python:3.12.0-bullseye

WORKDIR /WEkEO/

# copy the requirements file into the image
COPY ./requirements.txt /WEkEO/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install -r /WEkEO/requirements.txt

# copy every content from the local file to the image
COPY . /WEkEO/

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["main.py" ]
