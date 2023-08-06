#!/usr/bin/env bash

echo "Starting process..."

stop_grpc_process() {
    PYTHON_PROCESSES=$(ps -ef | grep python | grep -v "grep" | wc -l)
    if [ $PYTHON_PROCESSES -gt 0 ]; then
        ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs kill
        echo "Stopped existing gRPC process."
    fi
}

stop_tail_process() {
    TAIL_PROCESSES=$(ps -ef | grep tail | grep -v "grep" | wc -l)
    if [ $TAIL_PROCESSES -gt 0 ]; then
        ps -ef | grep tail | grep -v grep | awk '{print $2}' | xargs kill
        echo "Stopped existing tail processes."
    fi
}

if [ -f $GRPC_PID_FILE ]; then
    echo "FOUND gRPC pid file. Stop gRPC process..."
    stop_grpc_process
    rm -f $GRPC_PID_FILE
fi

echo "Start gRPC server..."
python api/grpc_server.py

stop_tail_process

echo "Continue watching gRPC logs..."
tail -f -n 0 $GRPC_LOG & tail -f -n 0 $GRPC_ERROR_LOG
