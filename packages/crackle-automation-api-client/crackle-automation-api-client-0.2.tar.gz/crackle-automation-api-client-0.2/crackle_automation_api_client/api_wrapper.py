""" Python API Wrapper for 'Crackle Automation Reporter Web Service' """
import json
from crackle_automation_api_client import MissingCredentialsError, SESSION


class Reporter():
    """
    Reporter API wrapper methods
    """
    def __init__(self, host, username, password):
        if not (host and username and password):
            raise MissingCredentialsError()
        self.host = host
        self.username = username
        self.password = password

    def list_reports(self):
        """
        List reports
        GET /reports/
        """
        endpoint = '/reports/'
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)
        return SESSION.get(path)

    def get_report(self, report_id):
        """
        Get a report object, which includes master reports
        GET /reports/{report_id}
        """
        endpoint = '/reports/{}'.format(report_id)
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)
        return SESSION.get(path)

    def create_report(self, **kwargs):
        """
        Create a new report object
        name (optional): string identifier
        POST /reports/
        """
        endpoint = '/reports/'
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)
        mandatory_data = {
            "platform": kwargs.get('platform', None),
            "environment": kwargs.get('environment', None),
            "testrail_base_url": kwargs.get('testrail_base_url', None),
            "testrail_test_run": kwargs.get('testrail_test_run', None),
            "publish_html_report": kwargs.get('publish_html_report', None)
        }
        if None in mandatory_data.values():
            failure_msg = ("Mandatory fields were not passed to "
                           "create_report()")
            raise Exception(failure_msg)

        optional_data = {
            "name": kwargs.get('name', '')
        }
        data = json.dumps({**mandatory_data, **optional_data})
        return SESSION.post(path, data=data)

    def delete_report(self, report_id):
        """
        Delete a report
        DELETE /report/{report_id}
        """
        endpoint = '/reports/{}'.format(report_id)
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)
        return SESSION.delete(path)

    def list_results(self):
        """
        List results
        GET /results/
        """
        endpoint = '/results/'
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)
        return SESSION.get(path)

    def get_result(self, result_id):
        """
        Get a result object
        GET /results/{result_id}
        """
        endpoint = '/results/{}'.format(result_id)
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)
        return SESSION.get(path)

    def get_result_single_report(self, result_id):
        """
        Convenience method. Get the 'single_report' value from a Result object
        GET /results/{result_id}/single_report
        """
        endpoint = '/results/{}/single_report'.format(result_id)
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)
        return SESSION.get(path)

    def create_result(self, **kwargs):
        """
        Create a result and associate it with a report
        POST /results/
        """
        endpoint = '/results/'
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)

        mandatory_data = {
            "report": kwargs.get('report', None),
            "scenario_name": kwargs.get('scenario_name', None),
            "status": kwargs.get('status', None),
            "gherkin_table_rows": kwargs.get('gherkin_table_rows', None),
            "gherkin_table_headers": kwargs.get('gherkin_table_headers', None)
        }
        if None in mandatory_data.values():
            failure_msg = ("Mandatory fields were not passed to "
                           "create_result()")
            raise Exception(failure_msg)

        optional_data = {
            "failing_step_name": kwargs.get('failing_step_name', ''),
            "failing_step_errormsg": kwargs.get('failing_step_errormsg', ''),
            "tags": kwargs.get('tags', ''),
            "missing_tags": kwargs.get('missing_tags', ''),
            "all_pairs": kwargs.get('all_pairs', ''),
            "found_pairs": kwargs.get('found_pairs', '')
        }
        data = json.dumps({**mandatory_data, **optional_data})
        return SESSION.post(path, data=data)

    def get_report_results(self, report_id):
        """
        Get a list of all Results associated with a Report
        GET /report/{report_id}/results/
        """
        endpoint = '/reports/{}/results/'.format(report_id)
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)
        return SESSION.get(path)

    def publish_html_master_report(self, report_id):
        """
        Publish the HTML Master Report for the given Report
        GET /report/{report_id}/publish_html_report/
        """
        endpoint = '/reports/{}/publish_html_report/'.format(report_id)
        SESSION.auth = (self.username, self.password)
        path = '{0}{1}'.format(self.host, endpoint)
        return SESSION.get(path)
