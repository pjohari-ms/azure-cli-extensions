# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

from azure.cli.testsdk import ResourceGroupPreparer, ScenarioTest


TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


class CosmosDBSqlFullTextPolicyScenarioTest(ScenarioTest):

    @ResourceGroupPreparer(
        name_prefix='cli_test_cosmosdb_sql_full_text_policy',
        location='centraluseuap')
    def test_cosmosdb_sql_full_text_policy_scenario(self):
        self.kwargs.update({
            'account': self.create_random_name('fulltext', 20),
            'database': self.create_random_name('database', 20),
            'container': self.create_random_name('container', 20),
            'policy': os.path.join(TEST_DIR, 'full-text-policy.json').replace('\\', '\\\\'),
        })

        self.cmd('cosmosdb create -g {rg} -n {account}')
        self.cmd('cosmosdb sql database create -g {rg} -a {account} -n {database}')
        self.cmd(
            'cosmosdb sql container create -g {rg} -a {account} -d {database} '
            '-n {container} -p /partitionKey --full-text-policy @{policy}',
            checks=[
                self.check('resource.fullTextPolicy.package', 'standard'),
                self.check('resource.fullTextPolicy.defaultSpec.tokenizer', 'word'),
                self.check('resource.fullTextPolicy.fullTextPaths[0].filters[0]', 'lowercase'),
            ])
        self.cmd(
            'cosmosdb sql container update -g {rg} -a {account} -d {database} '
            '-n {container} --full-text-policy @{policy}',
            checks=[
                self.check('resource.fullTextPolicy.defaultSpec.stopWordListKind', 'basic'),
                self.check('resource.fullTextPolicy.fullTextPaths[0].addStopWords[0]', 'cosmos'),
            ])
        self.cmd(
            'cosmosdb sql container show -g {rg} -a {account} -d {database} -n {container}',
            checks=[
                self.check('resource.fullTextPolicy.package', 'standard'),
                self.check('resource.fullTextPolicy.fullTextPaths[0].tokenizer', 'word'),
            ],
        )
