params.bucket_slash_uuid = 'notset'

workflow {
    convert_to_nwb(params.bucket_slash_uuid)
    convert_to_nwb.out.view()
}

process convert_to_nwb {
    publishDir "s3://${bucket_slash_uuid}/", mode: 'copy', overwrite: true
    container 'quay.io/ucsc_cgl/nwb-converter:latest'
    cpus '2'
    memory '8 GB'
    disk '2 GB'

    input:
        path bucket_slash_uuid

    output:
        path "${bucket_slash_uuid}.nwb"

    script:
        """
        run.py ${bucket_slash_uuid}
        """
}
