import grpc
from concurrent import futures
import uuid
from datetime import datetime

import product_service_pb2
import product_service_pb2_grpc
import common_pb2

class ProductService(product_service_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.products = {}
        self._initialize_sample_products()

    def _initialize_sample_products(self):
        sample_products = [
            {
                'name': 'Laptop',
                'description': 'High-performance laptop',
                'price': 999.99,
                'stock': 10,
                'category': 'Electronics',
                'image_url': '/images/laptop.jpg'
            },
            {
                'name': 'Smartphone',
                'description': 'Latest smartphone',
                'price': 699.99,
                'stock': 25,
                'category': 'Electronics',
                'image_url': '/images/phone.jpg'
            },
            {
                'name': 'Headphones',
                'description': 'Noise-cancelling headphones',
                'price': 199.99,
                'stock': 50,
                'category': 'Electronics',
                'image_url': '/images/headphones.jpg'
            }
        ]
        
        for product_data in sample_products:
            product_id = str(uuid.uuid4())
            product_data.update({
                'product_id': product_id,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
            self.products[product_id] = product_data

    def GetProduct(self, request, context):
        if request.product_id not in self.products:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_service_pb2.ProductResponse()
        
        return product_service_pb2.ProductResponse(**self.products[request.product_id])

    def ListProducts(self, request, context):
        products_list = list(self.products.values())
        
        # Filter by category if provided
        if request.category:
            products_list = [p for p in products_list if p['category'] == request.category]
        
        # Pagination
        page = request.pagination.page if request.pagination.page else 1
        limit = request.pagination.limit if request.pagination.limit else 10
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        paginated_products = products_list[start_idx:end_idx]
        
        return product_service_pb2.ProductListResponse(
            products=[product_service_pb2.ProductResponse(**p) for p in paginated_products],
            total=len(products_list),
            page=page,
            limit=limit
        )

    def CreateProduct(self, request, context):
        product_id = str(uuid.uuid4())
        product_data = {
            'product_id': product_id,
            'name': request.name,
            'description': request.description,
            'price': request.price,
            'stock': request.stock,
            'category': request.category,
            'image_url': request.image_url,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self.products[product_id] = product_data
        return product_service_pb2.ProductResponse(**product_data)

    def UpdateProduct(self, request, context):
        if request.product_id not in self.products:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_service_pb2.ProductResponse()
        
        product_data = self.products[request.product_id]
        if request.name: product_data['name'] = request.name
        if request.description: product_data['description'] = request.description
        if request.price: product_data['price'] = request.price
        if request.stock: product_data['stock'] = request.stock
        if request.category: product_data['category'] = request.category
        if request.image_url: product_data['image_url'] = request.image_url
        product_data['updated_at'] = datetime.now().isoformat()
        
        self.products[request.product_id] = product_data
        return product_service_pb2.ProductResponse(**product_data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_service_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Product Service started on port 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
