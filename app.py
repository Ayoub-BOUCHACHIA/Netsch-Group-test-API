import os
from utils import ConcreteDatastore

if __name__ == "__main__":

    data_registration = {
        "email": os.environ.get('MY_EMAIL'),
        "password1": os.environ.get('MY_PASSWORD_1'),
        "password2": os.environ.get('MY_PASSWORD_2'),
    }

    concreteDatastore = ConcreteDatastore()
    concreteDatastore.create_user(data_registration)
    concreteDatastore.login(
        data_registration['email'],
        data_registration['password1']
    )
    confirmation_url = concreteDatastore.get_confirmation_url()
    patch_response = concreteDatastore.patch_request()
    print(concreteDatastore)
    """
    email : bouchachiaayoub7@gmail.com
    first name :
    last name :
    confirmation url : https://hire-game.netsach.dev:443/api/v1.1/job-application-confirmation-request/a8449fcb-c593-4f98-801a-5181360cdcf4/
    patch response : {
        'confirmed': True,
        'job_application_request': '26986321-c7f5-44a4-9808-5f5fe6f482d1', 
        'uid': 'a8449fcb-c593-4f98-801a-5181360cdcf4', 
        'modification_date': '2023-08-18T10:23:27Z',
        'creation_date': '2023-08-18T10:23:26Z', 
        'public': False, 
        'url': 'https://hire-game.netsach.dev/api/v1.1/job-application-confirmation-request/a8449fcb-c593-4f98-801a-5181360cdcf4/', 
        'verbose_name': '<JobApplicationConfirmationRequest a8449fcb-c593-4f98-801a-5181360cdcf4>', 
        'created_by': None, 
        'can_admin_users': ['441326dc-4498-4aad-a39f-833d3b85047e'], 
        'can_view_users': [], 
        'can_admin_groups': [], 
        'can_view_groups': [], 
        'scopes': None, 
        'job_application_request_uid': '26986321-c7f5-44a4-9808-5f5fe6f482d1'
    }
    """
