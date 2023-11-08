#!/bin/bash

sudo docker cp default.conf nginx:/etc/nginx/conf.d/
sudo docker exec nginx nginx -t
sudo docker exec nginx nginx -s reload
