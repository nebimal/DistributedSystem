import grpc
from concurrent import futures
import time
import ecommerce_pb2
import ecommerce_pb2_grpc
import uuid
from threading import Lock

class ProductService(ecommerce_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.products = {}
        self.lock = Lock()
        # Add sample products
        self._add_sample_products()

    def _add_sample_products(self):
        sample_products = [
            {"name": "Laptop", "description": "High-performance laptop", "price": 999.99, "stock": 10, "category": "Electronics"},
            {"name": "Smartphone", "description": "Latest smartphone", "price": 699.99, "stock": 25, "category": "Electronics"},
            {"name": "Headphones", "description": "Wireless headphones", "price": 199.99, "stock": 50, "category": "Electronics"},
            {"name": "T-Shirt", "description": "Cotton t-shirt", "price": 19.99, "stock": 100, "category": "Clothing"},
            {"name": "Coffee Mug", "description": "Ceramic coffee mug", "price": 9.99, "stock": 75, "category": "Home"}
        ]
        
        for product_data in sample_products:
            product_id = str(uuid.uuid4())
            self.products[product_id] = ecommerce_pb2.Product(
                product_id=product_id,
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                stock=product_data["stock"],
                category=product_data["category"],
                image_url=f"/images/{product_data['name'].lower().replace(' ', '_')}.jpg"
            )

    def GetProduct(self, request, context):
        product = self.products.get(request.product_id)
        if product:
            return product
        context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

    def GetAllProducts(self, request, context):
        return ecommerce_pb2.ProductList(products=list(self.products.values()))

    def AddProduct(self, request, context):
        with self.lock:
            product_id = str(uuid.uuid4())
            new_product = ecommerce_pb2.Product(
                product_id=product_id,
                name=request.name,
                description=request.description,
                price=request.price,
                stock=request.stock,
                category=request.category,
                image_url=request.image_url
            )
            self.products[product_id] = new_product
            
            return ecommerce_pb2.ProductResponse(
                success=True,
                message="Product added successfully",
                product=new_product
            )

    def UpdateProduct(self, request, context):
        with self.lock:
            if request.product_id not in self.products:
                return ecommerce_pb2.ProductResponse(
                    success=False,
                    message="Product not found"
                )
            
            self.products[request.product_id] = request
            return ecommerce_pb2.ProductResponse(
                success=True,
                message="Product updated successfully",
                product=request
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ecommerce_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Product Service started on port 50052")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
