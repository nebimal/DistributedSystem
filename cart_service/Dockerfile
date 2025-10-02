FROM python:3.9-slim

WORKDIR /cart_service

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/cart_service.proto ../proto/common.proto

EXPOSE 50053

CMD ["python", "service.py"]
