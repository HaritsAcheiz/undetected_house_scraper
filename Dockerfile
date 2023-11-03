FROM apache/airflow:slim-latest-python3.11
USER root
COPY requirements.txt /opt/airflow
COPY dags/includes /opt/airflow/dags
RUN chmod 777 /opt/airflow
RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev libasound2
RUN wget -c https://ftp.mozilla.org/pub/firefox/releases/119.0/linux-x86_64/en-US/firefox-119.0.tar.bz2 -O firefox.tar.bz2
RUN tar -xvjf firefox.tar.bz2 -C /opt/
RUN ln -s /opt/firefox/firefox /usr/bin/
RUN rm firefox.tar.bz2
RUN apt install -y xvfb
USER airflow
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /opt/airflow/requirements.txt