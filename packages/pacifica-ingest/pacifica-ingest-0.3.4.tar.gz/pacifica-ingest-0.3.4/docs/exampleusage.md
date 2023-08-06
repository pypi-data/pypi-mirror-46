# Example Usage

The first thing to discuss when talking about interacting with the
ingest service is data format.

## Bundle Format

The bundle format is parsed using the [tarfile](https://docs.python.org/2/library/tarfile.html)
package from the Python standard library.

Both data and metadata are stored in a bundle. Metadata is stored in the
`metadata.txt` file (JSON format). Data is stored in the `data/` directory.

To display the contents of a bundle using the `tar` command:
```bash
tar -tf mybundle.tar
```

For example, the contents of `mybundle.tar` is:
```
data/mywork/project/project.doc
data/mywork/experiment/results.csv
data/mywork/experiment/results.doc
metadata.txt
```

## API Examples

The endpoints that define the ingest process are as follows. The assumption is that the installer
knows the IP address and port the WSGI service is listening on.

### Ingest (Single HTTP Request)

Post a bundle ([defined above](#bundle-format)) to the endpoint.

```
POST /ingest
... tar bundle as body ...
```

The response will be the job ID information as if you requested it directly.

```
{
  "job_id": 1234,
  "state": "OK",
  "task": "UPLOADING",
  "task_percent": "0.0",
  "updated": "2018-01-25 16:54:50",
  "created": "2018-01-25 16:54:50",
  "exception": ""
}
```

Failures that exist with this endpoint are during the course of uploading the bundle.
Sending data to this endpoint should consider long drawn out HTTP posts that maybe
longer than clients are used to handling.

### Move (Single HTTP Request)

Post a [metadata document](_static/move-md.json) to the endpoint.

```
POST /move
... content of move-md.json ...
```

The response will be the job ID information as if you requested it directly.

```
{
  "job_id": 1234,
  "state": "OK",
  "task": "UPLOADING",
  "task_percent": "0.0",
  "updated": "2018-01-25 16:54:50",
  "created": "2018-01-25 16:54:50",
  "exception": ""
}
```

### Get State for Job

Using the `job_id` field from the HTTP response from an ingest.

```
GET /get_state?job_id=1234
{
  "job_id": 1234,
  "state": "OK",
  "task": "ingest files",
  "task_percent": "0.0",
  "updated": "2018-01-25 17:00:32",
  "created": "2018-01-25 16:54:50",
  "exception": ""
}
```

As the bundle of data is being processed errors may occure, if that happens the following
will be returned. It is useful when consuming this endpoint to plan for failures. Consider
logging or showing a message visable to the user that shows the ingest failed.

```
GET /get_state?job_id=1234
{
  "job_id": 1234,
  "state": "FAILED",
  "task": "ingest files",
  "task_percent": "0.0",
  "updated": "2018-01-25 17:01:02",
  "created": "2018-01-25 16:54:50",
  "exception": "... some crazy python back trace ..."
}
```

# CLI Tools

There is an admin tool that consists of subcommands for manipulating ingest processes.

## Job Subcommand

The job subcommand allows administrators to directly manipulate the state of a job. Due
to complex computing environments some jobs may get "stuck" and get to a state where
they aren't failed and aren't progressing. This may happen for any number of reasons but
the solution is to manually fail the job.

```sh
IngestCMD job \
    --job-id 1234 \
    --state FAILED \
    --task 'ingest files' \
    --task-percent 0.0 \
    --exception 'Failed by adminstrator'
```
