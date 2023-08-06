from os import path
import numpy as np


Datasets = {

    "mri_sino": ["sinograms", "mri_sino500.npz"],
    "mri_rec_astra": ["reconstructions", "mri_rec_astra.npz"],
    "mri_proj_astra": ["volumes", "mri_proj_astra.npz"],

}


def get_folder_path(foldername=""):
    _file_dir = path.dirname(path.realpath(__file__))
    package_dir = _file_dir
    return path.join(package_dir, foldername)



def get_data(dataset_name):
    if dataset_name not in Datasets:
        raise ValueError("Unknown dataset name %s" % dataset_name)
    folder_name, file_name = Datasets[dataset_name]
    fname = path.join(get_folder_path(folder_name), file_name)
    return np.load(fname)
