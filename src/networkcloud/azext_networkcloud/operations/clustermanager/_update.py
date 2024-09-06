# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
This custom code inherits the auto-generated code for ClusterManager update,
disables the --identity parameter and adds the --mi-user-assigned and --mi-system-assigned parameters
"""

from azext_networkcloud.aaz.latest.networkcloud.clustermanager._update import (
    Update as _Update,
)
from azure.cli.core.aaz import register_callback

from ..common_managedidentity import ManagedIdentity


class Update(_Update):
    """Custom class for update operation of clustermanager"""

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        return ManagedIdentity.build_arguments_schema(args_schema)

    @register_callback
    def pre_operations(self):
        ManagedIdentity.pre_operations_update(self.ctx.args)