import luigi
import sciluigi as sl
from itertools import zip_longest
from subprocess import run, CalledProcessError
from collections import OrderedDict
import utils
from glob import glob
from json import dump, load

class TrimmoTaskWParameters(sl.Task):
    """
    Execute trimmomatic on fastq files
    """
    # Parameter
    in_data = None
    trimmo_parameters = None # OrderedDict
    adapters_path = sl.Parameter()
    tool_path = sl.Parameter()
    adapter = sl.Parameter()
    outp_path = sl.Parameter()

    def out_trimmo(self):
        outp_name = 'trimmed_seq'
        adapter_full_path = self.adapters_path + self.adapter
        self.default_trimmo_args = OrderedDict()
        args = ['SE', 'PE', '-basein', '-baseout', 'ILLUMINACLIP:', 'MAXINFO:', 'SLIDINGWINDOW:', 'LEADING:', 'CROP:',
                'TRAILING:', 'HEADCROP:', 'MINLEN:']
        vals = [None, True, None, None, adapter_full_path + ':2:30:10', None, None, 30, None, 30, 15, 20]
        # "leading": head_qual, "trailing": 30, "headcrop": 15}
        for arg, vals in zip_longest(args, vals):
            self.default_trimmo_args[arg] = vals

        # TODO move this constants to config file
        # print(self.default_trimmo_args)
        # print(self.tool_path)
        print(self.outp_path + 'trimmo_res.txt')
        return sl.TargetInfo(self, self.outp_path + 'trimmo_res.txt')

    def run(self):
        outp_full_path = self.outp_path + 'trimmo'
        print('!!!',self.in_data().path)
        fastqs = utils.deserialize(self.in_data().path, load)
        utils.mkdir_if_not_exist(self.outp_path)
        if not self.trimmo_parameters:
            self.trimmo_parameters = self.default_trimmo_args
        self.trimmo_parameters['-basein'] = fastqs[0]
        self.trimmo_parameters['-baseout'] = outp_full_path
        cmd = 'java -jar {tool_path} {args}'.format(tool_path=self.tool_path,
                                                    args=utils.make_args(self.trimmo_parameters))
        print('Command', cmd)
        try:
            run(cmd, shell=True, check=True)
        except CalledProcessError:
            print('i failed')
        else:
            utils.serialize(glob(self.outp_path + '*'), self.out_trimmo().path, dump)




###################################################################3
#    # ILLUMINACLIP:<fastaWithAdaptersEtc>:<seed mismatches>:<palindrome clip threshold>:<simple clip threshold>:<minAdapterLength>:<keepBothReads>
#    # MAXINFO:<targetLength>:<strictness>
#    # SLIDINGWINDOW:<windowSize>:<requiredQuality>
#    # LEADING:<quality>
#    # CROP:<length>
#    # TRAILING:<quality>
#    # HEADCROP: < length >
####################################################################
