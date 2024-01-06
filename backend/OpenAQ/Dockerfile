# start by pulling the python image
FROM python:3.12.0-bullseye

WORKDIR /OpenAQ/

# copy the requirements file into the image
COPY ./requirements.txt /OpenAQ/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir --upgrade -r /OpenAQ/requirements.txt

# copy every content from the local file to the image
COPY . /OpenAQ/

CMD ["python3", "-u", "main.py"]

