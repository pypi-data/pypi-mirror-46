"""
Documentation:
    https://esputnik.com/api/methods.html
"""

import json

from esputnik.esputnik import ESputnikAPIAdaptor

e_sputnik = ESputnikAPIAdaptor(
        user='name@gmail.com',
        password='secret'
    )


def test_version():
    return e_sputnik.version()


def test_send_message():
    data = [
        {
            'key': 'full_name',
            'value': 'John Dou'
        },
        {
            'key': 'email',
            'value': 'john@dou.com'
        },
        {
            'key': 'phone',
            'value': '+7777777777'
        }
    ]
    message_id = '100500'
    data = {
        'params': data,
        'recipients': ['john@dou.com', ],
    }
    return e_sputnik.message_send(message_id=message_id, data=data)


def test_smart_send():
    users = [
        {
            'full_name': 'John Dou',
            'email': 'john@dou.com',
            'phone': '+7777777777'
        },
        {
            'full_name': 'John Dou2',
            'email': 'john@dou2.com',
            'phone': '+7777777776'
        }
    ]
    message_id = '100500'
    recipients = []
    for user in users:
        recipients.append({'locator': user['email'], 'json_param': json.dumps(user)})
    data = {'recipients': recipients}
    return e_sputnik.message_smartsend(
        message_id=message_id,
        data=data
    )


def test_get_contacts():
    return e_sputnik.get_contacts()


def test_add_contact():
    data = {
        'first_name': 'John',
        'last_name': 'Dou',
        'channels': [
            {
                'type': 'email',
                'value': 'john@dou.com'
            }
        ],
        'groups': [
            {
                'name': 'Test group'
            }
        ],
        'address': {
            'region': 'Test region',
            'town': 'Test town',
            'address': 'Test address',
            'postcode': '123456',
        }
    }
    return e_sputnik.add_contact(data)


def test_update_contact():
    contact_id = '100500'
    data = {
        'first_name': 'Johny',
        'last_name': 'Dou',
        'channels': [
            {
                'type': 'email',
                'value': 'john@dou.com'
            }
        ],
        'address': {
            'region': 'New Test region',
            'town': 'New Test town',
            'address': 'New Test address',
            'postcode': '123456',
        }
    }
    return e_sputnik.update_contact(contact_id, data)


def test_delete_contact():
    contact_id = '100500'
    return e_sputnik.delete_contact(contact_id)


def test_get_contact():
    contact_id = '100500'
    return e_sputnik.get_contact(contact_id)


def test_contact_subscribe():
    data = {
        'contact': {
            'first_name': 'John',
            'last_name': 'Dou',
            'channels': [
                {
                    'type': 'email',
                    'value': 'john@dou.com'
                }
            ],
            'groups': [
                {
                    'name': 'Subscribers'
                }
            ],
            'address': {
                'region': 'Kyivska obl',
                'town': 'Kyiv',
                'address': '25, Main str.',
                'postcode': '78900',
            }
        },
        'groups': ['Subscribers', ]
    }
    return e_sputnik.contact_subscribe(data)


def test_unsubscribe_add():
    email = 'john@dou.com'
    return e_sputnik.emails_unsubscribed_add(email)


def test_unsubscribe_delete():
    email = 'john@dou.com'
    return e_sputnik.emails_unsubscribed_delete(email)


def test_message_status():
    message_id = '100500'
    return e_sputnik.message_status([message_id, ])
