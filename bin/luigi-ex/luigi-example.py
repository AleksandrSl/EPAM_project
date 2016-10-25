#!/usr/bin/env python3
import luigi
import os,sys

sampleName='test'

class Task1(luigi.Task):

    # Example parameter for our task: a
    # date for which a report should be run
    samplename=luigi.Parameter()
    header=luigi.Parameter()

    def requires(self):
        """
        Which other Tasks need to be complete before
        this Task can start? Luigi will use this to
        compute the task dependency graph.
        """
        return []

    def output(self):
        """
        When this Task is complete, where will it produce output?
        Luigi will check whether this output (specified as a Target)
        exists to determine whether the Task needs to run at all.
        """
        self.r1 = luigi.LocalTarget('{}-R1.fq'.format(self.samplename))
        self.r2 = luigi.LocalTarget('{}-R2.fq'.format(self.samplename))
        return (self.r1, self.r2)

    def run(self):
        """
        How do I run this Task?
        Luigi will call this method if the Task needs to be run.
        """
        # We can do anything we want in here, from calling python
        # methods to running shell scripts to calling APIs
        print('Runnng Task1')
        print(self.output())
        
        with self.r1.open('w') as r1stream:
            with self.r2.open('w') as r2stream:
                for i in range(100):
                     print('Output data ',i)
                     r1stream.write(str(self.header)+'-readR1_'+str(i)+'\n')
                     r2stream.write(str(self.header)+'-readR2_'+str(i)+'\n')
        #r1.close()
        #r2.close()
            


class Task2(luigi.Task):

    # Example parameter for our task: a sample name
    samplename=luigi.Parameter()
    
    def requires(self):
        """
        Which other Tasks need to be complete before
        this Task can start? Luigi will use this to
        compute the task dependency graph.
        """
        return Task1(samplename=str(self.samplename)+'-mod', header='header')

    def output(self):
        """
        When this Task is complete, where will it produce output?
        Luigi will check whether this output (specified as a Target)
        exists to determine whether the Task needs to run at all.
        """
        return luigi.LocalTarget(self.samplename+'.bam')

    def run(self):
        """
        How do I run this Task?
        Luigi will call this method if the Task needs to be run.
        """
        # We can do anything we want in here, from calling python
        # methods to running shell scripts to calling APIs
        print('Running task2')
        print(self.samplename)
        

if __name__ == "__main__":
    #sys.path.append('/path/to/the/example_file.py')
    sys.path.append(os.path.dirname(__file__))
    luigi.run(['Task1','--module luigi-example --samplename testsample'])
