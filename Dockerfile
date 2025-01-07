FROM apache/airflow:2.10.2

WORKDIR /opt/airflow

COPY requirements.txt requirements.txt

USER root
# Install OpenJDK-17
RUN apt update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-arm64
RUN export JAVA_HOME

USER airflow

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
