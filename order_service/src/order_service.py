import grpc
from concurrent import futures
import time
import ecommerce_pb2
import ecommerce_pb2_grpc
import uuid
from datetime import datetime
from threading import Lock

class OrderService(ecommerce_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.orders = {}
        self.lock = Lock()

    def CreateOrder(self, request, context):
        with self.lock:
            order_id = str(uuid.uuid4())
            current_time = datetime.now().isoformat()
            
            new_order = ecommerce_pb2.Order(
                order_id=order_id,
                user_id=request.user_id,
                items=request.items,
                total_amount=request.total_amount,
                status="PENDING",
                shipping_address=request.shipping_address,
                payment_method=request.payment_method,
                created_at=current_time,
                updated_at=current_time
            )
            
            self.orders[order_id] = new_order
            
            return ecommerce_pb2.OrderResponse(
                success=True,
                message="Order created successfully",
                order=new_order
            )

    def GetOrder(self, request, context):
        order = self.orders.get(request.order_id)
        if order:
            return order
        context.abort(grpc.StatusCode.NOT_FOUND, "Order not found")

    def GetUserOrders(self, request, context):
        user_orders = [order for order in self.orders.values() if order.user_id == request.user_id]
        return ecommerce_pb2.OrderList(orders=user_orders)

    def UpdateOrderStatus(self, request, context):
        with self.lock:
            order = self.orders.get(request.order_id)
            if not order:
                return ecommerce_pb2.OrderResponse(
                    success=False,
                    message="Order not found"
                )
            
            order.status = request.status
            order.updated_at = datetime.now().isoformat()
            
            return ecommerce_pb2.OrderResponse(
                success=True,
                message="Order status updated successfully",
                order=order
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ecommerce_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("Order Service started on port 50054")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
