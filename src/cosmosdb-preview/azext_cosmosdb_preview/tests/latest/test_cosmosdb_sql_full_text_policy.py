# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from types import SimpleNamespace

from azext_cosmosdb_preview.custom import (
    cli_cosmosdb_sql_container_create,
    cli_cosmosdb_sql_container_update,
)


FULL_TEXT_POLICY = {
    'defaultLanguage': 'en-US',
    'package': 'standard',
    'defaultSpec': {
        'language': 'en-US',
        'tokenizer': 'word',
        'filters': ['lowercase', 'stop'],
        'stopWordListKind': 'basic',
        'addStopWords': ['cosmos'],
        'removeStopWords': ['is', 'the'],
    },
    'fullTextPaths': [
        {
            'path': '/description',
            'language': 'en-US',
            'tokenizer': 'word',
            'filters': ['lowercase'],
            'stopWordListKind': 'basic',
            'addStopWords': ['cosmos'],
            'removeStopWords': ['is'],
        },
    ],
}


class CosmosDBSqlFullTextPolicyBodyTest(unittest.TestCase):

    def setUp(self):
        self.requests = []
        self.client = SimpleNamespace(
            begin_create_update_sql_container=self._capture_request,
            get_sql_container=lambda *_: SimpleNamespace(
                resource=SimpleNamespace(
                    partition_key=None,
                    indexing_policy=None,
                    default_ttl=None,
                    unique_key_policy=None,
                    conflict_resolution_policy=None,
                    materialized_view_definition=None,
                    full_text_policy=FULL_TEXT_POLICY,
                    client_encryption_policy=None,
                )),
        )

    def _capture_request(self, *args):
        self.requests.append(args[4].resource.as_dict())

    def test_create_maps_full_text_policy_to_request_body(self):
        cli_cosmosdb_sql_container_create(
            self.client,
            'resource-group',
            'account',
            'database',
            'container',
            '/partitionKey',
            full_text_policy=FULL_TEXT_POLICY,
        )

        self.assertEqual(self.requests[-1]['fullTextPolicy'], FULL_TEXT_POLICY)

    def test_update_preserves_full_text_policy_when_omitted(self):
        cli_cosmosdb_sql_container_update(
            self.client,
            'resource-group',
            'account',
            'database',
            'container',
        )

        self.assertEqual(self.requests[-1]['fullTextPolicy'], FULL_TEXT_POLICY)

    def test_update_maps_explicit_empty_policy(self):
        cli_cosmosdb_sql_container_update(
            self.client,
            'resource-group',
            'account',
            'database',
            'container',
            full_text_policy={},
        )

        self.assertEqual(self.requests[-1]['fullTextPolicy'], {})


if __name__ == "__main__":
    unittest.main()
