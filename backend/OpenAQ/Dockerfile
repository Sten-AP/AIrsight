# start by pulling the python image
FROM python:3.9.2

WORKDIR /home/airsight/application/backend/OpenAQ/

# copy the requirements file into the image
COPY ./requirements.txt /home/airsight/application/backend/OpenAQ/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install -r /home/airsight/application/backend/OpenAQ/requirements.txt

# copy every content from the local file to the image
COPY . /home/airsight/application/backend/OpenAQ/


# Crontab
COPY root /var/spool/cron/crontabs/root 
CMD cron -l 2 -f

# configure the container to run in an executed manner
#ENTRYPOINT [ "python3" ]
#CMD ["main.py" ]
