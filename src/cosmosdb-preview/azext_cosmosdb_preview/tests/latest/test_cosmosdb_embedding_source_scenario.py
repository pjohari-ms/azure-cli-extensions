# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

from azure.cli.testsdk import ResourceGroupPreparer, ScenarioTest


TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


class CosmosDBEmbeddingSourceScenarioTest(ScenarioTest):

    @ResourceGroupPreparer(
        name_prefix='cli_test_cosmosdb_embedding_source',
        location='centraluseuap')
    def test_cosmosdb_embedding_source_scenario(self):
        self.kwargs.update({
            'account': self.create_random_name('embeddingsource', 20),
            'database': self.create_random_name('database', 20),
            'container': self.create_random_name('container', 20),
            'policy': os.path.join(
                TEST_DIR, 'vector-embedding-policy.json').replace('\\', '\\\\'),
        })

        self.cmd('cosmosdb create -g {rg} -n {account}')
        self.cmd('cosmosdb sql database create -g {rg} -a {account} -n {database}')
        container_create = self.cmd(
            'cosmosdb sql container create -g {rg} -a {account} -d {database} '
            '-n {container} -p /partitionKey --vector-embeddings @{policy}').get_output_in_json()
        embedding_source = container_create['resource']['vectorEmbeddingPolicy']['vectorEmbeddings'][0]['embeddingSource']
        assert embedding_source['authType'] == 'Entra'
        assert embedding_source['sourcePaths'][0] == '/description'

        container_update = self.cmd(
            'cosmosdb sql container update -g {rg} -a {account} -d {database} '
            '-n {container} --vector-embeddings @{policy}').get_output_in_json()
        embedding_source = container_update['resource']['vectorEmbeddingPolicy']['vectorEmbeddings'][0]['embeddingSource']
        assert embedding_source['deploymentName'] == 'text-embedding-3-small'

        container_show = self.cmd(
            'cosmosdb sql container show -g {rg} -a {account} -d {database} '
            '-n {container}').get_output_in_json()
        embedding_source = container_show['resource']['vectorEmbeddingPolicy']['vectorEmbeddings'][0]['embeddingSource']
        assert embedding_source['modelName'] == 'text-embedding-3-small'
