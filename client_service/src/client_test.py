import grpc
import ecommerce_pb2
import ecommerce_pb2_grpc
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_ecommerce_flow():
    print("=== Testing E-commerce System ===\n")
    
    # Test User Registration
    print("1. User Registration:")
    register_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "address": "123 Main St, City, Country",
        "phone": "123-456-7890"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print(f"Registration Response: {response.json()}\n")
    
    # Test Login
    print("2. User Login:")
    login_data = {
        "username": "john_doe",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    login_result = response.json()
    print(f"Login Response: {login_result}\n")
    
    if not login_result['success']:
        print("Login failed. Exiting test.")
        return
    
    user_id = login_result['user']['user_id']
    
    # Test Product Browsing
    print("3. Product Browsing:")
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    print(f"Found {len(products['products'])} products\n")
    
    # Test Adding to Cart
    print("4. Adding to Cart:")
    if products['products']:
        product = products['products'][0]
        cart_data = {
            "user_id": user_id,
            "product_id": product['product_id'],
            "product_name": product['name'],
            "quantity": 2,
            "price": product['price']
        }
        
        response = requests.post(f"{BASE_URL}/cart/add", json=cart_data)
        print(f"Add to Cart Response: {response.json()}\n")
    
    # Test View Cart
    print("5. View Cart:")
    response = requests.get(f"{BASE_URL}/cart/{user_id}")
    print(f"Cart Contents: {response.json()}\n")
    
    # Test Order Placement
    print("6. Order Placement:")
    order_data = {
        "user_id": user_id,
        "shipping_address": "123 Main St, City, Country",
        "payment_method": "Credit Card"
    }
    
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    order_result = response.json()
    print(f"Order Placement Response: {order_result}\n")
    
    # Test Order Tracking
    print("7. Order Tracking:")
    response = requests.get(f"{BASE_URL}/orders/user/{user_id}")
    orders = response.json()
    print(f"User Orders: {orders}\n")
    
    # Test Admin Order Management (if we have an admin)
    print("8. Admin Order Management:")
    # First login as admin
    admin_login = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=admin_login)
    admin_result = response.json()
    
    if admin_result['success'] and orders['orders']:
        order_id = orders['orders'][0]['order_id']
        status_update = {
            "status": "CONFIRMED"
        }
        
        response = requests.put(f"{BASE_URL}/admin/orders/{order_id}/status", json=status_update)
        print(f"Order Status Update: {response.json()}\n")

if __name__ == '__main__':
    test_ecommerce_flow()
