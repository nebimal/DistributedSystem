import grpc
import ecommerce_pb2
import ecommerce_pb2_grpc
from concurrent import futures
import time
from flask import Flask, jsonify, request
import json
from threading import Lock

app = Flask(__name__)

# gRPC channel configurations
USER_SERVICE_CHANNEL = grpc.insecure_channel('localhost:50051')
PRODUCT_SERVICE_CHANNEL = grpc.insecure_channel('localhost:50052')
CART_SERVICE_CHANNEL = grpc.insecure_channel('localhost:50053')
ORDER_SERVICE_CHANNEL = grpc.insecure_channel('localhost:50054')

# Create service stubs
user_stub = ecommerce_pb2_grpc.UserServiceStub(USER_SERVICE_CHANNEL)
product_stub = ecommerce_pb2_grpc.ProductServiceStub(PRODUCT_SERVICE_CHANNEL)
cart_stub = ecommerce_pb2_grpc.CartServiceStub(CART_SERVICE_CHANNEL)
order_stub = ecommerce_pb2_grpc.OrderServiceStub(ORDER_SERVICE_CHANNEL)

@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        user_response = user_stub.RegisterUser(ecommerce_pb2.User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            phone=data['phone']
        ))
        
        return jsonify({
            'success': user_response.success,
            'message': user_response.message,
            'user': {
                'user_id': user_response.user.user_id,
                'username': user_response.user.username,
                'email': user_response.user.email
            } if user_response.success else None
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        user_response = user_stub.LoginUser(ecommerce_pb2.LoginRequest(
            username=data['username'],
            password=data['password']
        ))
        
        return jsonify({
            'success': user_response.success,
            'message': user_response.message,
            'user': {
                'user_id': user_response.user.user_id,
                'username': user_response.user.username,
                'email': user_response.user.email,
                'is_admin': user_response.user.is_admin
            } if user_response.success else None
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = product_stub.GetAllProducts(ecommerce_pb2.Empty())
        product_list = []
        for product in products.products:
            product_list.append({
                'product_id': product.product_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'category': product.category,
                'image_url': product.image_url
            })
        
        return jsonify({'success': True, 'products': product_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        cart = cart_stub.GetCart(ecommerce_pb2.CartRequest(user_id=user_id))
        cart_items = []
        for item in cart.items:
            cart_items.append({
                'product_id': item.product_id,
                'product_name': item.product_name,
                'quantity': item.quantity,
                'price': item.price
            })
        
        return jsonify({
            'success': True,
            'cart': {
                'user_id': cart.user_id,
                'items': cart_items,
                'total_amount': cart.total_amount
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    try:
        data = request.json
        cart_response = cart_stub.AddToCart(ecommerce_pb2.CartItem(
            user_id=data['user_id'],
            product_id=data['product_id'],
            product_name=data['product_name'],
            quantity=data['quantity'],
            price=data['price']
        ))
        
        cart_items = []
        for item in cart_response.cart.items:
            cart_items.append({
                'product_id': item.product_id,
                'product_name': item.product_name,
                'quantity': item.quantity,
                'price': item.price
            })
        
        return jsonify({
            'success': cart_response.success,
            'message': cart_response.message,
            'cart': {
                'user_id': cart_response.cart.user_id,
                'items': cart_items,
                'total_amount': cart_response.cart.total_amount
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.json
        # Get cart first
        cart = cart_stub.GetCart(ecommerce_pb2.CartRequest(user_id=data['user_id']))
        
        # Create order items from cart
        order_items = []
        for item in cart.items:
            order_items.append(ecommerce_pb2.OrderItem(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price
            ))
        
        # Create order
        order_response = order_stub.CreateOrder(ecommerce_pb2.Order(
            user_id=data['user_id'],
            items=order_items,
            total_amount=cart.total_amount,
            shipping_address=data['shipping_address'],
            payment_method=data['payment_method']
        ))
        
        # Clear cart after successful order
        if order_response.success:
            cart_stub.ClearCart(ecommerce_pb2.CartRequest(user_id=data['user_id']))
        
        return jsonify({
            'success': order_response.success,
            'message': order_response.message,
            'order': {
                'order_id': order_response.order.order_id,
                'status': order_response.order.status,
                'total_amount': order_response.order.total_amount
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/orders/user/<user_id>', methods=['GET'])
def get_user_orders(user_id):
    try:
        orders = order_stub.GetUserOrders(ecommerce_pb2.UserOrdersRequest(user_id=user_id))
        order_list = []
        for order in orders.orders:
            items = []
            for item in order.items:
                items.append({
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'quantity': item.quantity,
                    'price': item.price
                })
            
            order_list.append({
                'order_id': order.order_id,
                'status': order.status,
                'total_amount': order.total_amount,
                'items': items,
                'created_at': order.created_at
            })
        
        return jsonify({'success': True, 'orders': order_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.json
        order_response = order_stub.UpdateOrderStatus(ecommerce_pb2.OrderStatusUpdate(
            order_id=order_id,
            status=data['status']
        ))
        
        return jsonify({
            'success': order_response.success,
            'message': order_response.message
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("API Gateway started on port 5000")
    app.run(port=5000, debug=True)
