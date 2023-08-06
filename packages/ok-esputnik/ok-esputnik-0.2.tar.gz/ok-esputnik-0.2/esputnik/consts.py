__all__ = (
    'MEDIA_CHANNEL_TYPES',
    'CONTACT_FIELDS_CHOICES',
    'UNIQUENESS_CONTACT_CHOICES'
)


MEDIA_CHANNEL_TYPES = (
    'email',
    'sms'
)

CONTACT_FIELDS_CHOICES = (
    'firstName',
    'lastName',
    'email',
    'sms',
    'address',
    'town',
    'region',
    'postcode'
)

UNIQUENESS_CONTACT_CHOICES = (
    'email',
    'sms',
    'email_or_sms',
    'id'
)
