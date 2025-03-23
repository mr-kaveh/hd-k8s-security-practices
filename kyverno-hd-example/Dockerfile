# Use Golang as a base for building the binary
# This is a multistage build consists 
# of a Ruilder stage and a Runner Stage

## STAGE 1 : builder
FROM golang:alpine as builder
WORKDIR /app

# Copy source code and build it
COPY hd-main.go .
RUN go build -o app main.go


## STAGE 2 : runner

# Use scratch as the base for the final image
FROM scratch as runner
COPY --from=builder /app/app /app

# Command to run
ENTRYPOINT ["/app"]
