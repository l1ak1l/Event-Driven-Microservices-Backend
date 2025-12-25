#!/bin/bash

# Function to kill all background processes on exit
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

echo "Starting API Gateway on 8000..."
(cd api-gateway && uv run uvicorn app:app --port 8000 --reload) &

echo "Starting Order Service on 8001..."
(cd services/order-service && uv run uvicorn app:app --port 8001 --reload) &

echo "Starting Inventory Service on 8002..."
(cd services/inventory-service && uv run uvicorn app:app --port 8002 --reload) &

echo "Starting Notification Service on 8003..."
(cd services/notification-service && uv run uvicorn app:app --port 8003 --reload) &

echo "All services started. Logs will appear below."
echo "Press Ctrl+C to stop all services."
wait
