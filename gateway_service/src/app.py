from flask import Flask, jsonify, request
import grpc
import json

# Import generated gRPC code
import user_service_pb2
import user_service_pb2_grpc
import product_service_pb2
import product_service_pb2_grpc
import cart_service_pb2
import cart_service_pb2_grpc
import order_service_pb2
import order_service_pb2_grpc

app = Flask(__name__)

# gRPC channel configurations
USER_SERVICE_HOST = 'user-service:50051'
PRODUCT_SERVICE_HOST = 'product-service:50052'
CART_SERVICE_HOST = 'cart-service:50053'
ORDER_SERVICE_HOST = 'order-service:50054'

@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        with grpc.insecure_channel(USER_SERVICE_HOST) as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)
            response = stub.RegisterUser(
                user_service_pb2.UserRegistrationRequest(**data)
            )
            return jsonify({
                'user_id': response.user_id,
                'username': response.username,
                'email': response.email,
                'message': 'User registered successfully'
            }), 201
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 400

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        category = request.args.get('category')
        
        with grpc.insecure_channel(PRODUCT_SERVICE_HOST) as channel:
            stub = product_service_pb2_grpc.ProductServiceStub(channel)
            response = stub.ListProducts(
                product_service_pb2.ProductListRequest(
                    pagination=product_service_pb2.Pagination(page=page, limit=limit),
                    category=category
                )
            )
            
            products = [{
                'product_id': p.product_id,
                'name': p.name,
                'description': p.description,
                'price': p.price,
                'stock': p.stock,
                'category': p.category,
                'image_url': p.image_url
            } for p in response.products]
            
            return jsonify({
                'products': products,
                'total': response.total,
                'page': response.page,
                'limit': response.limit
            }), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 400

@app.route('/api/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        with grpc.insecure_channel(CART_SERVICE_HOST) as channel:
            stub = cart_service_pb2_grpc.CartServiceStub(channel)
            response = stub.GetCart(cart_service_pb2.CartRequest(user_id=user_id))
            
            cart_items = [{
                'product_id': item.product_id,
                'name': item.name,
                'price': item.price,
                'quantity': item.quantity,
                'image_url': item.image_url
            } for item in response.items]
            
            return jsonify({
                'user_id': response.user_id,
                'items': cart_items,
                'total_amount': response.total_amount,
                'total_items': response.total_items
            }), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 400

@app.route('/api/cart/<user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    try:
        data = request.get_json()
        with grpc.insecure_channel(CART_SERVICE_HOST) as channel:
            stub = cart_service_pb2_grpc.CartServiceStub(channel)
            response = stub.AddItem(
                cart_service_pb2.AddItemRequest(
                    user_id=user_id,
                    product_id=data['product_id'],
                    quantity=data.get('quantity', 1)
                )
            )
            
            cart_items = [{
                'product_id': item.product_id,
                'name': item.name,
                'price': item.price,
                'quantity': item.quantity,
                'image_url': item.image_url
            } for item in response.items]
            
            return jsonify({
                'user_id': response.user_id,
                'items': cart_items,
                'total_amount': response.total_amount,
                'total_items': response.total_items,
                'message': 'Item added to cart successfully'
            }), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 400

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        with grpc.insecure_channel(ORDER_SERVICE_HOST) as channel:
            stub = order_service_pb2_grpc.OrderServiceStub(channel)
            response = stub.CreateOrder(
                order_service_pb2.CreateOrderRequest(**data)
            )
            
            order_items = [{
                'product_id': item.product_id,
                'name': item.name,
                'price': item.price,
                'quantity': item.quantity
            } for item in response.items]
            
            return jsonify({
                'order_id': response.order_id,
                'user_id': response.user_id,
                'items': order_items,
                'total_amount': response.total_amount,
                'status': order_service_pb2.OrderStatus.Name(response.status),
                'tracking_number': response.tracking_number,
                'message': 'Order created successfully'
            }), 201
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 400

@app.route('/api/orders/<user_id>', methods=['GET'])
def get_user_orders(user_id):
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        with grpc.insecure_channel(ORDER_SERVICE_HOST) as channel:
            stub = order_service_pb2_grpc.OrderServiceStub(channel)
            response = stub.GetUserOrders(
                order_service_pb2.UserOrdersRequest(
                    user_id=user_id,
                    pagination=order_service_pb2.Pagination(page=page, limit=limit)
                )
            )
            
            orders = [{
                'order_id': o.order_id,
                'user_id': o.user_id,
                'items': [{
                    'product_id': item.product_id,
                    'name': item.name,
                    'price': item.price,
                    'quantity': item.quantity
                } for item in o.items],
                'total_amount': o.total_amount,
                'status': order_service_pb2.OrderStatus.Name(o.status),
                'tracking_number': o.tracking_number,
                'created_at': o.created_at
            } for o in response.orders]
            
            return jsonify({
                'orders': orders,
                'total': response.total,
                'page': response.page,
                'limit': response.limit
            }), 200
    except grpc.RpcError as e:
        return jsonify({'error': e.details()}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
