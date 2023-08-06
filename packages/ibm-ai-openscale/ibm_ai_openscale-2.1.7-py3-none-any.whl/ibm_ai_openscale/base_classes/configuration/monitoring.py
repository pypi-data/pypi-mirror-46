# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from ibm_ai_openscale.utils import *
from ibm_ai_openscale.base_classes.configuration.custom_metrics_viewer import CustomMetricsViewer
from ibm_ai_openscale.supporting_classes.enums import *
from datetime import datetime


_DEFAULT_LIST_LENGTH = 50


@logging_class
class Monitoring(CustomMetricsViewer):
    """Manage monitoring."""

    def __init__(self, subscription, ai_client):
        self._ai_client = ai_client
        self._subscription = subscription
        self._custom_metrics_viewer = CustomMetricsViewer(ai_client, subscription, MetricTypes.CUSTOM_MONITORING, 'CustomMetrics')

    def enable(self, monitor_uid, thresholds=None, **kwargs):
        """
        Enables monitoring for particular custom monitor.

        :param monitor_uid: uid of custom monitor
        :type monitor_uid: str

        :param thresholds: list of thresholds objects
        :type thresholds: list

        :param kwargs: configuration parameters depending on monitor definition
        :type kwargs: dict

        A way you might use me is:

        >>> from ibm_ai_openscale.supporting_classes import Threshold
        >>>
        >>> thresholds = [Threshold(metric_uid='log_loss', upper_limit=0.7)]
        >>> subscription.custom_monitoring.enable(monitor_uid='1212', thresholds=thresholds)
        """

        validate_type(monitor_uid, 'monitor_uid', str, True)
        validate_type(thresholds, 'thresholds', list, False)
        monitor_details = self._ai_client.data_mart.monitors.get_details(monitor_uid=monitor_uid)
        payload = {"enabled": True}

        if bool(kwargs):
            if 'parameters' in monitor_details.keys():
                monitor_parameters_names = monitor_details['parameters']['properties'].keys()

                if set(list(kwargs.keys())) <= set(monitor_parameters_names):
                    configuration_params = {}

                    for key, value in kwargs.items():
                        configuration_params[key] = value

                    payload['parameters'] = configuration_params
                else:
                    raise IncorrectParameter(parameter_name=', '.join(list(kwargs.keys())),
                                             reason='Passed parameters are different than defined ones (monitor definition): '
                                                    + str(monitor_parameters_names))

        if thresholds is not None:
            thresholds_value = []
            for t in thresholds:
                thresholds_value.extend(t._to_json())

            payload['thresholds'] = thresholds_value

        response = requests_session.put(
            self._ai_client._href_definitions.get_custom_monitoring_href(self._subscription.binding_uid, self._subscription.uid, monitor_uid),
            json=payload,
            headers=self._ai_client._get_headers()
        )

        handle_response(200, u'custom monitoring setup', response)

    def store_metrics(self, monitor_uid, metrics):
        """
        Stores metrics values for particular custom monitor instance.

        :param monitor_uid: uid of custom monitor
        :type monitor_uid: str

        :param metrics: metrics values
        :type metrics: dict

        A way you might use me is:

        >>> metrics = {"log_loss": 0.78, "recall_score": 0.67, "region": "us-south"}
        >>> subscription.custom_monitoring.store(monitor_uid='1212', metrics=metrics)
        """

        validate_type(monitor_uid, 'monitor_uid', str, True)
        validate_type(metrics, 'metrics', dict, True)

        payload = [
            {
                "monitor_definition_id": monitor_uid,
                "binding_id": self._subscription.binding_uid,
                "timestamp": datetime.utcnow().isoformat() + 'Z',
                "subscription_id": self._subscription.uid,
                "value": metrics
            }
        ]

        response = requests_session.post(
            self._ai_client._href_definitions.get_ootb_metrics_href(),
            json=payload,
            headers=self._ai_client._get_headers()
        )

        handle_response(202, u'storing metrics', response)

    def get_details(self, monitor_uid):
        """
        Returns details of custom monitoring configuration.
        :param monitor_uid: uid of custom monitor
        :type monitor_uid: str

        :return: configuration of custom monitoring
        :rtype: dict
        """

        validate_type(monitor_uid, 'monitor_uid', str, True)

        response = requests_session.get(
            self._ai_client._href_definitions.get_custom_monitoring_href(self._subscription.binding_uid, self._subscription.uid, monitor_uid),
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, u'custom monitoring details', response)

    def disable(self, monitor_uid):
        """
        Disables custom monitoring.

        :param monitor_uid: uid of custom monitor
        :type monitor_uid: str
        """

        validate_type(monitor_uid, 'monitor_uid', str, True)

        if not self.get_details(monitor_uid)['enabled']:
            raise ClientError('Monitor is not enabled, so it cannot be disabled.')

        response = requests_session.put(
            self._ai_client._href_definitions.get_custom_monitoring_href(self._subscription.binding_uid, self._subscription.uid, monitor_uid),
            json={
                "enabled": False
            },
            headers=self._ai_client._get_headers()
        )

        handle_response(200, u'quality monitoring unset', response)

    def get_metrics(self, deployment_uid, monitor_uid, format='samples'):
        """
        Returns custom metrics of specified type and format for selected subscription and monitor

        :param deployment_uid: deployment uid for which the metrics will be retrieved
        :type deployment_uid: str

        :param monitor_uid: uid of custom monitor
        :type monitor_uid: str

        :param format: format of returned metrics, possible values: `samples`, `time_series` (optional, default value: `samples`) (optional)
        :type format: str

        :return: metrics for deployment
        :rtype: dict
        """

        return super(Monitoring, self).get_metrics(deployment_uid=deployment_uid, monitor_uid=monitor_uid, format=format)

    def show_table(self, monitor_uid, limit=10):
        """
        Show records in custom metrics view. By default 10 records will be shown.

        :param monitor_uid: uid of custom monitor
        :type monitor_uid: str

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>> subscription.custom_monitoring.show_table(monitor_uid='123', limit=20)
        """

        self._custom_metrics_viewer.show_table(monitor_uid=monitor_uid, limit=limit)

    def print_table_schema(self, monitor_uid):
        """
        Show custom metrics view schema.

        :param monitor_uid: uid of custom monitor
        :type monitor_uid: str

        """

        self._custom_metrics_viewer.print_table_schema(monitor_uid)

    def get_table_content(self, monitor_uid, format='pandas', limit=None):
        """
        Get content of custom metrics view in chosen format. By default the format is 'pandas'.

        :param monitor_uid: uid of custom monitor
        :type monitor_uid: str

        :param format: format of returned content, may be one of following: ['python', 'pandas'], by default is set 'pandas' (optional)
        :type format: {str_type}

        :param limit: maximal number of fetched rows. (optional)
        :type limit: int

        :return: monitoring table content
        :rtype: pandas or dict depending on format

        A way you might use me is:

        >>> pandas_table_content = subscription.custom_monitoring.get_table_content(monitor_uid=monitor_uid)
        >>> table_content = subscription.custom_monitoring.get_table_content(monitor_uid=monitor_uid, format='python')
        """

        return self._custom_metrics_viewer.get_table_content(format=format, monitor_uid=monitor_uid, limit=limit)

    def describe_table(self, monitor_uid):
        """
        Prints description of the content of monitoring table (pandas style). It will remove columns with unhashable values.

        :param monitor_uid: uid of custom monitor
        :type monitor_uid: str

        A way you might use me is:

        >>> subscription.monitoring.describe_table(monitor_uid='123')
        """

        self._custom_metrics_viewer.describe_table(monitor_uid=monitor_uid)

    def print_table_schema(self):
        """
        Show quality metrics view schema.
        """
        self._custom_metrics_viewer.print_table_schema()
