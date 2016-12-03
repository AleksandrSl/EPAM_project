# проверить отсортирован ли файл
# samtools view -H /path/to/my.bam
# проверить есть ли информация о рид группах
# samtools view -H /path/to/my.bam | grep '^@RG'
import sciluigi as sl
from itertools import zip_longest
from subprocess import run, CalledProcessError
from collections import OrderedDict
import utils
from glob import glob
from json import dump, load

class BQSR(sl.Task):

    tool_path = sl.Parameter()
    outp_path = sl.Parameter()
    working_dir = sl.Parameter()
    ref_fasta = sl.Parameter()
    dbsnp = sl.Parameter()
    indels = sl.Parameter()
    in_data = None

    def out_data(self):
        return sl.TargetInfo(self, self.outp_path + 'BQSR_res')

    def run(self):
        with utils.cd(self.working_dir):
            utils.mkdir_if_not_exist(self.outp_path)
            res = utils.deserialize(self.in_data().path, load)

            # Analyze patterns of covariation in the sequence dataset
            # TODO: Добавить индексацию файла dedup_reads_w...
            cmds = ['java -jar {tool_path} -T BaseRecalibrator ' \
                   '-R {ref_fasta} -I dedup_reads_w_readgroups.bam ' \
                   '-knownSites {dbsnp} ' \
                   '-knownSites {indels} ' \
                   '-o recal_data.table'.format(tool_path=self.tool_path,
                                                ref_fasta=self.ref_fasta,
                                                dbsnp=self.dbsnp,
                                                indels=self.indels),
            # Do a second pass to analyze covariation remaining after recalibration
            'java -jar {tool_path} -T BaseRecalibrator ' \
                   '-R {ref_fasta} -I dedup_reads_w_readgroups.bam ' \
                   '-knownSites {dbsnp} ' \
                   '-knownSites {indels} ' \
                   '-BQSR recal_data.table -o post_recal_data.table'.format(tool_path=self.tool_path,
                                                                            ref_fasta=self.ref_fasta,
                                                                            dbsnp=self.dbsnp,
                                                                            indels=self.indels),
            # Generate before/after plots
            'java -jar {tool_path} -T AnalyzeCovariates -R {ref_fasta} ' \
                   '-L chr20 -before recal_data.table ' \
                   '-after post_recal_data.table ' \
                   '-plots recalibration_plots.pdf'.format(tool_path=self.tool_path,
                                                           ref_fasta=self.ref_fasta),
            # Apply the recalibration to your sequence data
            'java -jar {tool_path} -T PrintReads -R {ref_fasta} ' \
                   '-I dedup_reads_w_readgroups.bam ' \
                   '-BQSR recal_data.table -o recal_reads.bam'.format(tool_path=self.tool_path,
                                                                      ref_fasta=self.ref_fasta)]
            for cmd in cmds[2:]:
                print('Command', cmd)
                try:
                    run(cmd, shell=True, check=True)
                except CalledProcessError:
                    print('i failed')
                    raise
                else:
                    utils.serialize(glob('*'), self.out_data().path, dump)

#java -jar GenomeAnalysisTK.jar -T HaplotypeCaller -R reference.fa -I preprocessed_reads.bam -L 20 --genotyping_mode DISCOVERY -stand_emit_conf 10 -stand_call_conf 30 -o raw_variants.vcf




