import sys
import arrow
import boto3

DOMAIN = 'ChestDayUserData'

def _db():
    return boto3.client('sdb')


def _attributes_to_dict(attributes):
    return {x['Name']: x['Value'] for x in attributes}


def get_timezone_difference(user):
    result = _db().get_attributes(
        DomainName=DOMAIN,
        ItemName=user,
        AttributeNames=['timezone_difference'],
        ConsistentRead=True,
    )

    if 'Attributes' in result and len(result['Attributes']) > 0:
        return _attributes_to_dict(result['Attributes'])['timezone_difference']
    else:
        return None


def create_table():
    _db().create_domain(
        DomainName=DOMAIN
    )


def set_timezone_offset(user, timezone_offset):

    timezone_difference = '+' if timezone_offset >= 0 else '-'
    timezone_difference += '{:02d}:00'.format(abs(timezone_offset))

    _db().put_attributes(
        DomainName=DOMAIN,
        ItemName=user,
        Attributes=[
            {
                'Name': 'timezone_difference',
                'Value': str(timezone_difference),
                'Replace': True
            }
        ]
    )
