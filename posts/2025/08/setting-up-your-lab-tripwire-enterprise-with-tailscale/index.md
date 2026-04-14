---
title: "Setting up your lab Tripwire Enterprise with Tailscale"
date: 2025-08-11
categories: 
  - "tailscale"
tags: 
  - "tripwire"
coverImage: "61563ef3d974215a2.78012139-1365x2048-1.jpg"
---

One of the most common things I need in my lab is access to the web console for Tripwire Enterprise to do demos- but it can be a nuisance to demonstrate with a VM quickly if I'm out on the road... until Tailscale quietly made homelabs easy to remotely setup. Now, I don't even need to replace the default TE certificate, I can quickly deploy a virtual machine and get it up and running on my Tailscale network with a NGINX setup that means I even have a nice, trusted SSL certificate in moments - here's the workflow I use for this on Windows:

# Install tailscale client

After installing TE as usual, you'll want to download and install the Tailscale client and register it: [https://tailscale.com/download/windows](https://tailscale.com/download/windows)

# Get a cert:

Once tailscale is up and running, you'll want a certificate to use for your site:

```
tailscale cert yourmachine.domain.com
```

# Download NGINX

With Tailscale and your certs ready to go, you can setup NGINX - starting with a quick download (https://nginx.org/en/download.html).

Once unzipped, you can then add in your certificates from the previous step to a suitable directory for NGINX to use  
Finally, you'll want to setup NGINX to give access to your TE console - I use port 8443 for access the NGINX site, and, in this example, my TE console host is running on 192.168.1.20 - you'll want to update these to suit your needs (I've also weakened the security requirements here a bit to help support some legacy clients connecting to TE - in the real world I'd advise against this of course!).

```
/etc/nginx/nginx.conf

user nginx; # 'www-data' on Debian/Ubuntu
worker_processes auto;

pid nginx.pid;

events {
worker_connections 1024;
}

http {
include mime.types;
default_type application/octet-stream;

sendfile        on;
tcp_nopush      on;
tcp_nodelay     on;
keepalive_timeout  65;

# --- TLS defaults for the public side (clients -> NGINX) ---
ssl_session_cache   shared:SSL:10m;
ssl_session_timeout 1d;
ssl_protocols       TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers off;

# If you enable OCSP stapling, you need a resolver:
resolver 1.1.1.1 1.0.0.1 valid=300s;
resolver_timeout 5s;

# --- Upstream (your backend that has a self-signed cert and listens on 443) ---
upstream backend_https {
    server 192.168.1.20:443;   # change to your backend IP or hostname
    keepalive 32;
}

# --- Public listener on your custom port, with valid certs ---
server {
    listen 8443 ssl http2;               # custom port
    server_name yourcertificatesubjecthostname;             # change to your hostname

    ssl_certificate     yourcerthere.crt;  # change
    ssl_certificate_key yourcertkeyhere.key;    # change
    #ssl_stapling on;
    #ssl_stapling_verify on;

    # --- Reverse proxy to HTTPS backend (self-signed) ---
    location / {
        proxy_http_version 1.1;

        # Forward client details
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Use SNI when talking to backend (good practice)
        proxy_ssl_server_name on;

        # Quick/easy: don't verify the backend's self-signed cert
        proxy_ssl_verify off;
        proxy_ssl_conf_command CipherString "DEFAULT@SECLEVEL=0";
        proxy_ssl_ciphers ECDHE+AESGCM:ECDHE+CHACHA20:!DHE:!aNULL:!MD5:!3DES;
        proxy_ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;

        # If you prefer verification, comment the line above and use:
        # proxy_ssl_trusted_certificate /etc/nginx/trusted/upstream_ca.pem;  # put backend CA or cert here if you prefer - 
        # proxy_ssl_verify on;
        # proxy_ssl_verify_depth 2;
        # Optionally force a specific SNI name if backend needs it:
        # proxy_ssl_name backend.internal.example;

        proxy_pass https://backend_https;

        # Timeouts/buffers (tweak as needed)
        proxy_connect_timeout 10s;
        proxy_send_timeout    60s;
        proxy_read_timeout    60s;
        proxy_buffering on;
    }
}

}
```

# Finally...

If you run into dh2 errors (not unusual with a default install that hasn't been hardened yet) you'll want to to ensure that the TE console is using a decent, more modern cipher - e.g. add

```
tw.tomcat.ciphers=TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_256_CBC_SHA 
```

to your server.properties, as per https://customers.tripwire.com/customers/article?id=ka44T000000PObeQAG, and restart the console.

5 minutes setup, and you've got a shiny cert, proxied access, and a remote way of accessing your TE lab console
