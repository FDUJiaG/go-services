FROM golang:1.13-alpine3.10 AS builder
ARG VERSION
RUN apk update
RUN apk add gcc musl-dev \
    && mkdir /app
WORKDIR /app
COPY . /app
RUN CGO_ENABLED=1 GOOS=linux go build -o APP_46ea591951824d8e9376b0f98fe4d48a -a -ldflags "-w -s -X PROJECT_46ea591951824d8e9376b0f98fe4d48a/pkg/server/version.Version=${VERSION}" ./cmd/APP_46ea591951824d8e9376b0f98fe4d48a

FROM alpine:3.10
ARG REPO_URL
ARG BRANCH
ARG COMMIT_REF
LABEL repo-url=${REPO_URL}
LABEL branch=${BRANCH}
LABEL commit-ref=${COMMIT_REF}
RUN apk update \
    && apk add --no-cache \
    ca-certificates \
    && update-ca-certificates 2>/dev/null || true \
    && mkdir /app
WORKDIR /app
COPY --from=builder /app/APP_46ea591951824d8e9376b0f98fe4d48a /app/APP_46ea591951824d8e9376b0f98fe4d48a
EXPOSE 8080
VOLUME [ "/app/data" ]
