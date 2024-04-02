params.input_file = 'notset'

workflow {
    convert_to_nwb(params.input_file)
    convert_to_nwb.out.view()
}

process convert_to_nwb {
    publishDir "s3://braingeneersdev/test/", mode: 'copy', overwrite: true
    container 'quay.io/ucsc_cgl/nwb-converter:latest'
    cpus '2'
    memory '8 GB'
    disk '2 GB'

    input:
        val input_file

    output:
        path "${input_file}.nwb"

    script:
        """
        run.py ${input_file}
        """
}
