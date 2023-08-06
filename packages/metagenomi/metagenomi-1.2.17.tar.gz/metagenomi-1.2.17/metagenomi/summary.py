import os
import datetime

from boto3.dynamodb.conditions import Key, Attr
from metagenomi.db import (olddb, testdb, dbconn)
from metagenomi.helpers import (to_int, to_decimal, to_latlon)
from metagenomi.helpers import in_db
from metagenomi.tasks.mapping import Mapping
from metagenomi.tasks.assemblystats import AssemblyStats
from metagenomi.tasks.sampleinfo import SampleInfo
from metagenomi.tasks.prodigal import Prodigal
from metagenomi.tasks.nonpareil import Nonpareil
from metagenomi.tasks.cleaning import (QualityTrimming, AdapterRemoval, ContaminantRemoval)
from metagenomi.tasks.sequencinginfo import SequencingInfo

from metagenomi.models.assembly import Assembly
from metagenomi.models.sample import Sample
from metagenomi.models.sequencing import Sequencing
from metagenomi.project import MgProject

from metagenomi.helpers import download_file

import pandas as pd
import numpy as np


class MgSummary():
    def __init__(self, db=dbconn):
        self.db = db
        p = MgProject(db=self.db)
        p.load()

        # self.items = self.scan()

        self.assemblies = p.assemblies
        self.samples = p.samples
        self.sequencings = p.sequencings

    def count_objects(self, mgtype):
        if mgtype == 'assembly':
            items = self.assemblies
        elif mgtype == 'sample':
            items = self.samples
        elif mgtype == 'sequencing':
            items = self.sequencings

        count = {}
        for i in items:
            proj = i['mgproject']
            if proj in count:
                count[proj] = count[proj] + 1
            else:
                count[proj] = 1

        return count

    def count_proteins(self):
        count = {}
        for i in self.assemblies:
            proj = i.mgproject
            if i.prodigal is not None:
                if proj in count:
                    count[proj] = count[proj] + i.prodigal.proteins_predicted
                else:
                    count[proj] = i.prodigal.proteins_predicted
            else:
                if proj in count:
                    count[proj] = count[proj] + 0
                else:
                    count[proj] = 0
                # print(f'Prodigal has not yet been run on project {proj}')

        return count

    def count_assembled_bps(self):
        count = {}
        failed = []

        for i in self.assemblies:
            proj = i['mgproject']
            if 'AssemblyStats' in i:
                if proj in count:
                    count[proj] = count[proj] + i['AssemblyStats']['total_bps']
                else:
                    count[proj] = i['AssemblyStats']['total_bps']
            else:
                print(f'No assemblystats for {i["mgid"]}')

        return count

    def count_16s(self):
        count = {'NOT RUN': 0}
        for i in self.assemblies:
            proj = i['mgproject']
            if 'R16S' in i:
                if proj in count:
                    count[proj] = count[proj] + int(i['R16S']['num_16s'])
                else:
                    count[proj] = int(i['R16S']['num_16s'])
            else:
                count['NOT RUN'] = count['NOT RUN'] + 1
                print(i['mgid'])

        return count

    def count_16s_domains(self, as_df=True):
        count = {}
        for i in self.assemblies:
            proj = i['mgproject']
            if 'R16S' in i:
                if proj in count:
                    for k, v in i['R16S']['domains'].items():
                        if k in count[proj]:
                            count[proj][k] = count[proj][k] + v
                        else:
                            count[proj][k] = v

                else:
                    count[proj] = i['R16S']['domains']

            else:
                count['NOT RUN'] = count['NOT RUN'] + 1
                print(i['mgid'])

        if as_df:
            return pd.DataFrame(count)
        else:
            return count

    def count_bps(self, as_df=True):
        # 4 million bases per G zipped file size_mb
        # 4905611824 bp in 2710 MB size file
        # UPDATED: 1.8 million base pairs per 1 MB file size

        count = {}
        failed = []
        for i in self.sequencings:
            proj = i.mgproject
            if proj != 'PASO':
                # print(proj)
                if i.sequencing_info is not None:
                    # print('Seq info here')
                    if i.sequencing_info.bases > 0:
                        # print('bases!')
                        bases = i.sequencing_info.bases
                        if proj in count:
                            count[proj] = count[proj] + bases
                        else:
                            count[proj] = bases

                    else:
                        # print('size_mb here')
                        bases = 0
                        for k, v in i.sequencing_info.size_mb.items():
                            bases += v

                        bases = bases*1800000
                        # bases = bases*4000000
                        if proj in count:
                            count[proj] = count[proj] + bases
                        else:
                            count[proj] = bases

                    # else:
                    #     failed.append(i.mgid)
                else:
                    failed.append(i.mgid)

        return (count, failed)

    def assembly2sample(self, outfile):
        # for i in self.assemblies:
        #     seq = i['associated']['sequencing'][0]
        #     if seq != 'None':
        #         assembly2seq[seq] = i['mgid']

        with open(outfile, 'w') as f:
            f.write("sample\tassembly\n")
            for i in self.sequencing:
                samp = i['associated']['sample'][0]
                if 'assembly' in i['associated']:
                    assembly = i['associated']['assembly'][0]
                    f.write(f"{samp}\t{assembly}\n")



# def main():
#
#
# if __name__ == '__main__':
#     main()
