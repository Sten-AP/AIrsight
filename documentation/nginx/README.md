# Nginx Configuration for Airsight Project

## Overview

This document outlines the Nginx configuration for the Airsight project, focusing on its use as a reverse proxy. The configuration is implemented on a Debian 11 Virtual Machine hosted on Azure. The Airsight project utilizes containerization through Docker Compose for Grafana, the backend, and InfluxDB services. The Docker Compose configuration can be found in the [`docker-compose.yaml`](../../docker-compose.yaml) file.

## Reverse Proxy Setup

For details on the specific configuration of the reverse proxy used in the Airsight project, refer to the [`reverse-proxy.md`](reverse-proxy.md) file in the same directory.

## SSL Certificate Installation

To enhance security, the Nginx server is configured to use SSL certificates. If you need guidance on installing an SSL certificate for the Nginx server, follow the step-by-step instructions provided in the [`secure-nginx-certbot.md`](secure-nginx-certbot.md) file in the same directory.

Feel free to reach out if you have any questions or require further clarification on any aspect of the Nginx configuration for the Airsight project.