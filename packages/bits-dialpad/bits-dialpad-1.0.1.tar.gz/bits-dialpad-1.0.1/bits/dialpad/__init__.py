"""Dialpad class file."""

import json
import requests


class Dialpad(object):
    """Dialpad class."""

    def __init__(self, token, verbose=False):
        """Initialize a class instance."""
        self.token = token
        self.verbose = verbose

        # set the API base url
        self.base_url = 'https://dialpad.com/api/v2'

        # set the headers
        self.headers = {
            'Authorization': 'Bearer %s' % (self.token)
        }

    #
    # Helpers
    #
    def get_list(self, url, params):
        """Return a list of paginated items."""
        # get first page of results
        response = requests.get(url, headers=self.headers, params=params)

        # get json data
        try:
            data = json.loads(response.text)
        except Exception as e:
            print('ERROR: Failed to parse json response: %s' % (e))
            return

        cursor = data.get('cursor')
        items = data.get('items', [])

        while cursor:
            params['cursor'] = cursor

            # get next page of reesults
            response = requests.get(url, headers=self.headers, params=params)

            # get json data
            try:
                data = json.loads(response.text)
            except Exception as e:
                print('ERROR: Failed to parse json response: %s' % (e))
                print(response.text)
                return

            cursor = data.get('cursor')
            items.extend(data.get('items', []))

        return items

    #
    # Departments: /api/v2/departments
    #
    def get_departments(self):
        """Return a list of departments."""
        url = '%s/departments' % (self.base_url)
        return self.get_list(url, params={})

    #
    # Numbers: /api/v2/numbers
    #
    def get_numbers(self, status=None):
        """Return a list of numbers."""
        url = '%s/numbers' % (self.base_url)
        params = {
            # 'limit': '40',
            'status': status,
        }
        return self.get_list(url, params=params)

    #
    # Offices: /api/v2/offices
    #
    def get_offices(self):
        """Return a list of offices."""
        url = '%s/offices' % (self.base_url)
        return self.get_list(url, params={})

    #
    # Rooms: /api/v2/rooms
    #
    def get_rooms(self):
        """Return a list of rooms."""
        url = '%s/rooms' % (self.base_url)
        return self.get_list(url, params={})

    #
    # Users: /api/v2/users
    #
    def assign_user_number(self, user_id, area_code=None, number=None):
        """Assign a number to a user."""
        url = '%s/users/%s/assign_number' % (
            self.base_url,
            user_id,
        )
        body = {
            'area_code': area_code,
            'number': number,
        }
        response = requests.post(url, headers=self.headers, json=body)
        return response.json()

    def create_user(self, body):
        """Create a user in Dialpad."""
        url = '%s/users' % (self.base_url)
        response = requests.post(url, headers=self.headers, json=body)
        return response.json()

    def get_users(self, email=None, state=None, limit=1000, cursor=None):
        """Return a list of users."""
        params = {
            'email': email,
            'state': state,
            'limit': limit,
            'cursor': cursor,
        }
        url = '%s/users' % (self.base_url)

        # get first page of reesults
        response = requests.get(url, headers=self.headers, params=params)

        # get json data
        try:
            data = json.loads(response.text)
        except Exception as e:
            print('ERROR: Failed to parse json response: %s' % (e))
            return

        cursor = data.get('cursor')
        items = data.get('items', [])

        while cursor:
            params['cursor'] = cursor

            # get next page of reesults
            response = requests.get(url, headers=self.headers, params=params)

            # get json data
            try:
                data = json.loads(response.text)
            except Exception as e:
                print('ERROR: Failed to parse json response: %s' % (e))
                return

            cursor = data.get('cursor')
            items.extend(data.get('items', []))

        return items

    def patch_user(self, user_id, body):
        """Patch a Dialpad user."""
        url = '%s/users/%s' % (self.base_url, user_id)
        return requests.patch(url, headers=self.headers, json=body)
