# Reverse proxy Nginx

The following code is specified in the config file for the Nginx server or server block:

```
server {
    root /var/www/airsight.cloudsin.space/html;
    index index.html;

    server_name airsight.cloudsin.space www.airsight.cloudsin.space;

    location / {
        try_files $uri $uri/ =404;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/airsight.cloudsin.space/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/airsight.cloudsin.space/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    # Reverse Proxy for :3000
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Reverse Proxy for :3002
    location /grafana/ {
        proxy_pass http://localhost:3002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Reverse Proxy for :8086
    location /influxdb/ {
        proxy_pass http://localhost:8086;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Reverse Proxy for :9000
    location /portainer/ {
        proxy_pass http://localhost:9000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    if ($host = airsight.cloudsin.space) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;

    server_name airsight.cloudsin.space www.airsight.cloudsin.space;
    return 404; # managed by Certbot
}
```