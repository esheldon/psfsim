from __future__ import print_function
import os

from . import files

class ScriptWriter(dict):
    """
    class to write scripts and queue submission scripts

    parameters
    ----------
    run: string
        run identifier
    system: string
        Queue system.  Currently supports wq.
    njobs: int, optional
        Number of jobs to use.  Default is a jobs for
        each output file
    extra_commands: string
        Extra shell commands to run, e.g. for setting up
        your environment
    """

    def __init__(self, run, system, njobs=None, extra_commands=''):
        self['run'] = run
        self['extra_commands'] = extra_commands
        self['system'] = system

        self._load_config()
        self._makedirs()

        if njobs is not None:
            self['njobs'] = njobs
        else:
            self['njobs']=self.conf['output']['nfiles']

    def write_scripts(self):
        """
        write the basic bash scripts and queue submission scripts
        """
        for i in xrange(self['njobs']):
            if self['system']=='wq':
                self._write_wq(i)
            else:
                raise RuntimeError("bad system: '%s'" % self['system'])

            self._write_script(i)

    def _write_script(self, index):
        """
        write the basic bash script
        """
        self['jobnum'] = index + 1
        # temporary
        self['config_file'] = self['stars_config_file']

        text=_script_template % self

        script_fname=files.get_stars_script_file(self['run'], index)
        print("writing:",script_fname)
        with open(script_fname, 'w') as fobj:
            fobj.write(text)

    def _write_wq(self, index):
        """
        write the wq submission script
        """
        wq_fname=files.get_stars_wq_file(self['run'], index)

        nfmt=files.nfmt
        job_fmt = 'psfsim-stars-%s-'+nfmt
        self['job_name'] = job_fmt % (self['run'], index)
        self['logfile'] = files.get_stars_log_file(self['run'],index)
        self['script']=files.get_stars_script_file(self['run'], index)
        text = _wq_template  % self

        print("writing:",wq_fname)
        with open(wq_fname,'w') as fobj:
            fobj.write(text)

    def _makedirs(self):
        """
        make all the directories needed
        """
        script_dir = files.get_script_dir(self['run'])

        dirs=[script_dir]

        if self['system']=='wq':
            dirs += [files.get_wq_dir(self['run'])]

        for d in dirs:
            if not os.path.exists(d):
                try:
                    print("making dir:",d)
                    os.makedirs(d)
                except:
                    pass

    def _load_config(self):
        """
        load the galsim config and do some checks
        """
        self['stars_config_file']=files.get_stars_config_file(self['run'])

        self.conf = files.read_stars_config(self['run'])

        if self.conf['run'] != self['run']:
            mess="run on config is '%s' but should be '%s'"
            raise ValueError(mess % (self.conf['run'], self['run']))

_script_template = """#!/bin/bash
# set up environment before running this script

galsim -n %(njobs)d -j %(jobnum)d %(config_file)s
"""

_wq_template = """#!/bin/bash
command: |
    %(extra_commands)s

    logfile="%(logfile)s"
    tmp_logfile="$(basename $logfile)"
    tmp_logfile="$TMPDIR/$tmp_logfile"
    bash %(script)s &> "$tmp_logfile"

    mv -vf "$tmp_logfile" "$logfile"

job_name: "%(job_name)s"
"""
