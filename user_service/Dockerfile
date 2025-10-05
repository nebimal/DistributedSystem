FROM python:3.9-slim

WORKDIR /user_service

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY *.proto ./

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. *.proto

EXPOSE 50051

CMD ["python", "user_server.py"]
