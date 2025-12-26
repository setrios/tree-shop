from products.models import Tree
from decimal import Decimal, ROUND_HALF_UP


class Cart():
    def __init__(self, request):
        self.session = request.session

        # get current session key if it exists
        cart = self.session.get('session_key')

        # if user is new - create session key
        if not cart:
            cart = self.session['session_key'] = {}

        # make sure cart is avaliable on whole site
        # we need context processor for that
        self.cart = cart


    def add(self, product, quantity=1):
        product_id = str(product.id)
        # current_qty = self.cart[product_id]['quantity']  # vvv same, but with defualt values
        current_qty = self.cart.get(product_id, {}).get('quantity', 0)

        # stock check
        if current_qty + quantity > product.quantity:
            raise ValueError("Not enough stock available")

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price)
            }
        else: 
            self.cart[product_id]['quantity'] += quantity

        self.session.modified = True


    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True


    def update(self, product, quantity):
        product_id = str(product.id)

        if quantity > product.quantity:
            raise ValueError("Not enough stock")

        if quantity <= 0:
            self.remove(product)
        else:
            self.cart[product_id]['quantity'] = quantity

        self.session.modified = True


    def clear(self):
        self.session['session_key'] = {}
        self.cart = self.session['session_key']
        self.session.modified = True


    def get_cart_items(self):
        product_ids = self.cart.keys()
        products = Tree.objects.filter(id__in=product_ids)
        
        cart_items = []
        for product in products:
            item = self.cart[str(product.id)]
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': float(item['price']),
                'total_price': float(item['price']) * item['quantity'],
            })
        
        return cart_items


    def get_total_price(self):
        total = sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
        return total.quantize(Decimal('0.00'))


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


