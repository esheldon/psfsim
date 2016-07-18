from __future__ import print_function
import os

#
# data directory structure
#

def get_basedir():
    """
    The base directory $PSFSIM_DIR.

    Runs are held under bad/run
    """
    if 'PSFSIM_DIR' not in os.environ:
        raise ValueError("PSFSIM_DIR environment variable is not set")

    return os.environ['PSFSIM_DIR']

def get_rundir(run):
    """
    The run directory $PSFSIM_DIR/run
    """
    bdir=get_basedir()
    return os.path.join(bdir, run)

def get_script_dir(run):
    """
    The script directory $PSFSIM_DIR/{run}/scripts
    """
    bdir=get_basedir()
    return os.path.join(bdir, run, 'scripts')

def get_output_dir(run):
    """
    The script directory $PSFSIM_DIR/{run}/output
    """
    bdir=get_basedir()
    return os.path.join(bdir, run, 'output')

def get_stars_file_pattern():
    """
    get the pattern for star files
    """
    return 'psfsim-stars-%s-%04d.fits'

def get_stars_file(run, index):
    """
    get the path to a stars file
    """
    dir=get_output_dir(run)
    pattern=get_stars_file_pattern(run)
    fname=pattern % (run, index)

    return os.path.join(dir, fname)

#
# configuration files
#

def get_config_dir():
    """
    get the value of the $PSFSIM_CONFIG_DIR environement variable
    """
    if 'PSFSIM_CONFIG_DIR' not in os.environ:
        raise ValueError("PSFSIM_CONFIG_DIR environment variable is not set")

    return os.environ['PSFSIM_CONFIG_DIR']

def get_stars_config_file(run):
    """
    the path to the stars config file
    """

    cdir=get_config_dir()
    fname='psfsim-stars-%s.yaml' % run
    return os.path.join(cdir, fname)

def read_stars_config(run):
    """
    read the yaml config file
    """
    import yaml

    fname= get_stars_config_file(run)
    return read_yaml(fname)

def get_gals_config_file(run):
    """
    the path to the gals config file
    """

    cdir=get_config_dir()
    fname='psfsim-gals-%s.yaml' % run
    return os.path.join(cdir, fname)

def read_gals_config(run):
    """
    read the yaml config file
    """
    import yaml
    fname = get_gals_config_file(run)
    return read_yaml(fname)

def read_yaml(fname):
    """
    wrapper to read yaml files
    """
    print("reading:",fname)
    with open(fname) as fobj:
        data=yaml.load( fobj )

    return data

