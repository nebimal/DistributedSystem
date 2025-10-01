from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("user_id", "username", "email", "password", "first_name", "last_name", "address", "phone", "is_admin")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    IS_ADMIN_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    address: str
    phone: str
    is_admin: bool
    def __init__(self, user_id: _Optional[str] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., password: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., address: _Optional[str] = ..., phone: _Optional[str] = ..., is_admin: bool = ...) -> None: ...

class UserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ("success", "message", "user")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    user: User
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class Product(_message.Message):
    __slots__ = ("product_id", "name", "description", "price", "stock", "category", "image_url")
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    name: str
    description: str
    price: float
    stock: int
    category: str
    image_url: str
    def __init__(self, product_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., price: _Optional[float] = ..., stock: _Optional[int] = ..., category: _Optional[str] = ..., image_url: _Optional[str] = ...) -> None: ...

class ProductRequest(_message.Message):
    __slots__ = ("product_id",)
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    def __init__(self, product_id: _Optional[str] = ...) -> None: ...

class ProductList(_message.Message):
    __slots__ = ("products",)
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    products: _containers.RepeatedCompositeFieldContainer[Product]
    def __init__(self, products: _Optional[_Iterable[_Union[Product, _Mapping]]] = ...) -> None: ...

class ProductResponse(_message.Message):
    __slots__ = ("success", "message", "product")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    product: Product
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., product: _Optional[_Union[Product, _Mapping]] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ("order_id", "user_id", "items", "total_amount", "status", "shipping_address", "payment_method", "created_at", "updated_at")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SHIPPING_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_METHOD_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    user_id: str
    items: _containers.RepeatedCompositeFieldContainer[OrderItem]
    total_amount: float
    status: str
    shipping_address: str
    payment_method: str
    created_at: str
    updated_at: str
    def __init__(self, order_id: _Optional[str] = ..., user_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[OrderItem, _Mapping]]] = ..., total_amount: _Optional[float] = ..., status: _Optional[str] = ..., shipping_address: _Optional[str] = ..., payment_method: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class OrderItem(_message.Message):
    __slots__ = ("product_id", "product_name", "quantity", "price")
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    product_name: str
    quantity: int
    price: float
    def __init__(self, product_id: _Optional[str] = ..., product_name: _Optional[str] = ..., quantity: _Optional[int] = ..., price: _Optional[float] = ...) -> None: ...

class OrderRequest(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    def __init__(self, order_id: _Optional[str] = ...) -> None: ...

class UserOrdersRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class OrderStatusUpdate(_message.Message):
    __slots__ = ("order_id", "status")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class OrderList(_message.Message):
    __slots__ = ("orders",)
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    orders: _containers.RepeatedCompositeFieldContainer[Order]
    def __init__(self, orders: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...) -> None: ...

class OrderResponse(_message.Message):
    __slots__ = ("success", "message", "order")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    order: Order
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class Cart(_message.Message):
    __slots__ = ("user_id", "items", "total_amount")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    items: _containers.RepeatedCompositeFieldContainer[CartItem]
    total_amount: float
    def __init__(self, user_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[CartItem, _Mapping]]] = ..., total_amount: _Optional[float] = ...) -> None: ...

class CartItem(_message.Message):
    __slots__ = ("user_id", "product_id", "product_name", "quantity", "price")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    product_id: str
    product_name: str
    quantity: int
    price: float
    def __init__(self, user_id: _Optional[str] = ..., product_id: _Optional[str] = ..., product_name: _Optional[str] = ..., quantity: _Optional[int] = ..., price: _Optional[float] = ...) -> None: ...

class CartRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class CartResponse(_message.Message):
    __slots__ = ("success", "message", "cart")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CART_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    cart: Cart
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., cart: _Optional[_Union[Cart, _Mapping]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
