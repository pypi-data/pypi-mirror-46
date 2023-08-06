import urllib
import tarfile
import shutil
import pdb
import os
from tqdm import tqdm
import numpy as np
from astropy.table import vstack, Table, Column


def get_model(model_grid_name):
    if model_grid_name == 'Oss-Orich-aringer':
        url_csv = ''
        url_fits = ''

    elif model_grid_name == 'Oss-Orich-bb':
        url = ''
        url_fits = ''

    elif model_grid_name == 'Zubko-Crich-aringer':
        url_csv = ''
        url_fits = ''

    elif model_grid_name == 'Zubko-Crich-bb':
        url_csv = ''
        url_fits = ''

    elif model_grid_name == 'arnold-palmer':
        url_csv = ''
        url_fits = ''

    elif model_grid_name == 'big-grains':
        url_csv = ''
        url_fits = ''

    elif model_grid_name == 'corundum-20':
        url_csv = ''
        url_fits = ''

    elif model_grid_name == 'fifth-iron':
        url_csv = ''
        url_fits = ''

    elif model_grid_name == 'one-fifth-carbon':
        url_csv = ''
        url_fits = ''

    else:
        raise ValueError(
            'ERROR: Model name not an option. \nCurrent built-in options: \n \t Zubko-Crich-aringer \n \t Oss-Orich-bb \n \t Oss-Orich-aringer \n \t Crystalline-20-bb \n \t corundum-20-bb \n \t arnold-palmer \n \t big-grains \n \t fifth-iron \n \t one-fifth-carbon')

    #\n Padova options: J400, J1000, H11, R12, R13'

    # Download files
    print("Downloading")
    urllib.request.urlretrieve(url_csv, model_grid_name+'_outputs.csv')
    urllib.request.urlretrieve(url_fits, model_grid_name+'_models.fits')
    print("Download Complete!")

