# start by pulling the python image
FROM python:3.10.12

WORKDIR /OpenAQ/

# copy the requirements file into the image
COPY ./requirements.txt /OpenAQ/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install -r /OpenAQ/requirements.txt

# copy every content from the local file to the image
COPY . /OpenAQ/

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["main.py" ]
