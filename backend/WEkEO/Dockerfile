# start by pulling the python image
FROM python:3.12.0-bullseye

WORKDIR /WEkEO/

# copy the requirements file into the image
COPY ./requirements.txt /WEkEO/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir --upgrade -r /WEkEO/requirements.txt

# copy every content from the local file to the image
COPY . /WEkEO/

CMD ["python3", "-u", "main.py"]
