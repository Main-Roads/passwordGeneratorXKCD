# Stage 1: Builder stage
FROM python:3.14-alpine AS builder

# Install build dependencies
RUN apk update && apk add --no-cache \
    python3-dev \
    gcc \
    musl-dev

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.14-alpine as runtime

# create directory for the app user
ARG APPUSER=xkcd \
 APPGROUP=xkcd \
 PORT_ARG=5000
 
ARG HOME=/home/$APPUSER
ENV FLASK_APP=project/__init__.py \
 FLASK_ENV=production \
 APP_FOLDER=/home/$APPUSER/web \
 APP_CONFIG=/home/$APPUSER/web/project/config.yaml \
 PATH=/home/$APPUSER/.local/bin:$PATH \
 PORT=$PORT_ARG

EXPOSE ${PORT}/tcp

# Create app user and directories
RUN rm -Rf $HOME && mkdir -p $APP_FOLDER && \
    addgroup -S $APPGROUP && \
    adduser -S -h $HOME -G $APPGROUP $APPUSER && \
    chown -R $APPUSER:$APPGROUP $HOME

WORKDIR $APP_FOLDER

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/$APPUSER/.local

# Copy application files
COPY --chown=$APPUSER:$APPGROUP VERSION $APP_FOLDER/project/
COPY --chown=$APPUSER:$APPGROUP ./config.prod.yaml $APP_CONFIG
COPY --chown=$APPUSER:$APPGROUP ./web/ $APP_FOLDER
COPY --chown=$APPUSER:$APPGROUP ./healthcheck.sh /healthcheck.sh
COPY --chown=$APPUSER:$APPGROUP ./entrypoint.sh /entrypoint.sh

# Make healthcheck script executable
RUN find /*.sh -maxdepth 1 -type f -exec chmod +x {} \;

# change to the app user
USER $APPUSER

HEALTHCHECK --interval=30s --timeout=3s CMD /healthcheck.sh

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]