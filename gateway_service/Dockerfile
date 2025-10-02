FROM python:3.9-slim

WORKDIR /gateway_service

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/gateway_service.proto ../proto/common.proto

EXPOSE 8000

CMD ["python", "service.py"]
