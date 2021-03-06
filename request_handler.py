import json
from http.server import BaseHTTPRequestHandler, HTTPServer
# from views import delete_animal, get_all_animals, get_single_animal, create_animal, update_animal, get_animals_by_location, get_animals_by_status
# from views import delete_location, get_all_locations, get_single_location, create_location, update_location
# from views import delete_customer, get_all_customers, get_single_customer, create_customer, update_customer, get_customer_by_email
# from views import delete_employee, get_all_employees, get_single_employee, create_employee, update_employee, get_employees_by_location
from urllib.parse import urlparse, parse_qs

from views import get_all_entries, get_single_entry, delete_entry, get_entries_with_search, create_entry, update_entry
from views import get_all_moods
from views import get_all_tags

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # def parse_url(self, path):
    #     """Parses url into usable components

    #     Args:
    #         self (object?): 
    #         path (url path): 

    #     Returns:
    #         the resource and ID in a tuple
    #     """
    #     # Just like splitting a string in JavaScript. If the
    #     # path is "/animals/1", the resulting list will
    #     # have "" at index 0, "animals" at index 1, and "1"
    #     # at index 2.
    #     path_params = path.split("/")
    #     resource = path_params[1]
    #     id = None

    #     # Try to get the item at index 2
    #     try:
    #         # Convert the string "1" to the integer 1
    #         # This is the new parseInt()
    #         id = int(path_params[2])
    #     except IndexError:
    #         pass  # No route parameter exists: /animals
    #     except ValueError:
    #         pass  # Request had trailing slash: /animals/

    #     return (resource, id)  # This is a tuple

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                        'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                        'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    # def do_GET(self):
    #     """Handles GET requests to the server
    #     """
    #     # Set the response code to 'Ok'
    #     self._set_headers(200)
    #     response = {}  # Default response

    #     # Parse the URL and capture the tuple that is returned
    #     (resource, id) = self.parse_url(self.path)

    #     if resource == "animals":
    #         if id is not None:
    #             response = f"{get_single_animal(id)}"

    #         else:
    #             response = f"{get_all_animals()}"

    #     if resource == "locations":
    #         if id is not None:
    #             response = f"{get_single_location(id)}"

    #         else:
    #             response = f"{get_all_locations()}"

    #     if resource == "employees":
    #         if id is not None:
    #             response = f"{get_single_employee(id)}"

    #         else:
    #             response = f"{get_all_employees()}"

    #     if resource == "customers":
    #         if id is not None:
    #             response = f"{get_single_customer(id)}"

    #         else:
    #             response = f"{get_all_customers()}"

    #     self.wfile.write(response.encode())

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
            elif resource == "moods":
                if id is not None:
                    response = f"{get_single_mood(id)}"
                else:
                    response = f"{get_all_moods()}"
            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"
            # elif resource == "locations":
            #     if id is not None:
            #         response = f"{get_single_location(id)}"
            #     else:
            #         response = f"{get_all_locations()}"

        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed
            
            # see if the query dictionary has an email key
            if query.get('q') and resource == 'entries':
                response = get_entries_with_search(query['q'][0])
            # if query.get('location_id') and resource == 'animals':
            #     response = get_animals_by_location(query['location_id'][0])
            # if query.get('status') and resource == 'animals':
            #     response = get_animals_by_status(query['status'][0])
            # if query.get('location_id') and resource == 'employees':
            #     response = get_employees_by_location(query['location_id'][0])

        self.wfile.write(response.encode())


    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new data
        new_data = None

        if resource == "entries":
            new_data = create_entry(post_body)
        # if resource == "locations":
        #     new_data = create_location(post_body)
        # if resource == "employees":
        #     new_data = create_employee(post_body)
        # if resource == "customers":
        #     new_data = create_customer(post_body)

        self.wfile.write(f"{new_data}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        """Handles PUT requests to the server
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)
        
        # if resource == "customers":
        #     success = update_customer(id, post_body)

        # if resource == "employees":
        #     success = update_employee(id, post_body)

        # if resource == "locations":
        #     success = update_location(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())


    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        # Delete a single animal from the list
        if resource == "entries":
            delete_entry(id)
        # if resource == "locations":
        #     delete_location(id)
        # if resource == "customers":
        #     delete_customer(id)
        # if resource == "employees":
        #     delete_employee(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
