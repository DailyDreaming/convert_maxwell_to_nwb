## Convert to NWB Nextflow Workflow

This workflow converts various file formats into NWB format (currently raw maxwell is supported).

NOTE: This workflow is intended to be run with a Shared PVC on the [National Research Platform (NRP)](https://portal.nrp-nautilus.io)

### Running as a Nextflow Workflow triggered by an MQTT message

This workflow was written specifically to be run by the service here: https://github.com/braingeneers/mission_control/tree/main/nextflow

The MQTT message needs a bucket name slash UUID as an input (example: `"bucket_slash_uuid": "braingeneersdev/test"`), and will launch workflows for all listed valid convertible files found.

To do this, one must publish an MQTT message with the following JSON file contents:

```json
{"url": "https://github.com/DailyDreaming/convert_to_nwb", "bucket_slash_uuid": "braingeneersdev/test"}
```

If the file is called `nwb-params.json`, one can run/trigger this workflow via:

```bash
mosquitto_pub -h mqtt.braingeneers.gi.ucsc.edu \
              -t "workflow/start" \
              -u braingeneers \
              -P $(awk '/profile-key/ {print $NF}' ~/.aws/credentials) \
              -f nwb-params.json
```

4. Once complete, outputs should be deposited in the "/shared" prefix beside "/original/data" in the bucket slash uuid prefix:

```bash
(venv) quokka@qcore 01:34 PM ~/git/mission_control$ aws s3 ls s3://braingeneersdev/test/original/data/
    2024-04-02 12:26:18 1875693211 Or2_6M_raw_traces.raw.h5
    2024-04-02 12:30:40   55050547 debug_0p20_1.raw.h5

(venv) quokka@qcore 01:34 PM ~/git/mission_control$ aws s3 ls s3://braingeneersdev/test/shared/
    2024-04-12 07:06:19 2275921478 Or2_6M_raw_traces.raw.h5.nwb
    2024-04-16 12:37:44   58398636 debug_0p20_1.raw.h5.nwb
```

### More Detailed Instructions on Running Nextflow on the [National Research Platform (NRP)](https://portal.nrp-nautilus.io)

See: https://github.com/braingeneers/mission_control/tree/main/nextflow/infra
