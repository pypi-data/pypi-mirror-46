import json
from typing import Dict, List, Union
from six import string_types

from esputnik.client import ESputnikAPIClient
from esputnik.exceptions import IncorrectDataError
from esputnik.templates import (
    prepare_contact,
    prepare_contact_subscribe,
    prepare_contacts,
    prepare_contact_search,
    prepare_contact_upload,
    prepare_event,
    prepare_send_email,
    prepare_smartsend_email,
    prepare_email,
    prepare_sms,
    prepare_viber_message
)

__all__ = (
    'ESputnikAPIAdaptor',
)


def _prepare_emails(value) -> List:
    if not value:
        raise IncorrectDataError(
            code='emails',
            message='You must provide some emails.'
        )
    if isinstance(value, list):
        return value
    elif isinstance(value, string_types):
        return [value]
    return list(value)


class ESputnikAPIAdaptor:
    """
    Base class that should be inherited by each class that has to work
    the API.

    Attributes:
        api_client (APIClient): APIClient instance to work with the API.
        api_client_class (APIClient): APIClient default class to use
            when no api_client passed on initialization stage.
    """
    api_client_class = ESputnikAPIClient

    def __init__(
            self,
            user: str,
            password: str,
            host: str = 'https://esputnik.com/api/',
            version: int = 1,
            *args,
            **kwargs
    ) -> None:
        """
        Initializes new api adaptor instance to use in classes that
        work with API.

        Args:
            api_client (None, optional): Custom APIClient instance, if
                you need to pass special params or even your own class.
        """
        self.api_client = self.__class__.api_client_class(
            api_user=user,
            api_password=password,
            host=host,
            version=version
        )

        super().__init__(*args, **kwargs)

    def version(self):
        """
        Get protocol version.
        """
        return self.api_client.get(
            'version'
        )

    def account_info(self):
        """
        Get current account info.
        """
        return self.api_client.get(
            'account/info'
        )

    def addressbooks(self):
        """
        Get catalog list.
        The catalog contains the list of additional fields
        for contacts that are available in your organisation.
        """
        return self.api_client.get(
            'addressbooks'
        )

    def balance(self):
        """
        Get organisation balance.
        """
        return self.api_client.get(
            'balance'
        )

    def add_contact(self, data: Dict):
        """
        Add contact.

        Args:
            data (Dict): dict of data to send
        """
        data = json.dumps(prepare_contact(data))
        return self.api_client.post(
            'contact',
            data
        )

    def update_contact(self, contact_id: str, data: Dict):
        """
        Update contact.

        Type of method: PUT.

        Args:
            contact_id (str): id of contact in your esputnik database
            data (Dict): dict of data to send
        """
        data = json.dumps(prepare_contact(data))
        return self.api_client.put(
            f'contact/{contact_id}',
            data
        )

    def delete_contact(self, contact_id: str):
        """
        Delete contact.

        Type of method: DELETE.

        Args:
            contact_id (str): id of contact in your esputnik database
        """
        return self.api_client.delete(
            f'contact/{contact_id}'
        )

    def get_contact(self, contact_id: str):
        """
        Get contact.

        Type of method: GET.

        Args:
            contact_id (str): id of contact in your esputnik database
        """
        return self.api_client.get(
            f'contact/{contact_id}'
        )

    def contact_subscribe(self, data: Dict):
        """
        Subscribe contact.
        Used for subscription forms integration.
        If contact does not exists - it will be created with not confirmed email.
        If contact exists - it will be updated.

        Type of method: POST.

        Args:
            data (Dict): dict of data to send
        """
        data = json.dumps(prepare_contact_subscribe(data))
        return self.api_client.post(
            'contact/subscribe',
            data
        )

    def add_contacts(self, data: Dict):
        """
        Add/update contacts.
        Existing contacts will be updated, new contacts will be added.

        Type of method: POST.

        Args:
            data (Dict): dict of data to send
        """
        data = json.dumps(prepare_contacts(data))
        return self.api_client.post(
            'contacts',
            data
        )

    def get_contacts(self, data: Dict = None):
        """
        Search contacts.
        The method returns max 500 results.
        There are total amount of contacts in TotalCount header.

        Type of method: GET.
        """
        if data:
            data = prepare_contact_search(data)
        return self.api_client.get(
            'contacts',
            data
        )

    def contacts_upload(self, data: Dict):
        """
        Add/update contacts from external file.
        Existing contacts will be updated, new contacts will be created.

        Type of method: POST.

        Args:
            data (Dict): dict of data to send
        """
        data = json.dumps(prepare_contact_upload(data))
        return self.api_client.post(
            'contacts/upload',
            data
        )

    def emails_unsubscribed_add(self, emails: Union[List, str]):
        """
        Add emails to unsubscribed list (unsubscribe emails).

        Type of method: POST.

        Args:
            emails (List): list of emails
        """
        data = json.dumps({
            "emails": _prepare_emails(emails)
        })
        return self.api_client.post(
            'emails/unsubscribed/add',
            data
        )

    def emails_unsubscribed_delete(self, emails: Union[List, str]):
        """
        Remove emails from unsubscribed list.

        Type of method: POST.

        Args:
            emails (List): list of emails
        """
        data = json.dumps({
            "emails": _prepare_emails(emails)
        })
        return self.api_client.post(
            'emails/unsubscribed/delete',
            data
        )

    def event(self, data: Dict):
        """
        Generate event.

        Type of method: POST.

        Args:
            data (Dict): dict of data to send
        """
        data = json.dumps(prepare_event(data))
        return self.api_client.post(
            'event',
            data
        )

    def group_contacts(self, group_id):
        """
        Get contacts from segment.

        Type of method: GET.

        Args:
            group_id: id of group in your esputnik database
        """
        return self.api_client.get(
            f'group/{group_id}/contacts'
        )

    def group_contacts_detach(self, group_id):
        """
        Delete all contacts from static segment.

        Type of method: POST.

        Args:
            group_id: id of group in your esputnik database
        """
        return self.api_client.post(
            f'group/{group_id}/contacts/detach'
        )

    def groups(self):
        """
        Get segments.

        Type of method: GET.
        """
        return self.api_client.get(
            'groups'
        )

    def message_send(self, message_id: str, data: Dict):
        """
        Dispatch start of the created message. Message can be parametrized additionally.

        Type of method: POST.

        Args:
            message_id (str): if of message in your esputnik database
            data (Dict): dict of data to send
        """
        if data.get('recipients') is None and data.get('group_id') is None:
            raise IncorrectDataError(
                code='message_send',
                message='You mast provide \'recipients\' or \'group_id\'.'
            )
        data = json.dumps(prepare_send_email(data))
        return self.api_client.post(
            f'message/{message_id}/send',
            data
        )

    def message_smartsend(self, message_id: str, data: Dict):
        """
        Sending prepared message to one or many contacts.
        The message can be parametrized for each contact separately.

        Args:
            message_id (str): unique id of the message in your esputnik database
            data (Dict): dict of data to send
        """
        data = json.dumps(prepare_smartsend_email(data))
        return self.api_client.post(
            f'message/{message_id}/smartsend',
            data
        )

    def message_email(self, data: Dict):
        """
        Send email message. If contact with such email address is not exist it will be created.

        Args:
            data (Dict): dict of data to send
        """
        data = json.dumps(prepare_email(data))
        return self.api_client.post(
            'message/email',
            data
        )

    def message_sms(self, data: Dict):
        """
        Send SMS message. If contact with such phone number is not exist it will be created.

        Type of method: POST.
        """
        data = json.dumps(prepare_sms(data))
        return self.api_client.post(
            'message/sms',
            data
        )

    def message_status(self, ids: List):
        """
        Get status of a single message.

        Type of method: GET.

        Args:
            ids (List): list of ids to check statuses
        """
        data = {
            'ids': ids or []
        }
        return self.api_client.get(
            'message/status',
            data
        )

    def message_viber(self, data: Dict):
        """
        Send VIBER message. If contact with such phone number is not exist it will be created.

        Type of method:
        POST.

        Args:
            data (Dict): dict of data to send
        """
        data = json.dumps(prepare_viber_message(data))
        return self.api_client.post(
            'message/viber',
            data
        )
