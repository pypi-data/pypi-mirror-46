from metagenomi.tasks.taskbase import MgTask
from metagenomi.helpers import to_decimal
from metagenomi.helpers import to_int


class Mapping(MgTask):
    def __init__(self, mgid, **data):
        if not len(data):
            raise ValueError('Cannot initialize a mapping with no data')

        MgTask.__init__(self, mgid, **data)

        self.aligned_mapq_greaterequal_10 = to_int(self.d.get(
                                                'aligned_mapq_greaterequal_10',
                                                'None'))
        self.aligned_mapq_less_10 = to_int(self.d.get('aligned_mapq_less_10',
                                                   'None'))
        self.percent_pairs = to_decimal(self.d.get('percent_pairs', 'None'))
        self.reads_per_sec = to_int(self.d.get('reads_per_sec', 'None'))
        self.seed_size = to_int(self.d.get('seed_size', 'None'))
        self.time_in_aligner_seconds = to_int(self.d.get(
                                        'time_in_aligner_seconds', 'None'))

        self.too_short_or_too_many_nns = to_int(self.d.get(
                                            'too_short_or_too_many_nns',
                                            'None'))
        self.total_bases = to_int(self.d.get('total_bases', 'None'))
        self.total_reads = to_int(self.d.get('total_reads', 'None'))
        self.unaligned = to_int(self.d.get('unaligned', 'None'))
        self.paired = self.d.get('paired', True)
        self.reads_mapped = dict(self.d.get('reads_mapped', 'None'))

        self.reference = str(self.d.get('reference', 'None'))

        self.schema = {**self.schema, **{
            'aligned_mapq_greaterequal_10': {
                'required': True, 'type': 'integer'},
            'aligned_mapq_less_10': {'required': True, 'type': 'integer'},
            'percent_pairs': {'required': True, 'type': 'decimal'},
            'reads_per_sec': {'required': True, 'type': 'integer'},
            'seed_size': {'required': True, 'type': 'integer'},
            'time_in_aligner_seconds': {'required': True, 'type': 'integer'},
            'too_short_or_too_many_nns': {'required': True, 'type': 'integer'},
            'total_bases': {'required': True, 'type': 'integer'},
            'total_reads': {'required': True, 'type': 'integer'},
            'unaligned': {'required': True, 'type': 'integer'},
            'paired': {'required': True, 'type': 'boolean'},
            'reads_mapped': {
                'required': True, 'type': 'dict', 'schema': {
                    'fwd': {'type': 's3file'},
                    'rev': {'type': 's3file'},
                    'single': {'type': 's3file'}
                }
            },
            'reference': {'required': True, 'type': 's3file'}
        }}

        if self.check:
            self.validate()

    def write(self):
        '''
        Create new Mapping entry
        '''
        self._update(self.whoami(), self.to_dict(validate=True, clean=True))
