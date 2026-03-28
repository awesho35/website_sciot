FROM nginx:alpine

# Copy all static frontend files into the nginx html root
# Build context is the website root, so we copy the static assets directly
COPY index.html /usr/share/nginx/html/index.html
COPY programmation.html /usr/share/nginx/html/programmation.html
COPY menu.html /usr/share/nginx/html/menu.html
COPY jouerausciot.html /usr/share/nginx/html/jouerausciot.html
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/
COPY ressources/ /usr/share/nginx/html/ressources/

# Serve static files on port 80 (the stack nginx reverse-proxies to this container)
RUN printf 'server {\n    listen 80;\n    server_name _;\n    root /usr/share/nginx/html;\n    index index.html;\n    location / {\n        try_files $uri $uri/ /index.html;\n    }\n}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80
