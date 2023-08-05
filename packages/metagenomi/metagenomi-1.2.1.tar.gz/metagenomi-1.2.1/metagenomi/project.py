import time
from boto3.dynamodb.conditions import Key, Attr

from metagenomi.logger import logger
from metagenomi.db import dbconn
from metagenomi.models.assembly import Assembly
from metagenomi.models.sequencing import Sequencing
from metagenomi.models.sample import Sample
from metagenomi.base import MgObj
from decimal import Decimal


class MgProject:
    '''
    A representation of a lot of MgObjects
    '''

    def __init__(self, mgproject='ALL', db=dbconn, check=False, derive_associations=False, load=False):
        self.db = db
        self.check = check

        self.mgproject = mgproject
        self.sequencings = []
        self.assemblies = []
        self.samples = []
        self.association_map = {}
        self.items = None

        # if self.mgproject == 'ALL':
        #     self.items = self.query(self.mgproject)


        # start = time.time()
        # if self.mgproject == 'ALL':
            # print('Loading all via scan')
            # self.items = self.scan()
        # else:
            # self.items = self.query(self.mgproject)
        # end = time.time()
        # print(f'Queried {len(self.items)} in {end-start} seconds')
        # TODO: implement https://github.com/tqdm/tqdm

        if load:
            self.load_assemblies(check=check)
            self.load_sequencings(check=check)
            self.load_samples(check=check)

        if derive_associations:
            self.derive_associations()

    def load_assemblies(self, check=False):
        start = time.time()
        if self.mgproject == 'ALL':
            items = self.query('assembly', index='mgtype-s3path-index', key='mgtype')
        else:
            if self.items is None:
                self.items = self.query(self.mgproject)
            items = self.items

        assemblies = [i for i in items if i['mgtype'] == 'assembly']
        self.assemblies = [Assembly(db=self.db, check=self.check, **i)
                           for i in assemblies]
        end = time.time()
        m = f'Loaded {len(self.assemblies)} assemblies in {end-start} seconds'
        print(m)
        logger.info(m)

    def load_sequencings(self, check=False):
        start = time.time()
        if self.mgproject == 'ALL':
            items = self.query('sequencing', index='mgtype-s3path-index', key='mgtype')
        else:
            if self.items is None:
                self.items = self.query(self.mgproject)
            items = self.items

        sequencings = [i for i in items if i['mgtype'] == 'sequencing']
        self.sequencings = [Sequencing(db=self.db, check=self.check, **i)
                            for i in sequencings]
        end = time.time()
        m = f'Loaded {len(self.sequencings)} sequencings in {end-start} seconds'
        print(m)
        logger.info(m)

    def load_samples(self, check=False):
        start = time.time()
        if self.mgproject == 'ALL':
            print('querying all samples')
            items = self.query('sample', index='mgtype-s3path-index', key='mgtype')
        else:
            if self.items is None:
                self.items = self.query(self.mgproject)
            items = self.items

        self.samples = [Sample(db=self.db, check=self.check, **i)
                        for i in items if i['mgtype'] == 'sample']
        end = time.time()
        m = f'Loaded {len(self.samples)} samples in {end-start} seconds'
        print(m)
        logger.info(m)

    def query(self, value, index='mgproject-mgtype-index', key='mgproject'):
        """
        Queries the database given a value, index, and key.
        First selects the index, and then returns all items (in a pageinated
        fasion where Key(key).eq(value).
        """
        print('Querying the database')

        response = self.db.table.query(
            IndexName=index,
            KeyConditionExpression=Key(key).eq(value)
            )

        items = response['Items']
        while True:
            print(f'Loaded {len(items)} items')
            if response.get('LastEvaluatedKey'):
                response = self.db.table.query(
                    IndexName=index,
                    KeyConditionExpression=Key(key).eq(value),
                    ExclusiveStartKey=response['LastEvaluatedKey']
                    )
                items += response['Items']
            else:
                break

        return items

    def scan(self, filter_key=None, filter_value=None, comparison='equals'):
        """
        not currently in use
        """

        if filter_key and filter_value:
            if comparison == 'equals':
                filtering_exp = Key(filter_key).eq(filter_value)
            elif comparison == 'contains':
                filtering_exp = Attr(filter_key).contains(filter_value)

            response = self.db.table.scan(
                FilterExpression=filtering_exp)

            items = response['Items']
            while True:
                print(f'Loaded {len(items)} items')
                if response.get('LastEvaluatedKey'):
                    response = self.db.table.scan(
                        ExclusiveStartKey=response['LastEvaluatedKey'],
                        FilterExpression=filtering_exp
                        )
                    items += response['Items']
                else:
                    break

            return items

        else:
            response = self.db.table.scan()

            items = response['Items']
            while True:
                print(f'Loaded {len(items)} items')
                if response.get('LastEvaluatedKey'):
                    response = self.db.table.scan(
                        ExclusiveStartKey=response['LastEvaluatedKey']
                        )
                    items += response['Items']
                else:
                    break

            return items

    def derive_associations(self):
        '''

        '''
        for mgobj in self.assemblies + self.samples + self.sequencings:
            for type, mgobj_list in mgobj.associated.items():
                for o in mgobj_list:
                    if not o == 'None':
                        connection = self.find_mgobj(o)
                        if mgobj in self.association_map:
                            self.association_map[
                                mgobj
                                ] = self.association_map[mgobj] + [connection]
                        else:
                            self.association_map[mgobj] = [connection]

    def find_mgobj(self, o):
        '''
        Given the mgid of an object, return the instance of that object.
        TODO: Test speed of this function
        '''
        if isinstance(o, MgObj):
            return o

        for i in self.assemblies + self.samples + self.sequencings:
            if i.mgid == o:
                return i

        raise ValueError(f'Object {o} is not in this project')

    def delete(self, mgid):
        '''
        DOES NOT WORK YET
        '''
        pass
        # response = self.db.table.delete_item(
        #     Key={
        #         'mgid': mgid,
        #         },
        #     ConditionExpression="info.rating <= :val",
        #     ExpressionAttributeValues={
        #         ":val": Decimal(5)
        #         }
        #     )
        # return response
