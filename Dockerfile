FROM ubuntu:jammy
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends git ffmpeg python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /app/
WORKDIR /app/
RUN python3 -m pip install -U https://github.com/coletdjnz/yt-dlp-youtube-oauth2/archive/refs/heads/master.zip
RUN echo "--username oauth2 --password ''" > /etc/yt-dlp.conf
RUN pip3 install --no-cache-dir --upgrade --requirement Installer
RUN yt-dlp https://youtube.com/shorts/KNu5Kn6keyw
CMD python3 -m AdityaHalder
