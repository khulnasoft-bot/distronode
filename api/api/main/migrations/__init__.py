# Copyright (c) 2016 Distronode, Inc.
# All Rights Reserved.

from django.db.migrations import Migration


class ActivityStreamDisabledMigration(Migration):
    def apply(self, project_state, schema_editor, collect_sql=False):
        from api.main.signals import disable_activity_stream

        with disable_activity_stream():
            return Migration.apply(self, project_state, schema_editor, collect_sql)
