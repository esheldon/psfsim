# psfsim

Framework for running PSF simulations for testing psf modeling, interpolation,
and shear recovery.  Most people will use this library to access the files.

Any galsim config files with the proper naming scheme can be used, but we are
co-developing a set of scripts in the https://github.com/esheldon/psfsim_config
repository

Examples accessing output files.
--------------------------------

```python
# make sure the PSFSIM_DIR environment variable is set to the base directory
# e.g. at BNL we use
# PSFSIM_DIR=/gpfs/mnt/gpfs01/astro/workarea/esheldon/lensing/des-lensing/psfsim

import psfsim
from psfsim import files

# location of a star field image
run='v006'
index=8842
files.get_stars_file(run, index)
'/gpfs/mnt/gpfs01/astro/workarea/esheldon/lensing/des-lensing/psfsim/v006/output/psfsim-stars-v006-008842.fits'

# location of the truth catalog for the star field
files.get_stars_truth_file(run, index)
'/gpfs/mnt/gpfs01/astro/workarea/esheldon/lensing/des-lensing/psfsim/v006/output/psfsim-stars-truth-v006-008842.fits'
```

Examples running the sims
---------------------------

```bash
# write scripts for run v001, for the wq batch system

psfsim-make-scripts v001 wq

# You can also have some additional commands run.  For
# example, this sets up an anaconda environment

psfsim-make-scripts v001 wq --extra-commands="source activate psfsim"

# the above write scripts into $PSFSIM_DIR/$run/scripts

cd $PSFSIM_DIR/v001/scripts

# run a script
bash psfsim-stars-v001-0019.sh

# submit to the queue
wq sub -b psfsim-stars-v001-0019.yaml

# outputs are in $PSFSIM_DIR/$run/output

# the output file
ls $PSFSIM_DIR/v001/output/psfsim-stars-v001-0017.fits

# the log file
ls $PSFSIM_DIR/v001/output/psfsim-stars-v001-0017.log
```

Setup
-----

To find file paths, you need the PSFSIM_DIR environment variable set

To run the sims, you also need the PSFSIM_CONFIG_DIR environment variable set

Dependencies for running sims
-----------------------------

- galsim and all its dependencies
- galsim_extra https://github.com/esheldon/galsim_extra

Optional Dependencies
---------------------

- psfsim_config - this repo holds our official configuration files
