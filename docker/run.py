#!/usr/bin/python3
"""
Takes any supported (local) file or list of files as arguments and converts to NWB format.

Output files are placed in /tmp/nwb/.

If run inside of a docker image, you'll need to mount this directory, for example:

  docker run -v /home/quokka/outputs:/tmp/nwb quay.io/ucsc_cgl/nwb-converter:latest input.raw.h5
"""
import os
import sys

from datetime import datetime
from dateutil import tz
from typing import List

from neuroconv.datainterfaces import MaxOneRecordingInterface


def convert_maxwell_to_nwb(src_local_path: str, dst_local_path: str) -> str:
    """Neuroconv only works locally, so this only accepts local file paths."""
    if not os.path.exists(src_local_path):
        raise FileNotFoundError(f'Local path does not exist: {src_local_path}')

    interface = MaxOneRecordingInterface(file_path=src_local_path, verbose=True)
    metadata = interface.get_metadata()
    metadata["NWBFile"].update(session_start_time=datetime.now(tz=tz.gettz("US/Pacific")))
    interface.run_conversion(nwbfile_path=dst_local_path, metadata=metadata)

    print(f'Successfully converted {src_local_path} to {dst_local_path}')
    return dst_local_path


def convert_to_nwb(path: str):
    """
    Converts any recognized (and implemented) ephys file format into NWB format.

    path: Any URI string representing a file (i.e. s3://file/path.txt, /home/user/dir/path.txt, etc.).
    dry_run: If True, this skips conversion, which typically takes hours, and only downloads the path URI
     from s3 and re-uploads it to s3 with a new name (if an s3 URI is used).
    """
    if path.endswith('.nwb'):
        print(f'Nothing to be done.  File "{path}" is already an NWB file.')
        return

    if path.endswith('.raw.h5'):
        convert_maxwell_to_nwb(path, f'{path}.nwb')
    else:
        raise NotImplementedError(f'Unsupported file type cannot be converted to NWB: {path}')


def main(paths: List[str]):
    # print(f'sys.argv: {sys.argv}')
    for path in paths:
        print(f'Converting Path to NWB: {path}')
        # path = os.path.abspath(path)
        convert_to_nwb(path)
        # print(f'Abspath: {path}')
        # with open(path, 'r') as f:
        #     x = f.read()
        # with open(f'{path}.nwb', 'w') as f:
        #     f.write(x)
    # with open(f'text.text.nwb', 'w') as f:
    #     f.write(str(sys.argv))


if __name__ == '__main__':
    main(sys.argv[1:])
