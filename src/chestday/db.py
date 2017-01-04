import sys
import arrow
import boto3

DOMAIN = 'ChestDayUserData'

def _db():
    return boto3.client('sdb')


def _attributes_to_dict(attributes):
    return {x['Name']: x['Value'] for x in attributes}


def get_timezone_offset(user):
    result = _db().get_attributes(
        DomainName=DOMAIN,
        ItemName=user,
        AttributeNames=['timezone_offset']
    )

    if 'Attributes' in result and len(result['Attributes']) > 0:
        return int(_attributes_to_dict(result['Attributes'])['timezone_offset'])
    else:
        return None


def create_table():
    _db().create_domain(
        DomainName=DOMAIN
    )


def set_timezone_offset(user, timezone_offset):
    _db().put_attributes(
        DomainName=DOMAIN,
        ItemName=user,
        Attributes=[
            {
                'Name': 'timezone_offset',
                'Value': str(timezone_offset),
                'Replace': True
            }
        ]
    )
