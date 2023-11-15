# Securing Nginx with Let's Encrypt on Linux using Certbot

## 1. Installing Nginx

```bash
sudo apt update
```

Check the version of `nginx` to be installed:

```bash
apt policy nginx
```

Install `nginx`:

```bash
sudo apt install nginx
```

Start and enable `nginx`:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

Check `nginx` status:

```bash
sudo systemctl status nginx
```

> Note: If you encounter the error "Can't open PID file /run/nginx.pid (yet?) after start: Operation not permitted," proceed to the next steps.

## 2. Nginx Server Block Setup

Check the main `nginx` configuration:

```bash
cat /etc/nginx/nginx.conf
```

Check the default `nginx` configuration:

```bash
cat /etc/nginx/conf.d/default.conf
```

Create a folder for the website:

```bash
sudo mkdir -p /var/www/airsight.cloudsin.space/html
```

Update ownership:

```bash
sudo chown -R $USER:$USER /var/www/airsight.cloudsin.space/html
```

Update permissions:

```bash
sudo chmod -R 755 /var/www/airsight.cloudsin.space
```

Create a simple web page:

```bash
vi /var/www/airsight.cloudsin.space/html/index.html
```

```html
<html>
    <head>
        <title>Welcome to airsight.cloudsin.space!</title>
    </head>
    <body>
        <h1>Success! The airsight.cloudsin.space server block is working!</h1>
    </body>
</html>
```

Create necessary directories:

```bash
sudo mkdir /etc/nginx/sites-available/
sudo mkdir /etc/nginx/sites-enabled
```

Create an `nginx` server block:

```bash
sudo vi /etc/nginx/sites-available/airsight.cloudsin.space
```

```conf
# ... (See the provided configuration)
```

Add an include statement to `/etc/nginx/nginx.conf`:

```bash
sudo vi /etc/nginx/nginx.conf
```

```
include /etc/nginx/sites-enabled/*;
```

Create a symlink:

```bash
sudo ln -s /etc/nginx/sites-available/airsight.cloudsin.space /etc/nginx/sites-enabled/
```

Test `nginx` configuration:

```bash
sudo nginx -t
```

Reload `nginx` configuration:

```bash
sudo nginx -s reload
```

Create A records and check DNS:

```bash
dig airsight.cloudsin.space
dig www.airsight.cloudsin.space
```

## 3. Install Certbot

Go to the official Certbot [page](https://certbot.eff.org/instructions) for detailed instructions.

```bash
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

Check Certbot version:

```bash
sudo certbot --version
```

## 4. Secure Nginx with Let's Encrypt

Test Certbot:

```bash
sudo certbot --nginx --test-cert
```

Open the Nginx block:

```bash
cat /etc/nginx/sites-available/airsight.cloudsin.space
```

Go to the browser at https://airsight.cloudsin.space to test the setup.

Issue a real certificate:

```bash
sudo certbot --nginx
```

Test certificate renewal:

```bash
sudo certbot renew --dry-run
```

Check systemctl timers:

```bash
systemctl list-timers
```

## 5. Useful Links

- [Nginx Download](http://nginx.org/en/download.html)
- [Nginx Installation](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)
- [Sites-Available/Sites-Enabled Not Here?](https://www.digitalocean.com/community/questions/sites-available-sites-enabled-not-here)
- [Certbot](https://certbot.eff.org/lets-encrypt/)
- [Installing Snap on Ubuntu](https://snapcraft.io/docs/)