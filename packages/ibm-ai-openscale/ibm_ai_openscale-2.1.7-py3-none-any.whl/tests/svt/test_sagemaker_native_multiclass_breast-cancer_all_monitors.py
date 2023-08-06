# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import unittest
import boto3
import time
from preparation_and_cleaning import *
from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes.payload_record import PayloadRecord
from ibm_ai_openscale.supporting_classes.enums import ProblemType, InputDataType
from ibm_ai_openscale.supporting_classes import Feature


class TestAIOpenScaleClient(unittest.TestCase):

    ai_client = None
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    wml_client = None
    subscription = None
    binding_uid = None
    aios_model_uid = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    source_uid = None
    transaction_id = None

    test_uid = str(uuid.uuid4())

    # AWS configuration
    credentials = {
        "access_key_id": "AKIAI3LQITG4RLLSUIHA",
        "secret_access_key": "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",
        "region": "us-east-1"
    }

    def score(self, binding_details, subscription_details):
        access_id = binding_details['entity']['credentials']['access_key_id']
        access_key = binding_details['entity']['credentials']['secret_access_key']
        region = binding_details['entity']['credentials']['region']
        endpoint_name = subscription_details['entity']['deployments'][0]['name']

        runtime = boto3.client('sagemaker-runtime',
                               region_name=region,
                               aws_access_key_id=access_id,
                               aws_secret_access_key=access_key)

        fields = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'compactness_mean',
                  'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean', 'radius_se',
                  'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se',
                  'concave points_se', 'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
                  'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst',
                  'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst']
        payload = "15.02,23.98,112.8,899.3,0.1197,0.1496,0.2417,0.1203,0.2248,0.06382,0.6009,1.398,3.999,67.78,0.008268,0.03082,0.05042,0.01112,0.02102,0.003854,20.88,32.09,136.1,1344,0.1634,0.3559,0.5588,0.1847,0.353,0.08482\n9.02,23.98,112.8,899.3,0.1197,0.1496,0.2417,0.1203,0.2248,0.06382,0.6009,1.398,3.999,67.78,0.008268,0.03082,0.05042,0.01112,0.02102,0.003854,20.88,32.09,136.1,1344,0.1634,0.3559,0.5588,0.1847,0.353,0.08482"

        start_time = time.time()
        response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                           ContentType='text/csv',
                                           Body=payload)
        response_time = time.time() - start_time
        result = json.loads(response['Body'].read().decode())

        values = []
        for v in payload.split('\n'):
            values.append([float(s) for s in v.split(',')])

        request = {'fields': fields, 'values': values}
        response = {
            'fields': list(result['predictions'][0]),
            'values': [list(x.values()) for x in result['predictions']]
        }

        return request, response, response_time

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)

        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_bind_sagemaker(self):
        TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("SageMaker ml engine", SageMakerMachineLearningInstance(self.credentials))
        print("Binding uid: {}".format(TestAIOpenScaleClient.binding_uid))

    def test_03_get_binding_details(self):
        binding_details = self.ai_client.data_mart.bindings.get_details()
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)

    def test_04_get_assets(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()

        asset_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_details()
        print("Assets details: {}".format(asset_details))

        asset_name = ""
        for detail in asset_details:
            if 'DEMO-multi-classification-2018-10-10-14-26-26' in detail['name']:
                asset_name = detail['name']
                TestAIOpenScaleClient.source_uid = detail['source_uid']

        print("asset name: {}".format(asset_name))
        print("asset uid: {}".format(TestAIOpenScaleClient.source_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.source_uid)

    def test_05_get_asset_deployments(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_asset_deployments()

    def test_06_subscribe_sagemaker_asset(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            SageMakerMachineLearningAsset(
                source_uid=TestAIOpenScaleClient.source_uid,
                binding_uid=TestAIOpenScaleClient.binding_uid,
                input_data_type=InputDataType.STRUCTURED,
                problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
                prediction_column='predicted_label',
                probability_column='score',
                label_column='diagnosis',
                feature_columns=['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'],
                categorical_columns=[],
            ))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription uid: ".format(TestAIOpenScaleClient.subscription_uid))

    def test_07_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        details = TestAIOpenScaleClient.subscription.get_details()
        print('Subscription details: ' + str(details))

        self.assertTrue('s3' in str(details))

    def test_08_list_deployments(self):
        print("Listing deployments:\n")
        self.subscription.list_deployments()

    def test_09_validate_default_subscription_configuration(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()

        for configuration in subscription_details['entity']['configurations']:
            if configuration['type'] == 'payload_logging' or configuration['type'] == 'performance_monitoring':
                self.assertTrue(configuration['enabled'])
            else:
                self.assertFalse(configuration['enabled'])

    def test_10_score_model_and_log_payload(self):
        binding_details = self.ai_client.data_mart.bindings.get_details(self.binding_uid)
        subscription_details = self.subscription.get_details()

        request, response, response_time = self.score(binding_details=binding_details, subscription_details=subscription_details)
        records_list = []
        TestAIOpenScaleClient.transaction_id = str(uuid.uuid4()).replace("-", "")
        records_list.append(PayloadRecord(request=request, response=response, response_time=int(response_time),
                                          scoring_id=TestAIOpenScaleClient.transaction_id))
        for i in range(0, 15):
            records_list.append(PayloadRecord(request=request, response=response, response_time=int(response_time)))

        self.subscription.payload_logging.store(records=records_list)
        time.sleep(20)

    def test_11_stats_on_payload_logging_table(self):
        print("Print table schema:")
        self.subscription.payload_logging.print_table_schema()

        print("Describe table description:")
        self.subscription.payload_logging.describe_table()

        table_content = self.subscription.payload_logging.get_table_content()
        print("Table content:\n{}".format(table_content))

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        print("Python Table content:\n{}".format(python_table_content))

        self.assertTrue(table_content.size > 1)
        self.assertIsNotNone(python_table_content)

    def test_12_stats_on_performance_monitoring_table(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.performance_monitoring.show_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content(
            format='python')
        self.assertGreater(len(performance_metrics['values']), 0)

    def test_13_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.8, min_records=5)

    def test_14_get_quality_monitoring_details(self):
        print("Quality monitoring details:\n{}".format(TestAIOpenScaleClient.subscription.quality_monitoring.get_details()))

    # SKIPPED FOR NOW
    #
    # def test_15_setup_explainability(self):
    #     with open('assets/training_distribution_breast_cancer.json') as json_file:
    #         training_data_statistics = json.load(json_file)
    #
    #     self.assertIsNotNone(training_data_statistics)
    #
    #     TestAIOpenScaleClient.subscription.explainability.enable(
    #         training_data_statistics=training_data_statistics
    #     )
    #
    # def test_16_get_explainability_details(self):
    #     print("Explainability details:\n{}".format(TestAIOpenScaleClient.subscription.explainability.get_details()))
    #     subscription_details = TestAIOpenScaleClient.subscription.get_details()
    #     self.assertTrue('label' in str(subscription_details))
    #
    # def test_17_setup_fairness(self):
    #     with open('assets/training_distribution_breast_cancer.json') as json_file:
    #         training_data_statistics = json.load(json_file)
    #
    #     self.assertIsNotNone(training_data_statistics)
    #
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
    #         features=[
    #             Feature("radius_mean", [[0, 10], [19, 20]], [[15, 16]], 0.8)
    #         ],
    #         favourable_classes=[0],
    #         unfavourable_classes=[1],
    #         min_records=4,
    #         training_data_statistics=training_data_statistics
    #     )
    #
    # def test_18_get_fairness_monitoring_details(self):
    #     print("Fairness details:\n{}".format(TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()))

    # def test_19_validate_subscription_configuration_with_all_monitors(self):
    #     subscription_details = TestAIOpenScaleClient.subscription.get_details()
    #
    #     for configuration in subscription_details['entity']['configurations']:
    #         self.assertTrue(configuration['enabled'])

    def test_20_export_subscription_configuration(self):
        config = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.export_configuration(TestAIOpenScaleClient.subscription_uid)
        print("Subscription configuration:", config)
        self.assertTrue('diagnosis' in str(config))

        print('Storing exported subscription configuration to json file ...')
        import json
        with open('assets/sagemaker_native_multiclass_breast-cancer_all_monitors_sub_configuration.json', 'w') as fp:
            json.dump(config, fp)

    def test_21_send_feedback_data(self):
        feedback_records = []

        fields = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst', 'diagnosis']

        for i in range(1, 10):
            feedback_records.append(
                [17.02,23.98,112.8,899.3,0.1197,0.1496,0.2417,0.1203,0.2248,0.06382,0.6009,1.398,3.999,67.78,0.008268,0.03082,0.05042,0.01112,0.02102,0.003854,20.88,32.09,136.1,1344,0.1634,0.3559,0.5588,0.1847,0.353,0.08482, 1])

        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=feedback_records, fields=fields)

        time.sleep(20)
        print('subscription_details' + str(TestAIOpenScaleClient.subscription.get_details()))

    def test_22_run_quality_monitor(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        self.assertTrue('Prerequisite Check' in str(run_details))

        status = run_details['status']
        id = run_details['id']
        start_time = time.time()
        elapsed_time = 0

        while status != 'completed' and elapsed_time < 60:
            time.sleep(10)
            run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(run_uid=id)
            status = run_details['status']
            print("Run details: {}".format(run_details))
            self.assertNotIn('failed', status)

            elapsed_time = time.time() - start_time

        self.assertTrue('completed' in status)

    def test_23_stats_on_quality_monitoring_table(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table(limit=None)
        TestAIOpenScaleClient.subscription.quality_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def test_24_stats_on_feedback_logging_table(self):
        TestAIOpenScaleClient.subscription.feedback_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.feedback_logging.show_table()
        TestAIOpenScaleClient.subscription.feedback_logging.describe_table()
        TestAIOpenScaleClient.subscription.feedback_logging.get_table_content()
        feedback_logging = TestAIOpenScaleClient.subscription.feedback_logging.get_table_content(format='python')
        self.assertTrue(len(feedback_logging['values']) > 0)

    # SKIP FOR NOW
    #
    # def test_25_get_explainability_details(self):
    #     print("Explainability details:\n{}".format(TestAIOpenScaleClient.subscription.explainability.get_details()))
    #
    # def test_26_run_explainability(self):
    #     TestAIOpenScaleClient.status = TestAIOpenScaleClient.subscription.explainability.run(
    #         transaction_id="{}-1".format(TestAIOpenScaleClient.transaction_id),
    #         background_mode=False
    #     )['entity']['status']['state']
    #     print("Status: {}".format(TestAIOpenScaleClient.status))
    #     self.assertTrue(TestAIOpenScaleClient.status == "finished")
    #
    #     print("Waiting 20 seconds for propagation...")
    #     time.sleep(20)
    #
    # def test_27_print_explainability_table_schema(self):
    #     TestAIOpenScaleClient.subscription.explainability.print_table_schema()
    #
    # def test_28_stats_on_explainability_table(self):
    #     TestAIOpenScaleClient.subscription.explainability.show_table()
    #     TestAIOpenScaleClient.subscription.explainability.describe_table()
    #     pandas_df = TestAIOpenScaleClient.subscription.explainability.get_table_content()
    #     print(str(pandas_df))
    #     self.assertTrue(pandas_df.size > 1)
    #
    # def test_29_run_fairness(self):
    #     run_details = TestAIOpenScaleClient.subscription.fairness_monitoring.run()
    #     print('Run details: ' + str(run_details))
    #
    #     status = ""
    #     for i in range(0, 12):
    #         run_details = TestAIOpenScaleClient.subscription.fairness_monitoring.get_run_details(deployment_uid=self.deployment_uid)
    #         print("Current run details: {}".format(run_details))
    #         if 'last_run_status' in run_details['entity']['parameters'].keys():
    #             status = run_details['entity']['parameters']['last_run_status']
    #             print("Current run status: {}".format(status))
    #             if status == 'FINISHED':
    #                 break
    #         time.sleep(10)
    #
    #     self.assertEqual('FINISHED', status)
    #
    #     print("Waiting 20 seconds...")
    #     time.sleep(20)
    #
    #     print("Fairness details:\n{}".format(TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()))
    #
    # def test_30_stats_on_fairness_monitoring_table(self):
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
    #     TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()
    #     pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
    #     print(str(pandas_df))
    #     self.assertTrue(pandas_df.size > 1)
    #     print('fairness_monitoring.get_table_content',TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python'))

    def test_31_disable_all_monitors(self):
        self.subscription.quality_monitoring.disable()

        # self.subscription.fairness_monitoring.disable()
        # self.subscription.explainability.disable()
        self.subscription.payload_logging.disable()
        self.subscription.performance_monitoring.disable()

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print(subscription_details)

        for configuration in subscription_details['entity']['configurations']:
            self.assertFalse(configuration['enabled'])

    def test_32_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def test_33_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)

    @classmethod
    def tearDownClass(cls):
        print("Deleting DataMart.")
        cls.ai_client.data_mart.delete()


if __name__ == '__main__':
    unittest.main()
