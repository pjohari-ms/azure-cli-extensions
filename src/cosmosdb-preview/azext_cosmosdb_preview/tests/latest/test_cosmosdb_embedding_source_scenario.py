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
        self.cmd(
            'cosmosdb sql container create -g {rg} -a {account} -d {database} '
            '-n {container} -p /partitionKey --vector-embeddings @{policy}',
            checks=[
                self.check(
                    'resource.vectorEmbeddingPolicy.vectorEmbeddings[0].embeddingSource.authType',
                    'Entra'),
                self.check(
                    'resource.vectorEmbeddingPolicy.vectorEmbeddings[0].embeddingSource.sourcePaths[0]',
                    '/description'),
            ])
        self.cmd(
            'cosmosdb sql container update -g {rg} -a {account} -d {database} '
            '-n {container} --vector-embeddings @{policy}',
            checks=[
                self.check(
                    'resource.vectorEmbeddingPolicy.vectorEmbeddings[0].embeddingSource.deploymentName',
                    'text-embedding-3-small'),
            ])
        self.cmd(
            'cosmosdb sql container show -g {rg} -a {account} -d {database} -n {container}',
            checks=[
                self.check(
                    'resource.vectorEmbeddingPolicy.vectorEmbeddings[0].embeddingSource.modelName',
                    'text-embedding-3-small'),
            ],
        )
