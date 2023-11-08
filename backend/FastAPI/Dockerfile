# start by pulling the python image
FROM python:3.9.2

# copy the requirements file into the image
COPY ./requirements.txt /home/airsight/application/backend/requirements.txt

# switch working directory
WORKDIR /home/airsight/application/backend/FastAPI

# install the dependencies and packages in the requirements file
RUN pip install -r /home/airsight/application/backend/requirements.txt

# copy every content from the local file to the image
COPY . /home/airsight/application/backend/FastAPI

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

EXPOSE 5000

CMD ["fastapi.py" ]
