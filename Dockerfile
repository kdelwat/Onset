FROM node:14 AS frontend
WORKDIR /build
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install
COPY . .
RUN npm run build

FROM tiangolo/uwsgi-nginx-flask:python3.10 AS backend
RUN apt-get update && apt-get install -y gcc
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app /app/app
COPY engine /app/engine
COPY main.py /app/main.py
COPY uwsgi.ini /app/uwsgi.ini
COPY --from=frontend /build/app/templates/index.html /app/app/templates/index.html
COPY --from=frontend /build/app/static /app/app/static
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static
EXPOSE 80
