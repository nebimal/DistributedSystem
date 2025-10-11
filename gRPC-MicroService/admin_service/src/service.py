import grpc
from concurrent import futures
import order_service_pb2
import order_service_pb2_grpc
import product_service_pb2
import product_service_pb2_grpc

import common_pb2

class AdminService:
    def __init__(self):
        self.order_stub = order_service_pb2_grpc.OrderServiceStub(
            grpc.insecure_channel('order-service:50054')
        )
        self.product_stub = product_service_pb2_grpc.ProductServiceStub(
            grpc.insecure_channel('product-service:50052')
        )

    def get_all_orders(self):
        # In a real implementation, you would have a proper way to get all orders
        # For this example, we'll simulate getting orders
        try:
            # This would need to be implemented properly in the order service
            return []
        except grpc.RpcError as e:
            print(f"Error fetching orders: {e}")
            return []

    def update_order_status(self, order_id, status):
        try:
            response = self.order_stub.UpdateOrderStatus(
                order_service_pb2.UpdateOrderStatusRequest(
                    order_id=order_id,
                    status=status
                )
            )
            return response
        except grpc.RpcError as e:
            print(f"Error updating order status: {e}")
            return None

    def cancel_order(self, order_id):
        try:
            response = self.order_stub.CancelOrder(
                order_service_pb2.OrderRequest(order_id=order_id)
            )
            return response
        except grpc.RpcError as e:
            print(f"Error cancelling order: {e}")
            return None

def serve():
    # Admin service would typically have its own gRPC service definition
    # For simplicity, we're implementing it as a helper service
    admin_service = AdminService()
    print("Admin Service started - ready to manage orders and products")
    
    # Keep the service running
    try:
        while True:
            import time
            time.sleep(3600)  # Sleep for 1 hour
    except KeyboardInterrupt:
        print("Admin Service stopped")

if __name__ == '__main__':
    serve()
