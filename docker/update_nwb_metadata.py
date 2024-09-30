#!/usr/bin/env python
import argparse

from pynwb import NWBHDF5IO
from pynwb.file import Subject


metadata = {'electrode_group_description': 'V1 Maxwell Electrode Group',
            'electrodes_channel_name_description': 'Name (number) of the electrode channel',
            'electrode_name_description': 'Name (number) of the electrode',
            'subject': Subject(
                subject_id="001",
                age="P90D",
                description="mouse 5",
                species="Mus musculus",
                sex="M"
            ),
            'institution': 'UCSC',
            'experimenter': 'Tal Sharf',
            'keywords': ['ephys', 'mouse'],
            'experiment_description': 'Disease model for Parkinsons'}


def update_electrode_group_desc(nwbfile, desc):
    #  check_description - 'ElectrodeGroup' object at location '/general/extracellular_ephys/0'
    #       Message: Description ('no description') is a placeholder.
    if nwbfile.electrode_groups['0'].description.strip() == 'no description':
        del nwbfile.electrode_groups['0'].fields['description']
        setattr(nwbfile.electrode_groups['0'], 'description', desc)


def update_electrodes_channel_name(nwbfile, desc):
    #  check_description - 'VectorData' object with name 'channel_name'
    #        Message: Description ('no description') is a placeholder.
    if nwbfile.electrodes['channel_name'].fields['description'].strip() == 'no description':
        del nwbfile.electrodes['channel_name'].fields['description']
        setattr(nwbfile.electrodes['channel_name'], 'description', desc)


def update_electrode_name(nwbfile, desc):
    #  check_description - 'VectorData' object with name 'electrode'
    #        Message: Description ('no description') is a placeholder.
    if nwbfile.electrodes['electrode'].fields['description'].strip() == 'no description':
        del nwbfile.electrodes['electrode'].fields['description']
        setattr(nwbfile.electrodes['electrode'], 'description', desc)


def update_subject(nwbfile, subject):
    # check_subject_exists - 'NWBFile' object at location '/'
    #        Message: Subject is missing.
    if 'subject' in nwbfile.fields:
        del nwbfile.fields['subject']
    nwbfile.subject = subject


def update_institution(nwbfile, institute):
    # check_institution - 'NWBFile' object at location '/'
    #        Message: Metadata /general/institution is missing.
    if 'institution' in nwbfile.fields:
        del nwbfile.fields['institution']
    nwbfile.institution = institute


def update_experimenter(nwbfile, experimenter):
    # check_experimenter_exists - 'NWBFile' object at location '/'
    #        Message: Experimenter is missing.
    if 'experimenter' in nwbfile.fields:
        del nwbfile.fields['experimenter']
    nwbfile.experimenter = experimenter


def update_keywords(nwbfile, keywords):
    # check_keywords - 'NWBFile' object at location '/'
    #        Message: Metadata /general/keywords is missing.
    if 'keywords' in nwbfile.fields:
        del nwbfile.fields['keywords']
    nwbfile.keywords = keywords


def update_experiment_description(nwbfile, experiment_description):
    # check_experiment_description - 'NWBFile' object at location '/'
    #        Message: Experiment description is missing.
    if 'experiment_description' in nwbfile.fields:
        del nwbfile.fields['experiment_description']
    nwbfile.experiment_description = experiment_description


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename')
    parser.add_argument('output_filename')
    args = parser.parse_args()
    with NWBHDF5IO(args.input_filename, mode='r') as read_io:
        nwbfile = read_io.read()
        update_electrode_group_desc(nwbfile, desc=metadata['electrode_group_description'])
        update_electrodes_channel_name(nwbfile, desc=metadata['electrodes_channel_name_description'])
        update_electrode_name(nwbfile, desc=metadata['electrode_name_description'])
        update_subject(nwbfile, subject=metadata['subject'])
        update_institution(nwbfile, institute=metadata['institution'])
        update_experimenter(nwbfile, experimenter=metadata['experimenter'])
        update_keywords(nwbfile, keywords=metadata['keywords'])
        update_experiment_description(nwbfile, experiment_description=metadata['experiment_description'])
        nwbfile.set_modified()
        nwbfile.generate_new_id()

        with NWBHDF5IO(args.output_filename, mode='w') as export_io:
            export_io.export(src_io=read_io, nwbfile=nwbfile, write_args={'link_data': False})


if __name__ == '__main__':
    main()
