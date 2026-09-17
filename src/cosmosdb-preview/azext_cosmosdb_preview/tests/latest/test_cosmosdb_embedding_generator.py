# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from types import SimpleNamespace

from azext_cosmosdb_preview.custom import (
    _create_database_account,
    cli_cosmosdb_update,
)


class CosmosDBEmbeddingGeneratorBodyTest(unittest.TestCase):

    def setUp(self):
        self.create_requests = []
        self.update_requests = []
        self.existing = SimpleNamespace(
            consistency_policy=SimpleNamespace(
                max_staleness_prefix=100,
                max_interval_in_seconds=5,
                default_consistency_level='Session',
            ))
        self.client = SimpleNamespace(
            begin_create_or_update=self._capture_create,
            begin_update=self._capture_update,
            get=lambda *_: self.existing,
        )

    @staticmethod
    def _poller():
        return SimpleNamespace(result=lambda: None)

    def _capture_create(self, *args):
        self.create_requests.append(args[2].as_dict())
        return self._poller()

    def _capture_update(self, *args):
        self.update_requests.append(args[2].as_dict())
        return self._poller()

    def test_create_maps_explicit_false(self):
        _create_database_account(
            self.client,
            'resource-group',
            'account',
            arm_location='centraluseuap',
            enable_embedding_generator=False,
        )

        properties = self.create_requests[-1]['properties']
        self.assertIs(properties['enableEmbeddingGenerator'], False)

    def test_update_omits_embedding_generator_when_unspecified(self):
        cli_cosmosdb_update(self.client, 'resource-group', 'account')

        properties = self.update_requests[-1]['properties']
        self.assertNotIn('enableEmbeddingGenerator', properties)

    def test_update_maps_explicit_true(self):
        cli_cosmosdb_update(
            self.client,
            'resource-group',
            'account',
            enable_embedding_generator=True,
        )

        properties = self.update_requests[-1]['properties']
        self.assertIs(properties['enableEmbeddingGenerator'], True)


if __name__ == "__main__":
    unittest.main()
