
def cart_dict(product, quantity,color):
    price = disconted_price(product.price, product.discount)
    productDict = {
        'id' :product.id,
        'name':product.product_name,
        'price': price,
        'quantity': int(quantity),
        'colors': {
            color: int(quantity)
        },  
        'image': product.image_1,  
    }
    return productDict

def disconted_price(price, discount):
    discnt = (100 - int(discount)) * 0.01
    new_price = int(price) * discnt
    return new_price