import requests
import atexit

from pact import Consumer, Provider
from pytest import mark

pact = Consumer('shopping-cart-service').has_pact_with(Provider('product-service'), port=5003)
# Setup
pact.start_service()
# Teardown
atexit.register(pact.stop_service)


@mark.contract
def test_get_product_by_id():
    expected = {
        "id": 123,
        "name": "Example Product",
        "price": 9.99
    }

    (pact
        .given('product with id 123 exists')
        .upon_receiving('get product by id')
        .with_request('GET', '/products/123')
        .will_respond_with(200, body=expected))

    with pact:
        response = requests.get('http://localhost:5003/products/123')
        assert response.status_code == 200
        assert response.json() == expected


@mark.contract
def test_get_product_by_category():
    expected = {
        "products": [
            {
                "id": 123,
                "name": "Example Product",
                "price": 9.99
            },
            {
                "id": 124,
                "name": "Example Product 4",
                "price": 9.99
            },
            {
                "id": 125,
                "name": "Example Product 5",
                "price": 9.99
            }
        ]
    }

    (pact
        .given('category with id 123 exists')
        .upon_receiving('get product by category')
        .with_request('GET', '/category/123')
        .will_respond_with(200, body=expected))

    with pact:
        response = requests.get('http://localhost:5003/category/123')
        assert response.status_code == 200
        assert response.json() == expected

# pytest -m contract