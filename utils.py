import requests
from conf import BASE_URL
import json


class AuthenticationError(Exception):

    def __init__(self, message="Authentication error"):
        self.message = message
        super().__init__(self.message)


class ConcreteDatastore():

    def __init__(self):
        self.__data_user = None
        self.confirmation_url = None
        self.patch_response = None

    def __str__(self):
        if self.__data_user:
            return f"""
            email : {self.__data_user['email']}
            first name : {self.__data_user['first_name']}
            last name : {self.__data_user['last_name']}
            confirmation url : {self.confirmation_url}
            patch response : {self.patch_response} 
            """
        else:
            return "Empty, not yet authenticated"

    def create_user(self, data_registration):
        """
        create_user: a function that takes the registration information from a dictionary, adding the non-empty email field.
        create a user via the API and return a runtime message
        """

        if not self.__data_user:
            url = BASE_URL + 'api/v1.1/auth/register/'
            response = requests.post(url, json=data_registration)
            # Check the response status code
            if response.status_code == 201:
                self.__data_user = json.loads(response.content)
                return "User was successfully created", response.content

            return "User creation request failed.", response.status_code
        return "User already created for this instance.", None

    def login(self, email, password):
        """
        login method: verification of user existence and send authentication data 
        """

        if not self.__data_user:
            url = BASE_URL + 'api/v1.1/auth/login/'

            response = requests.post(url,
                                     json={
                                         'email': email,
                                         'password': password
                                     })

            # Check the response status code
            if response.status_code == 200:
                self.__data_user = json.loads(response.content)
                return "Connection established", response.content

            return "Connection failed", response.status_code

        return "User already logged in", None

    def get_confirmation_url(self):
        """
        function to find the confirmation url 
        """

        if not self.__data_user:
            raise AuthenticationError('Please log in or create a user !!')
        
        # Prepare the url for the request
        url =  '{}api/v1.1/job-application-request/?c_auth_with_token={}'.format(
            BASE_URL,
            self.__data_user['token']
        )

        response = requests.post(
            url,
            json={
                'email': self.__data_user['email'],
                'first_name': self.__data_user['first_name'],
                'last_name': self.__data_user['last_name'],
            }
        )

        # Check the response status code
        assert response.status_code == 201

        new_url = "{}?c_auth_with_token={}".format(
            json.loads(response.content)['url'], self.__data_user['token']
        )

        # Test the request a maximum of 10 times, otherwise raise an error.
        number_of_tests = 10
        for _ in range(number_of_tests):
            response = requests.get(url)
            assert response.status_code == 200
            # convert the bytes object to dict
            response = json.loads(response.content)
            # if the length of response['results'] != 1 we have to handle this case 
            # we throw an error assertion   
            assert len(response['results']) == 1
            result = response['results'][0] 
            if result['status'] == "COMPLETED":
                self.confirmation_url = result['confirmation_url']
                return self.confirmation_url

        raise NotImplementedError("This method must return confirmation_url")

    def patch_request(self):
        """
        Launch a patch request with the confirmed attribute set to True
        """
        if not self.__data_user:
            raise AuthenticationError('Please log in or create a user !!')

        # Prepare the url for the request
        url = "{}?c_auth_with_token={}".format(
            self.confirmation_url,
            self.__data_user['token']
        )

        data = {"confirmed": True}
        response = requests.patch(url, json=data)

        assert response.status_code == 200

        self.patch_response = json.loads(response.content)

        assert self.patch_response['confirmed']

        return self.patch_response
