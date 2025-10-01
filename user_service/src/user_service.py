import grpc
from concurrent import futures
import time
import ecommerce_pb2
import ecommerce_pb2_grpc
import uuid
from threading import Lock

class UserService(ecommerce_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {}
        self.lock = Lock()
        # Add admin user
        admin_id = str(uuid.uuid4())
        self.users[admin_id] = ecommerce_pb2.User(
            user_id=admin_id,
            username="admin",
            email="admin@ecommerce.com",
            password="admin123",
            first_name="Admin",
            last_name="User",
            address="Admin Address",
            phone="1234567890",
            is_admin=True
        )

    def RegisterUser(self, request, context):
        with self.lock:
            # Check if username already exists
            for user in self.users.values():
                if user.username == request.username:
                    return ecommerce_pb2.UserResponse(
                        success=False,
                        message="Username already exists"
                    )
            
            user_id = str(uuid.uuid4())
            new_user = ecommerce_pb2.User(
                user_id=user_id,
                username=request.username,
                email=request.email,
                password=request.password,
                first_name=request.first_name,
                last_name=request.last_name,
                address=request.address,
                phone=request.phone,
                is_admin=False
            )
            self.users[user_id] = new_user
            
            return ecommerce_pb2.UserResponse(
                success=True,
                message="User registered successfully",
                user=new_user
            )

    def LoginUser(self, request, context):
        for user in self.users.values():
            if user.username == request.username and user.password == request.password:
                return ecommerce_pb2.UserResponse(
                    success=True,
                    message="Login successful",
                    user=user
                )
        
        return ecommerce_pb2.UserResponse(
            success=False,
            message="Invalid username or password"
        )

    def GetUser(self, request, context):
        user = self.users.get(request.user_id)
        if user:
            return user
        context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ecommerce_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("User Service started on port 50051")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
