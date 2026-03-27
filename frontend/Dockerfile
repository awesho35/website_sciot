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

# Remove default nginx config; the main reverse-proxy nginx provides the routing
RUN rm /etc/nginx/conf.d/default.conf 2>/dev/null || true

EXPOSE 80
