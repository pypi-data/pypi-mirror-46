import warnings

from abc import ABCMeta

from boto3.dynamodb.conditions import Key

from metagenomi.base import MgObj
from metagenomi.logger import logger
from metagenomi.helpers import get_time


class MgModel(MgObj):
    '''
    MgModel - base class for all models
    '''
    __metaclass__ = ABCMeta

    def __init__(self, mgid, **data):
        MgObj.__init__(self, mgid, **data)

        # If data not passed, object is loaded in the MgObj base class
        self.associated = self.d.get('associated', {})

        if 'created' in self.d:
            self.created = self.d['created']
        else:
            self.created = get_time()

        if 'mgproject' in self.d:
            self.mgproject = self.d['mgproject'].upper()
        else:
            self.mgproject = self.mgid[:4].upper()

        self.alt_id = self.d.get('alt_id')

        self.schema = {
            **self.schema, **{
                'alt_id': {'type': 'string', 'required': False, 'regex': "^[a-zA-Z0-9]*$"},
                'mgtype': {'type': 'string', 'required': True,
                           'allowed': ['sequencing', 'assembly', 'sample']},
                'associated': {'type': 'dict', 'required': True, 'schema': {
                    'sequencing': {'type': 'list', 'schema': {'type': 'mgid'}},
                    'assembly':  {'type': 'list', 'schema': {'type': 'mgid'}},
                    'sample':  {'type': 'list', 'schema': {'type': 'mgid'}},
                    }
                },
                'created': {'type': 'datestring', 'required': True},
                'mgproject': {'type': 'string', 'required': True,
                              'maxlength': 4, 'minlength': 4}
            }
        }

    def update_alt_id(self, new_alt_id, write=True):
        if self.unique_altid(new_alt_id):
            self.alt_id = new_alt_id
            if write:
                if self.validate():
                    self.update('alt_id', new_alt_id)
        else:
            msg = f'{new_alt_id} is already in DB - cannot re-write'
            logger.debug(msg)
            raise ValueError(msg)

    def unique_mgid(self, mgid=None):
        if mgid is None:
            mgid = self.mgid

        response = self.db.table.query(
            KeyConditionExpression=Key('mgid').eq(self.mgid))

        if len(response['Items']) < 1:
            return True
        return False

    def unique_altid(self, alt_id=None):
        if alt_id is None:
            alt_id = self.alt_id

        if alt_id is None:
            return True

        response = self.db.table.query(
            IndexName='alt_id-mgproject-index',
            KeyConditionExpression=Key('alt_id').eq(alt_id))

        if len(response['Items']) < 1:
            return True
        return False

    def write(self, force=False, dryrun=False):
        '''
        Write this object to the database - over-ridden in other derived
        classes when needed
        '''
        unique_altid = self.unique_altid()
        unique_mgid = self.unique_mgid()

        d = self.to_dict(validate=True, clean=True)

        # Add it back in at the appropriate spot
        d['mgid'] = self.mgid

        if dryrun:
            # TODO: improve printing here
            print('--- dry run ----')
            print(f'Would write to {self.db.table}')
            print(d)
            return

        if (unique_altid and unique_mgid) or force:
            response = self.db.table.put_item(
                Item=d
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                logger.info(f'Wrote {response} to db')
            else:
                raise ValueError('Response returned an HTTPStatusCode other than 200')

        else:
            # TODO: Does this capture all cases?
            msg = ''
            if not unique_altid:
                msg += f'{self.alt_id} is already in DB - cannot re-write'
            if not unique_mgid:
                msg += f'\n{self.mgid} is already in DB - cannot re-write'

            logger.debug(msg)
            raise ValueError(msg)

    def update(self, key, value, dryrun=False):
        '''
        TODO: VALIDATION???

        '''

        if dryrun:
            print('Dry run')
            print(f'Would update {key} to {value}')
            return

        else:
            response = self.db.table.update_item(
                                Key={
                                    'mgid': self.mgid
                                },
                                UpdateExpression=f"set {key} = :r",
                                ExpressionAttributeValues={
                                    ':r': value
                                },
                                ReturnValues="UPDATED_NEW"
                            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('update successful')
            else:
                # TODO: wrap this into the logger??
                print(response)
                raise ValueError('Something went wrong with the update request')

            return response
