# psfsim
PSF simulations for testing psf modeling, interpolation, and shear recovery

Examples
--------


```bash
# write scripts for run v001, for the wq batch system

psfsim-make-scripts v001 wq

# set up some environment

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

You need the PSFSIM_DIR and PSFSIM_CONFIG_DIR environment variables set

Dependencies
------------

- pyyaml

Optional Dependencies
---------------------

- psfsim_config - this repo holds some configuration files

to use the scripts you will need to have

- galsim
- galsim_extra
