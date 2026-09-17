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


VECTOR_EMBEDDING_POLICY = {
    'vectorEmbeddings': [
        {
            'path': '/vector',
            'dataType': 'float32',
            'dimensions': 400,
            'distanceFunction': 'cosine',
            'embeddingSource': {
                'sourcePaths': ['/description'],
                'endpoint': 'https://myaccount.services.ai.azure.com',
                'deploymentName': 'text-embedding-3-small',
                'modelName': 'text-embedding-3-small',
                'authType': 'Entra',
            },
        },
    ],
}


class CosmosDBEmbeddingSourceBodyTest(unittest.TestCase):

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
                    vector_embedding_policy=VECTOR_EMBEDDING_POLICY,
                    client_encryption_policy=None,
                )),
        )

    def _capture_request(self, *args):
        self.requests.append(args[4].resource.as_dict())

    def test_create_maps_embedding_source_to_vector_policy(self):
        cli_cosmosdb_sql_container_create(
            self.client,
            'resource-group',
            'account',
            'database',
            'container',
            '/partitionKey',
            vector_embedding_policy=VECTOR_EMBEDDING_POLICY,
        )

        policy = self.requests[-1]['vectorEmbeddingPolicy']
        self.assertEqual(policy, VECTOR_EMBEDDING_POLICY)

    def test_update_preserves_vector_policy_when_omitted(self):
        cli_cosmosdb_sql_container_update(
            self.client,
            'resource-group',
            'account',
            'database',
            'container',
        )

        policy = self.requests[-1]['vectorEmbeddingPolicy']
        self.assertEqual(policy, VECTOR_EMBEDDING_POLICY)

    def test_update_maps_explicit_empty_policy(self):
        cli_cosmosdb_sql_container_update(
            self.client,
            'resource-group',
            'account',
            'database',
            'container',
            vector_embedding_policy={},
        )

        self.assertEqual(self.requests[-1]['vectorEmbeddingPolicy'], {})


if __name__ == "__main__":
    unittest.main()
