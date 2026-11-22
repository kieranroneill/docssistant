FROM node:24-alpine AS build

WORKDIR /app

RUN corepack enable

COPY package.json pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

COPY ./web ./web

# vite inlines these at build time, so they cannot be changed by the running container
ARG VITE_DESCRIPTION
ARG VITE_LOG_LEVEL=ERROR
ARG VITE_TITLE

RUN pnpm build

FROM nginx:1.29-alpine

COPY ./build/package/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/web/dist /usr/share/nginx/html/app

EXPOSE 8080
