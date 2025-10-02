import grpc
from concurrent import futures
import uuid
import hashlib
import time
from datetime import datetime

import user_service_pb2
import user_service_pb2_grpc
import common_pb2

class UserService(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {}
        self.user_credentials = {}

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def RegisterUser(self, request, context):
        user_id = str(uuid.uuid4())
        
        if request.username in self.user_credentials:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Username already exists")
            return user_service_pb2.UserResponse()
        
        user_data = {
            'user_id': user_id,
            'username': request.username,
            'email': request.email,
            'first_name': request.first_name,
            'last_name': request.last_name,
            'phone': request.phone,
            'address': request.address,
            'created_at': datetime.now().isoformat()
        }
        
        self.users[user_id] = user_data
        self.user_credentials[request.username] = {
            'user_id': user_id,
            'password_hash': self._hash_password(request.password)
        }
        
        return user_service_pb2.UserResponse(**user_data)

    def GetUser(self, request, context):
        if request.user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_service_pb2.UserResponse()
        
        return user_service_pb2.UserResponse(**self.users[request.user_id])

    def AuthenticateUser(self, request, context):
        if (request.username not in self.user_credentials or 
            self.user_credentials[request.username]['password_hash'] != self._hash_password(request.password)):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid credentials")
            return user_service_pb2.AuthResponse()
        
        user_id = self.user_credentials[request.username]['user_id']
        return user_service_pb2.AuthResponse(
            success=True,
            token=str(uuid.uuid4()),
            user_id=user_id,
            message="Authentication successful"
        )

    def UpdateUser(self, request, context):
        if request.user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_service_pb2.UserResponse()
        
        user_data = self.users[request.user_id]
        if request.email: user_data['email'] = request.email
        if request.first_name: user_data['first_name'] = request.first_name
        if request.last_name: user_data['last_name'] = request.last_name
        if request.phone: user_data['phone'] = request.phone
        if request.address: user_data['address'] = request.address
        
        self.users[request.user_id] = user_data
        return user_service_pb2.UserResponse(**user_data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("User Service started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
