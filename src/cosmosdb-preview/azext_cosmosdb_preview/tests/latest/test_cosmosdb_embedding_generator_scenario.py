# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import ScenarioTest


class CosmosDBEmbeddingGeneratorScenarioTest(ScenarioTest):

    def test_cosmosdb_embedding_generator_scenario(self):
        self.kwargs.update({
            'account': 'dbaccount30',
            'rg': 'CosmosDBResourceGroup27',
        })

        # TODO(review-prerequisite): Confirm this existing API for NoSQL account uses continuous backup and all versions and deletes change feed.

        self.cmd(
            'cosmosdb update -g {rg} -n {account} '
            '--enable-embedding-generator true',
            checks=[self.check('enableEmbeddingGenerator', True)])
        self.cmd(
            'cosmosdb update -g {rg} -n {account} --tags embeddingGenerator=enabled',
            checks=[self.check('enableEmbeddingGenerator', True)])
        self.cmd(
            'cosmosdb show -g {rg} -n {account}',
            checks=[self.check('enableEmbeddingGenerator', True)])

        # TODO(review-prerequisite): Confirm the shared prerequisite account must remain enabled after this scenario rather than be deleted.
