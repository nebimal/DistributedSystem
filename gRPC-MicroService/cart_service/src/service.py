import grpc
from concurrent import futures
import product_service_pb2
import product_service_pb2_grpc

import cart_service_pb2
import cart_service_pb2_grpc
import common_pb2

class CartService(cart_service_pb2_grpc.CartServiceServicer):
    def __init__(self):
        self.carts = {}
        self.product_stub = product_service_pb2_grpc.ProductServiceStub(
            grpc.insecure_channel('product-service:50052')
        )

    def GetCart(self, request, context):
        if request.user_id not in self.carts:
            return cart_service_pb2.CartResponse(user_id=request.user_id, items=[], total_amount=0, total_items=0)
        
        cart = self.carts[request.user_id]
        return self._calculate_cart_response(request.user_id, cart)

    def AddItem(self, request, context):
        try:
            # Get product details
            product_response = self.product_stub.GetProduct(
                product_service_pb2.ProductRequest(product_id=request.product_id)
            )
            
            if request.user_id not in self.carts:
                self.carts[request.user_id] = {}
            
            cart = self.carts[request.user_id]
            
            if request.product_id in cart:
                cart[request.product_id]['quantity'] += request.quantity
            else:
                cart[request.product_id] = {
                    'product_id': request.product_id,
                    'name': product_response.name,
                    'price': product_response.price,
                    'quantity': request.quantity,
                    'image_url': product_response.image_url
                }
            
            return self._calculate_cart_response(request.user_id, cart)
            
        except grpc.RpcError as e:
            context.set_code(e.code())
            context.set_details(e.details())
            return cart_service_pb2.CartResponse()

    def RemoveItem(self, request, context):
        if (request.user_id not in self.carts or 
            request.product_id not in self.carts[request.user_id]):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Item not found in cart")
            return cart_service_pb2.CartResponse()
        
        cart = self.carts[request.user_id]
        del cart[request.product_id]
        
        return self._calculate_cart_response(request.user_id, cart)

    def UpdateItem(self, request, context):
        if (request.user_id not in self.carts or 
            request.product_id not in self.carts[request.user_id]):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Item not found in cart")
            return cart_service_pb2.CartResponse()
        
        cart = self.carts[request.user_id]
        if request.quantity <= 0:
            del cart[request.product_id]
        else:
            cart[request.product_id]['quantity'] = request.quantity
        
        return self._calculate_cart_response(request.user_id, cart)

    def ClearCart(self, request, context):
        if request.user_id in self.carts:
            del self.carts[request.user_id]
        
        return common_pb2.StatusResponse(success=True, message="Cart cleared successfully")

    def _calculate_cart_response(self, user_id, cart):
        items = []
        total_amount = 0
        total_items = 0
        
        for item_data in cart.values():
            item_total = item_data['price'] * item_data['quantity']
            items.append(cart_service_pb2.CartItem(
                product_id=item_data['product_id'],
                name=item_data['name'],
                price=item_data['price'],
                quantity=item_data['quantity'],
                image_url=item_data['image_url']
            ))
            total_amount += item_total
            total_items += item_data['quantity']
        
        return cart_service_pb2.CartResponse(
            user_id=user_id,
            items=items,
            total_amount=total_amount,
            total_items=total_items
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cart_service_pb2_grpc.add_CartServiceServicer_to_server(CartService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Cart Service started on port 50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
