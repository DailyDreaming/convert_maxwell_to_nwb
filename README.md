## Convert to NWB

Converts ephys files (currently only from the Maxwell format) to NWB in one easy to use docker container.

Takes any supported (local) file or list of files as arguments.

To run, mount the directory containing your input file path(s), and the output should appear in the same directory:

  docker run -v /home/quokka/data:/home/quokka/data quay.io/ucsc_cgl/nwb-converter:0.1 python3 /bin/run.py /home/quokka/data/your_maxwell_file.raw.h5
