#!/usr/bin/env python3
import os
import sys
import boto3

from functools import lru_cache
from datetime import datetime
from dateutil import tz
from typing import List
from shutil import copyfile

from neuroconv.datainterfaces import MaxOneRecordingInterface


@lru_cache()
def get_s3_client():
    return boto3.client('s3')


def download_s3_file(src_s3_path: str, dst_local_path: str) -> str:
    bucket, file_key = src_s3_path[len('s3:'):].lstrip('/').split('/', 1)
    dst_local_path = os.path.abspath(dst_local_path)
    s3 = get_s3_client()
    print(f'Now downloading "{src_s3_path}" to "{dst_local_path}"')
    s3.download_file(Bucket=bucket, Key=file_key, Filename=dst_local_path)
    print(f'Download successful: "{dst_local_path}"')
    return dst_local_path


def s3_file_exists(s3_path: str) -> bool:
    bucket, file_key = s3_path[len('s3:'):].lstrip('/').split('/', 1)
    s3 = get_s3_client()
    try:
        s3.head_object(Bucket=bucket, Key=file_key)
        return True
    except Exception as e:
        if 'An error occurred (404) when calling the HeadObject operation: Not Found' in str(e):
            return False
        raise


def upload_s3_file(src_local_path: str, dst_s3_path: str) -> str:
    bucket, file_key = dst_s3_path[len('s3:'):].lstrip('/').split('/', 1)
    src_local_path = os.path.abspath(src_local_path)
    s3 = get_s3_client()
    print(f'Now uploading "{src_local_path}" to "{dst_s3_path}"')
    s3.upload_file(Filename=src_local_path, Bucket=bucket, Key=file_key)
    print(f'Upload successful: "{dst_s3_path}"')
    return dst_s3_path


def convert_maxwell_to_nwb(src_local_path: str, dst_local_path: str, dry_run: bool = False) -> str:
    """Neuroconv only works locally, so this only accepts local file paths."""
    if not os.path.exists(src_local_path):
        raise FileNotFoundError(f'Local path does not exist: {src_local_path}')

    if dry_run:
        copyfile(src_local_path, dst_local_path)
    else:
        interface = MaxOneRecordingInterface(file_path=src_local_path, verbose=True)
        metadata = interface.get_metadata()
        metadata["NWBFile"].update(session_start_time=datetime.now(tz=tz.gettz("US/Pacific")))
        interface.run_conversion(nwbfile_path=dst_local_path, metadata=metadata)

    print(f'Successfully converted {src_local_path} to {dst_local_path}')
    return dst_local_path


def get_dst_s3_nwb_path(original_s3_path: str) -> str:
    """
    Given an input file path, replace the "/original/data/" closest to the end of the string
      with "/shared/" and append ".nwb" to the file name.

    Return None if "/original/data/" is not in the filepath.

    For example, if original_s3_path is "s3://a/b/c/original/data/filename.suffix",
      return "s3://a/b/c/shared/filename.suffix.nwb"
    """
    basename = os.path.basename(original_s3_path)
    if original_s3_path.endswith(f'/original/data/{basename}'):
        path_prefix = original_s3_path[:-len(f'/original/data/{basename}')]  # strip off the original data filepath suffix
        return f'{path_prefix}/shared/{basename}.nwb'
    return f'{original_s3_path}.nwb'


def convert_to_nwb(path: str, dry_run: bool = False):
    """
    Converts any recognized (and implemented) ephys file format into NWB format.

    path: Any URI string representing a file (i.e. s3://file/path.txt, /home/user/dir/path.txt, etc.).
    dry_run: If True, this skips conversion, which typically takes hours, and only downloads the path URI
     from s3 and re-uploads it to s3 with a new name (if an s3 URI is used).
    """
    if path.endswith('.nwb'):
        print(f'Nothing to be done.  File "{path}" is already an NWB file.')
        return

    if not path.endswith('.raw.h5'):
        raise NotImplementedError(f'Unsupported file type cannot be converted to NWB: {path}')

    if path.startswith('s3:'):
        dst_s3_path = get_dst_s3_nwb_path(path)
        if not dst_s3_path:
            print(f'Warning: non-canonical s3 path for Maxwell is missing "/original/data/".', file=sys.stderr)

        if s3_file_exists(dst_s3_path):
            print(f'NWB file at {dst_s3_path} already exists.  Skipping conversion of NWB file.', file=sys.stderr)
            return
        else:
            # download from s3; convert locally; re-upload to s3 with new path
            maxwell_local_path = download_s3_file(src_s3_path=path, dst_local_path=os.path.basename(path))
            nwb_local_path = convert_maxwell_to_nwb(maxwell_local_path, f'{maxwell_local_path}.nwb', dry_run=dry_run)
            upload_s3_file(src_local_path=nwb_local_path, dst_s3_path=dst_s3_path)
    else:
        # do a local conversion; do not upload to s3
        convert_maxwell_to_nwb(path, f'{path}.nwb', dry_run=dry_run)


def main(paths: List[str]):
    for path in paths:
        convert_to_nwb(path)


if __name__ == '__main__':
    main(sys.argv[1:])
