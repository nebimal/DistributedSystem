import grpc
from concurrent import futures
import time
import ecommerce_pb2
import ecommerce_pb2_grpc
from threading import Lock
import uuid

class CartService(ecommerce_pb2_grpc.CartServiceServicer):
    def __init__(self):
        self.carts = {}
        self.lock = Lock()

    def AddToCart(self, request, context):
        with self.lock:
            user_id = request.user_id
            if user_id not in self.carts:
                self.carts[user_id] = ecommerce_pb2.Cart(
                    user_id=user_id,
                    items=[],
                    total_amount=0.0
                )
            
            cart = self.carts[user_id]
            
            # Check if item already exists in cart
            for item in cart.items:
                if item.product_id == request.product_id:
                    item.quantity += request.quantity
                    break
            else:
                cart.items.append(request)
            
            # Recalculate total
            cart.total_amount = sum(item.price * item.quantity for item in cart.items)
            
            return ecommerce_pb2.CartResponse(
                success=True,
                message="Item added to cart",
                cart=cart
            )

    def GetCart(self, request, context):
        cart = self.carts.get(request.user_id)
        if not cart:
            cart = ecommerce_pb2.Cart(user_id=request.user_id, items=[], total_amount=0.0)
        return cart

    def RemoveFromCart(self, request, context):
        with self.lock:
            user_id = request.user_id
            if user_id not in self.carts:
                return ecommerce_pb2.CartResponse(
                    success=False,
                    message="Cart not found"
                )
            
            cart = self.carts[user_id]
            # Remove item from cart
            cart.items[:] = [item for item in cart.items if item.product_id != request.product_id]
            
            # Recalculate total
            cart.total_amount = sum(item.price * item.quantity for item in cart.items)
            
            return ecommerce_pb2.CartResponse(
                success=True,
                message="Item removed from cart",
                cart=cart
            )

    def ClearCart(self, request, context):
        with self.lock:
            user_id = request.user_id
            if user_id in self.carts:
                self.carts[user_id] = ecommerce_pb2.Cart(
                    user_id=user_id,
                    items=[],
                    total_amount=0.0
                )
            
            return ecommerce_pb2.CartResponse(
                success=True,
                message="Cart cleared",
                cart=self.carts.get(user_id, ecommerce_pb2.Cart(user_id=user_id))
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ecommerce_pb2_grpc.add_CartServiceServicer_to_server(CartService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Cart Service started on port 50053")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
