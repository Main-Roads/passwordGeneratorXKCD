#FROM nginx:1.19-alpine
FROM nginx:1.21.5-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/version || exit 1