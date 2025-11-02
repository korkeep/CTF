FROM golang:1.22 AS builder

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

WORKDIR /app
COPY ./deploy/ ./

RUN go build -o app



FROM debian:bullseye-slim
ENV PORT=8000


WORKDIR /app

COPY --from=builder /app/app .

COPY ./deploy/flag /flag
RUN chmod 755 /flag

EXPOSE $PORT
CMD ["./app"]