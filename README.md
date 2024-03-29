Выполнил: Дарашкевич Евгений Михайлович, БПМИ216.

Выбранный вариант: Социальная сеть.

# User service

## Quick start

### How to launch service and database

```
src/services/users/run.sh
```

### Test

You can find some examples of usage in `src/services/users/examples/` directory.

# Post service

## Quick start

### Install protobuf library

For MacOS
```
brew install protobuf
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
export PATH="$PATH:$(go env GOPATH)/bin"
```

### How to launch service and database

```
src/services/posts/run.sh
```

### Test

You can find some examples of usage in `src/services/posts/examples/` directory.
