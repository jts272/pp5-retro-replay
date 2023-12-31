from decimal import Decimal
from products.models import Product


class Basket:
    def __init__(self, request):
        """Get or create the user's basket data using Django sessions.

        Arguments:
            request -- HttpRequest

        Reference:
        https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=5406
        """
        # Get the session from the request object
        self.session = request.session
        # Check user's cookies for session data
        basket = self.session.get("session_key")
        if "session_key" not in request.session:
            # Create new session
            basket = self.session["session_key"] = {}
        # Get existing session data or new empty dictionary basket
        self.basket = basket

    def __iter__(self):
        """Allow iteration of the Basket class for showing summary data.

        Yields:
            Item price in number format

        Reference:
        https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=9977
        """

        # Iterate over session keys to get product keys contained within
        product_ids = self.basket.keys()
        # Get basket items from the database
        products = Product.objects.filter(pk__in=product_ids)
        # Make copy of the session data for further processing
        basket = self.basket.copy()

        for product in products:
            # Give each product access to its product data
            basket[str(product.pk)]["product"] = product

        for item in basket.values():
            # Convert str price from add function to decimal for calculations
            item["price"] = Decimal(item["price"])
            yield item

    def __len__(self):
        """Count the number of keys in the basket. This represents the
        number of individual products in the basket.

        Returns:
            Number of keys found in the session basket

        Reference:
        https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=8998
        """
        return len(self.basket.keys())

    def add(self, product):
        """Gets the product provided and adds it to the basket if not present.

        Arguments:
            product -- product to query the database for

        Reference:
        https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=7710
        """
        # Get product id which is provided by the add to basket view
        product_id = product.pk
        # Check if product is present in basket from class init method
        # 'basket' is equivalent to the user's session
        if product_id not in self.basket:
            # Add product to basket with reference to its price
            self.basket[product_id] = {"price": str(product.price)}

        # Mark the session as modified to save it
        self.session.modified = True

    def remove(self, product):
        """Removes the given item from the basket

        Arguments:
            product -- product to remove, captured in ajax and passed in
            from the remove from basket view

        Reference:
        https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_
        """
        # Get product id which is provided by the remove from basket view
        product_id = product

        if product_id in self.basket:
            # Remove the product from the basket
            del self.basket[product_id]

        # Mark the session as modified to save it
        self.session.modified = True

    def get_subtotal(self):
        """Performs a sum of all basket items to return the subtotal.

        Returns:
            Sum of price values from the basket

        Reference:
        https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=11009
        """
        return sum(Decimal(item["price"]) for item in self.basket.values())

    def clear_session(self):
        """Clear the basket by deleting the session key."""
        del self.session["session_key"]
        self.session.modified = True
