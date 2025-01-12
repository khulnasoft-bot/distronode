import os
from django.db import connection

from insights_analytics_collector import CsvFileSplitter, register
import galaxy_ng.app.metrics_collection.common_data as data


@register("config", "1.0", description="General platform configuration.", config=True)
def config(since, **kwargs):
    cfg = data.config()

    # just for compatibility, remove when Wisdom team is aware of that
    license_info = {}
    compatibility_csv = {
        "license_type": license_info.get("license_type", "UNLICENSED"),
        "free_instances": license_info.get("free_instances", 0),
        "total_licensed_instances": license_info.get("instance_count", 0),
        "license_expiry": license_info.get("time_remaining", 0),
        "external_logger_enabled": "todo",
        "external_logger_type": "todo",
        "logging_aggregators": ["todo"],
        "pendo_tracking": "todo"
    }
    return cfg | compatibility_csv


@register("instance_info", "1.0", description="Node information", config=True)
def instance_info(since, **kwargs):
    return data.instance_info()


@register("distronode_collection_table", "1.0", format="csv", description="Data on distronode_collection")
def distronode_collection_table(since, full_path, until, **kwargs):
    source_query = """
        COPY (
            SELECT "distronode_collection"."pulp_id",
                   "distronode_collection"."pulp_created",
                   "distronode_collection"."pulp_last_updated",
                   "distronode_collection"."namespace",
                   "distronode_collection"."name"
            FROM "distronode_collection"
        )
        TO STDOUT WITH CSV HEADER
    """

    return _simple_csv(full_path, "distronode_collection", source_query)


@register(
    "distronode_collectionversion_table",
    "1.0",
    format="csv",
    description="Data on distronode_collectionversion",
)
def distronode_collectionversion_table(since, full_path, until, **kwargs):
    source_query = """COPY (
            SELECT "distronode_collectionversion"."content_ptr_id",
                   "core_content"."pulp_created",
                   "core_content"."pulp_last_updated",
                   "distronode_collectionversion"."collection_id",
                   "distronode_collectionversion"."contents",
                   "distronode_collectionversion"."dependencies",
                   "distronode_collectionversion"."description",
                   "distronode_collectionversion"."license",
                   "distronode_collectionversion"."version",
                   "distronode_collectionversion"."requires_distronode",
                   "distronode_collectionversion"."is_highest",
                   "distronode_collectionversion_tags"."tag_id"
            FROM "distronode_collectionversion"
            INNER JOIN "core_content" ON (
                "distronode_collectionversion"."content_ptr_id" = "core_content"."pulp_id"
                )
            LEFT OUTER JOIN "distronode_collectionversion_tags" ON (
                "distronode_collectionversion"."content_ptr_id" =
                "distronode_collectionversion_tags"."collectionversion_id"
                )
        ) TO STDOUT WITH CSV HEADER
    """
    return _simple_csv(full_path, "distronode_collectionversion", source_query)


@register(
    "distronode_collectionversionsignature_table",
    "1.0",
    format="csv",
    description="Data on distronode_collectionversionsignature",
)
def distronode_collectionversionsignature_table(since, full_path, until, **kwargs):
    # currently no rows in the table, so no objects to base a query off
    source_query = """COPY (
            SELECT * FROM distronode_collectionversionsignature
        ) TO STDOUT WITH CSV HEADER
    """
    return _simple_csv(full_path, "distronode_collectionversionsignature", source_query)


@register(
    "distronode_collectionimport_table",
    "1.0",
    format="csv",
    description="Data on distronode_collectionimport",
)
def distronode_collectionimport_table(since, full_path, until, **kwargs):
    # currently no rows in the table, so no objects to base a query off
    source_query = """COPY (
            SELECT * FROM distronode_collectionimport
        ) TO STDOUT WITH CSV HEADER
    """
    return _simple_csv(full_path, "distronode_collectionimport", source_query)


# Does not exist
# @register(
#     "distronode_collectionstats_table",
#     "1.0",
#     format="csv",
#     description="Data on distronode_collectionstats",
# )
# def distronode_collectionstats_table(since, full_path, until, **kwargs):
#     pprint.pprint("distronode_collectionstats_table")
#     source_query = """COPY (SELECT * from distronode_collectionstats) TO STDOUT WITH CSV HEADER"""
#     return _simple_csv(full_path, "distronode_collectionimport", source_query)


@register(
    "container_containerrepository_table",
    "1.0",
    format="csv",
    description="Data on container_containerrepository",
)
def container_containerrepository_table(since, full_path, until, **kwargs):
    # currently no rows in the table, so no objects to base a query off
    source_query = """COPY (
            SELECT * FROM container_containerrepository
        ) TO STDOUT WITH CSV HEADER
    """
    return _simple_csv(full_path, "container_containerrepository", source_query)


@register(
    "container_containerremote_table",
    "1.0",
    format="csv",
    description="Data on container_containerremote",
)
def container_containerremote_table(since, full_path, until, **kwargs):
    # currently no rows in the table, so no objects to base a query off
    source_query = """COPY (
            SELECT * FROM container_containerremote
        ) TO STDOUT WITH CSV HEADER
    """
    return _simple_csv(full_path, "container_containerremote", source_query)


@register("container_tag_table", "1.0", format="csv", description="Data on container_tag")
def container_tag_table(since, full_path, until, **kwargs):
    # currently no rows in the table, so no objects to base a query off
    source_query = """COPY (
            SELECT * FROM container_tag
        ) TO STDOUT WITH CSV HEADER
    """
    return _simple_csv(full_path, "container_tag", source_query)


@register(
    "galaxy_legacynamespace", "1.0", format="csv", description="Data on galaxy_legacynamespace"
)
def galaxy_legacynamespace_table(since, full_path, until, **kwargs):
    source_query = """COPY (SELECT
            id, created, modified, name, company, avatar_url, description, namespace_id
            FROM galaxy_legacynamespace
        ) TO STDOUT WITH CSV HEADER"""
    return _simple_csv(full_path, "galaxy_legacynamespace", source_query)


@register("galaxy_legacyrole", "1.0", format="csv", description="Data on galaxy_legacyrole")
def galaxy_legacyrole_table(since, full_path, until, **kwargs):
    source_query = """COPY (SELECT
            id, created, modified, name, full_metadata, namespace_id
            FROM galaxy_legacyrole
        ) TO STDOUT WITH CSV HEADER"""
    return _simple_csv(full_path, "galaxy_legacyrole", source_query)


@register(
    "galaxy_aiindexdenylist", "1.0", format="csv", description="Data on galaxy_aiindexdenylist"
)
def galaxy_aiindexdenylist_table(since, full_path, until, **kwargs):
    source_query = """COPY (SELECT * FROM galaxy_aiindexdenylist
        ) TO STDOUT WITH CSV HEADER"""
    return _simple_csv(full_path, "galaxy_aiindexdenylist", source_query)


def _get_csv_splitter(file_path, max_data_size=209715200):
    return CsvFileSplitter(filespec=file_path, max_file_size=max_data_size)


def _simple_csv(full_path, file_name, query, max_data_size=209715200):
    file_path = _get_file_path(full_path, file_name)
    tfile = _get_csv_splitter(file_path, max_data_size)

    with connection.cursor() as cursor, cursor.copy(query) as copy:
        while data := copy.read():
            tfile.write(str(data, 'utf8'))

    return tfile.file_list()


def _get_file_path(path, table):
    return os.path.join(path, table + "_table.csv")
