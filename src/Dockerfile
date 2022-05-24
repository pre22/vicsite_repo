FROM python
ARG user=backend
ARG deployment_environment=development
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 DEPLOYMENT_ENVIRONMENT=${deployment_environment}
RUN apt-get upgrade -y && apt-get update && apt-get install -y \
    nano \
    sudo \
    curl \
    libffi-dev \
    libssl-dev \
    sqlite3 \
    libjpeg-dev \
    libopenjp2-7-dev \
    locales \
    cron \
    postgresql-client \
    gettext \
    build-essential \
    python3 \
    python3-dev \
    uwsgi-plugin-python3 \
    uwsgi-plugins-all
RUN useradd -m ${user} && \
    echo "${user}:${user}" | chpasswd && \
    adduser ${user} sudo && \
    pip install --upgrade pip uwsgi
USER ${user}
COPY --chown=${user} . /srv/http/${user}
WORKDIR /srv/http/${user}
RUN pip install -r requirements.txt --no-warn-script-location
CMD uwsgi --emperor uwsgi.ini --env DEPLOYMENT_ENVIRONMENT=${DEPLOYMENT_ENVIRONMENT} --uid ${user} --master
HEALTHCHECK --interval=5s --timeout=5s --retries=3 CMD curl -f http://localhost:8000/home/health/
EXPOSE 8000