FROM registry.access.redhat.com/ubi9/nginx-122:latest

COPY nginx.conf /opt/app-root/etc/nginx.default.d/default.conf
COPY public /opt/app-root/src

EXPOSE 8080
