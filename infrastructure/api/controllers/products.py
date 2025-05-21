from flask import (Blueprint, request)
from core.domain.models.products import Product

products = Blueprint('products', __name__, url_prefix='/api/products')

@products.route('/add-submodule', methods=['POST'])
def add_submodule():
    product = Product.from_dict(request.get_json())
    return product.to_dict(), 200