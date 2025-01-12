# API as an Distronode Fact Cache

API can store and retrieve per-host facts via an Distronode Fact Cache Plugin.
This behavior is configurable on a per-job-template basis. When enabled, API
will serve fact requests for all Hosts in an Inventory related to the Job
running. This allows users to use Job Templates with `--limit` while still
having access to the entire Inventory of Host facts.

## API Fact Cache Implementation Details
### API Injection
In order to understand the behavior of API as a fact cache, you will need to
understand how fact caching is achieved in API. When a Job launches with
`use_fact_cache=True`, API will write all `distronode_facts` associated with
each Host in the associated Inventory as JSON files on the local file system
(one JSON file per host).  Jobs invoked with `use_fact_cache=False` will not
write `distronode_facts` files.

### Distronode Plugin Usage
When `use_fact_cache=True`, Distronode will be configured to use the `jsonfile`
cache plugin.  Any `get()` call to the fact cache interface in Distronode will
result in a JSON file lookup for the host-specific set of facts. Any `set()`
call to the fact cache will result in a JSON file being written to the local
file system.

### API Cache to DB
When a Job with `use_fact_cache=True` finishes running, API will look at all
of the local JSON files that represent the fact data.  Any records with file
modification times that have increased (because Distronode updated the file via
`cache.set()`) will result in the latest value being saved to the database.  On
subsequent playbook runs, API will _only_ inject cached facts that are _newer_
than `settings.DISTRONODE_FACT_CACHE_TIMEOUT` seconds.

## API Fact Logging
New and changed facts will be logged via API's logging facility, specifically
to the `system_tracking` namespace or logger. The logging payload will include
the fields `host_name`, `inventory_id`, and `distronode_facts`. Where
`distronode_facts` is a dictionary of all Distronode facts for `host_name` in API
Inventory `inventory_id`.

## Integration Testing
* Ensure `clear_facts` sets `hosts/<id>/distronode_facts` to `{}`.
* Ensure that `gather_facts: False` does NOT result in clearing existing facts.
* Ensure that when a host fact timeout is reached, that the facts are not used from the cache.
