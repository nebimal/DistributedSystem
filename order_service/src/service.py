import grpc
from concurrent import futures
import uuid
from datetime import datetime
import random

import order_service_pb2
import order_service_pb2_grpc
import common_pb2
import cart_service_pb2
import cart_service_pb2_grpc

class OrderService(order_service_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.orders = {}
        self.cart_stub = cart_service_pb2_grpc.CartServiceStub(
            grpc.insecure_channel('cart-service:50053')
        )

    def CreateOrder(self, request, context):
        try:
            # Get current cart
            cart_response = self.cart_stub.GetCart(
                cart_service_pb2.CartRequest(user_id=request.user_id)
            )
            
            if not cart_response.items:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Cart is empty")
                return order_service_pb2.OrderResponse()
            
            order_id = str(uuid.uuid4())
            tracking_number = f"TN{random.randint(100000, 999999)}"
            
            order_data = {
                'order_id': order_id,
                'user_id': request.user_id,
                'items': [order_service_pb2.OrderItem(
                    product_id=item.product_id,
                    name=item.name,
                    price=item.price,
                    quantity=item.quantity
                ) for item in cart_response.items],
                'total_amount': cart_response.total_amount,
                'status': order_service_pb2.OrderStatus.Value('PENDING'),
                'shipping_address': request.shipping_address,
                'payment_method': request.payment_method,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'tracking_number': tracking_number
            }
            
            self.orders[order_id] = order_data
            
            # Clear the cart after order creation
            self.cart_stub.ClearCart(cart_service_pb2.CartRequest(user_id=request.user_id))
            
            return order_service_pb2.OrderResponse(**order_data)
            
        except grpc.RpcError as e:
            context.set_code(e.code())
            context.set_details(e.details())
            return order_service_pb2.OrderResponse()

    def GetOrder(self, request, context):
        if request.order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return order_service_pb2.OrderResponse()
        
        return order_service_pb2.OrderResponse(**self.orders[request.order_id])

    def GetUserOrders(self, request, context):
        user_orders = [order for order in self.orders.values() if order['user_id'] == request.user_id]
        
        # Pagination
        page = request.pagination.page if request.pagination.page else 1
        limit = request.pagination.limit if request.pagination.limit else 10
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        paginated_orders = user_orders[start_idx:end_idx]
        
        return order_service_pb2.UserOrdersResponse(
            orders=[order_service_pb2.OrderResponse(**order) for order in paginated_orders],
            total=len(user_orders),
            page=page,
            limit=limit
        )

    def UpdateOrderStatus(self, request, context):
        if request.order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return order_service_pb2.OrderResponse()
        
        order_data = self.orders[request.order_id]
        order_data['status'] = request.status
        order_data['updated_at'] = datetime.now().isoformat()
        
        self.orders[request.order_id] = order_data
        return order_service_pb2.OrderResponse(**order_data)

    def CancelOrder(self, request, context):
        if request.order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return common_pb2.StatusResponse()
        
        order_data = self.orders[request.order_id]
        if order_data['status'] in [order_service_pb2.OrderStatus.Value('SHIPPED'), 
                                  order_service_pb2.OrderStatus.Value('DELIVERED')]:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details("Cannot cancel shipped or delivered order")
            return common_pb2.StatusResponse()
        
        order_data['status'] = order_service_pb2.OrderStatus.Value('CANCELLED')
        order_data['updated_at'] = datetime.now().isoformat()
        
        return common_pb2.StatusResponse(success=True, message="Order cancelled successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_service_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("Order Service started on port 50054")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
