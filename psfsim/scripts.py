from __future__ import print_function

from . import files

class ScriptWriter(dict):
    def __init__(self, run, extra_commands=''):
        self['run'] = run
        self['extra_commands'] = extra_commands

        self._load_config()
        self._makedirs()

        self['njobs']=self.conf['output']['nfiles']

    def write_scripts(self):

        for i in xrange(self['njobs']):
            self._write_script(i)
            self._write_wq(i)

    def _write_script(self, index):

        self['jobnum'] = index + 1
        # temporary
        self['config_file'] = self['stars_config_file'],

        text=_script_template % self

        script_fname=files.get_stars_script_file(self['run'], index)
        print("writing:",script_fname)
        with open(script_fname, 'w') as fobj:
            fobj.write(text)

    def _write_wq(self, index):
        wq_fname=files.get_wq_file(self['run'], index)

        self['job_name'] = 'psfsim-stars-%s-%04d.yaml' % (self['run'], index)
        self['logfile'] = files.get_stars_log_file(self['run'],index)
        self['script']=files.get_stars_script_file(self['run'], index)
        text = _wq_template  % self

        print("writing:",wq_fname)
        with open(wq_fname,'w') as fobj:
            fobj.write(text)

    def _makedirs(self):
        script_dir = files.get_script_dir(self['run'])

        dirs=[script_dir]

        for d in dirs:
            if not os.path.exists(d):
                try:
                    print("making dir:",d)
                    os.makedirs(d)
                except:
                    pass

    def _load_config(self):
        self['stars_config_file']=files.get_stars_config_file(self['run'])

        self.conf = files.read_stars_config(self['run'])

        if self.conf['run'] != self['run']:
            mess="run on config is '%s' but should be '%s'"
            raise ValueError(mess % (self.conf['run'], self['run']))

_script_template = """#!/bin/bash
# set up environment before running this script

galsim -n %(nfiles)d -j %(jobnum)d %(config_file)s
"""

_wq_template = """#!/bin/bash
command: |
    %(extra_commands)s

    logfile=%(logfile)s
    tmp_logfile=$(basename $logfile)
    tmp_logfile=$TMPDIR/tmp_logfile
    %(script)s &> $tmp_logfile

    mv -vf $tmp_logfile $logfile

job_name: %(job_name)
"""
