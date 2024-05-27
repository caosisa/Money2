# Python 3.9-slim-buster 이미지를 베이스로 사용합니다.
FROM python:3.9-slim-buster

# Java JDK 17을 설치합니다.
RUN apt-get update && apt-get install -y openjdk-17-jdk

# Python이 .pyc 파일을 생성하지 않도록 하고, stdout과 stderr가 버퍼링되지 않도록 설정합니다.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# UID와 GID를 매개변수로 받아 사용자와 그룹을 생성합니다.
ARG UID=1000
ARG GID=1000

# 패키지 목록 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    python3-pip \
    && groupadd -g "${GID}" python \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리를 /home/python으로 설정합니다.
WORKDIR /home/python

# requirements.txt 파일을 복사하고 종속성을 설치합니다.
COPY --chown=python:python requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# pip 패키지 설치 이후에 USER 변경 명령을 실행합니다.
USER python:python

# Python 사용자 환경의 경로를 PATH에 추가합니다.
ENV PATH="/home/${USER}/.local/bin:${PATH}"

# 모든 소스 코드를 작업 디렉토리로 복사합니다.
COPY --chown=python:python . .

# FLASK_ENV 매개변수를 받아 환경 변수로 설정합니다.
ARG FLASK_ENV
ENV FLASK_ENV=${FLASK_ENV}

# 컨테이너가 5000번 포트를 노출하도록 설정합니다.
EXPOSE 5000

# Gunicorn을 사용하여 애플리케이션을 실행합니다.
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
