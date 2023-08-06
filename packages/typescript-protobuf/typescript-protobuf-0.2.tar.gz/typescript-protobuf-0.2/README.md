# json-ts-protobuf: Generate Typescript declaration files for JSON objects from protobuf specs

## Requirements
protoc 3.0.0 or greater python 3.5 Other configurations may work.

## Python Implementation
There is currently only a python implementation of the plugin

The plugin can be installed with

    pip install json-ts-protobuf

On posix, ensure that the protoc-gen-json-ts script installed onto your $PATH. Then run.

    protoc --json-ts_out=output/location

Alternately, you can explicitly provide the path:

    protoc --plugin=protoc-gen-json-ts=path/to/protoc-gen-json-ts --json-ts_out=output/location

To suppress output, you can run

    protoc --json-ts_out=quiet:output/location
