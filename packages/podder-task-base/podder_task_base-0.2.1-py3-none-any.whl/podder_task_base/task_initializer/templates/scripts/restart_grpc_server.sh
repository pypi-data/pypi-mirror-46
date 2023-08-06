#!/usr/bin/env bash

echo "Restart gRPC process..."

stop_grpc_process() {
    PYTHON_PROCESSES=$(ps -ef | grep python | grep -v "grep" | wc -l)
    if [ $PYTHON_PROCESSES -gt 0 ]; then
        ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs kill
        echo "Stopped existing gRPC process."
    fi
}

if [ -f $GRPC_PID_FILE ]; then
    echo "FOUND grpc pid_file. Stop gRPC process..."
    stop_grpc_process
    rm -f $GRPC_PID_FILE
fi

echo "Start gRPC server..."
python api/grpc_server.py
