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
