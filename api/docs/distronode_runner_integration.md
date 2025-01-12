## Distronode Runner Integration Overview

Much of the code in API around distronode and `distronode-playbook` invocation has been removed and put into the project `distronode-runner`. API now calls out to `distronode-runner` to invoke distronode and `distronode-playbook`.

### Lifecycle

In API, a task of a certain job type is kicked off (_i.e._, RunJob, RunProjectUpdate, RunInventoryUpdate, etc.) in `api/main/tasks/jobs.py`. A temp directory is built to house `distronode-runner` parameters (_i.e._, `envvars`, `cmdline`, `extravars`, etc.). The `temp` directory is filled with the various concepts in API (_i.e._, `ssh` keys, `extra vars`, etc.). The code then builds a set of parameters to be passed to the `distronode-runner` Python module interface, `distronode-runner.interface.run()`. This is where API passes control to `distronode-runner`. Feedback is gathered by API via callbacks and handlers passed in.

The callbacks and handlers are:
* `event_handler`: Called each time a new event is created in `distronode-runner`. API will dispatch the event to `redis` to be processed on the other end by the callback receiver.
* `cancel_callback`: Called periodically by `distronode-runner`; this is so that API can inform `distronode-runner` if the job should be canceled or not. Only applies for system jobs now, and other jobs are canceled via receptor.
* `finished_callback`: Called once by `distronode-runner` to denote that the process that was asked to run is finished. API will construct the special control event, `EOF`, with the associated total number of events that it observed.
* `status_handler`: Called by `distronode-runner` as the process transitions state internally. API uses the `starting` status to know that `distronode-runner` has made all of its decisions around the process that it will launch. API gathers and associates these decisions with the Job for historical observation.

### Debugging

If you want to debug `distronode-runner`, then set `API_CLEANUP_PATHS=False`, run a job, observe the job's `API_PRIVATE_DATA_DIR` property, and go the node where the job was executed and inspect that directory.

If you want to debug the process that `distronode-runner` invoked (_i.e._, Distronode or `distronode-playbook`), then observe the Job's `job_env`, `job_cwd`, and `job_args` parameters.
