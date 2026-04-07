cart = []

def add_to_cart(name):
    cart.append(name)

def show_cart():
    print("\n🛒 Cart:")
    for item in cart:
        print("-", item)
