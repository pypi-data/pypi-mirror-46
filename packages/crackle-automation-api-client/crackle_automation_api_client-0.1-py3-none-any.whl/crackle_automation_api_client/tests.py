""" Unit Tests for 'Crackle Automation Reporter Web Service' """
from __future__ import print_function
import json
import os
import unittest
from crackle_automation_api_client.api_wrapper import Reporter


class StopTests(Exception):
    """
    Forcefully abort all unit tests
    """


class Tests(unittest.TestCase):
    """ Test all helper methods """

    def setUp(self):
        """ Set up tasks for tests """
        self.host = os.getenv('reporting_service_url')
        self.username = os.getenv('reporting_service_user')
        self.password = os.getenv('reporting_service_password')
        if not (self.host or self.username or self.password):
            raise Exception('Configuration values missing.')
        self.reporter = Reporter(
            host=self.host, username=self.username, password=self.password)
        self.report_ids = []  # report_ids for cleanup

    def tearDown(self):
        """ Tear down tasks for tests """
        for report_id in self.report_ids:
            resp = self.reporter.delete_report(report_id)
            if not resp.status_code == 204:
                print("tearDown: Failed to delete test Report object. "
                      "{0}. {1}".format(resp.status_code, resp.content))
            print('tearDown: Deleted report: {}'.format(report_id))

    def test_create_report(self):
        """ test_create_report() """
        # 1. create_report()
        testrail_base_url = 'http://test.com'
        testrail_test_run = '1234'
        platform = 'test_platform'
        environment = 'test_env'
        name = 'test_name'
        publish_html_report = False
        resp = self.reporter.create_report(
            testrail_base_url=testrail_base_url,
            testrail_test_run=testrail_test_run,
            platform=platform, environment=environment, name=name,
            publish_html_report=publish_html_report)
        expected_code = 201
        actual_code = resp.status_code
        failure_msg = ("create_report(): Expected response status code to be "
                       "{0} but it was {1}".format(expected_code, actual_code))
        assert actual_code == expected_code, failure_msg
        self.report_ids.append(int(json.loads(resp.content).get('id')))
        return resp


    def test_delete_report(self):
        """ test_delete_report() """
        # 1. create_report()
        resp = self.test_create_report()
        report_id = int(json.loads(resp.content).get('id'))

        # 2. delete_report()
        resp = self.reporter.get_report(report_id)
        expected_code = 200
        actual_code = resp.status_code
        assertion = actual_code == expected_code
        if not assertion:
            failure_msg = ("delete_report(): Expected response status code to "
                           "be {0} but it was {1}. Aborting tests as "
                           "new test data cannot be cleaned up.".format(
                               expected_code, actual_code))
            raise StopTests(failure_msg)


    def test_get_report(self):
        """ test_get_report() """
        # 1. create_report()
        resp = self.test_create_report()
        report_id = int(json.loads(resp.content).get('id'))

        # 2. get_report()
        resp = self.reporter.get_report(report_id)
        expected_code = 200
        actual_code = resp.status_code
        failure_msg = ("get_report(): Expected response status code to be "
                       "{0} but it was {1}".format(expected_code, actual_code))
        assert actual_code == expected_code, failure_msg


    def test_list_reports(self):
        """ test_list_reports() """
        # 1. create_report()
        self.test_create_report()

        # 2. list_reports()
        resp = self.reporter.list_reports()
        expected_code = 200
        actual_code = resp.status_code
        failure_msg = ("list_reports(): Expected response status code to be "
                       "{0} but it was {1}".format(expected_code, actual_code))
        assert actual_code == expected_code, failure_msg

        # 3. list_reports() content
        assert resp.content, "list_reports(): No items in the list"

    def test_create_result(self):
        """ test_create_result() """
        # 1. create_report()
        resp = self.test_create_report()
        report_id = int(json.loads(resp.content).get('id'))

        # 2. create_result()
        mandatory_data = {
            "report": report_id,
            "scenario_name": 'test_scenario_name',
            "status": 'test_status',
            "gherkin_table_rows": 'test_gherkin_table_rows',
            "gherkin_table_headers": 'gherkin_table_headers'
        }
        resp = self.reporter.create_result(**mandatory_data)
        expected_code = 201
        actual_code = resp.status_code
        failure_msg = ("create_result(): Expected response status code to be "
                       "{0} but it was {1}".format(expected_code, actual_code))
        assert actual_code == expected_code, failure_msg
        return resp

    def test_get_report_results(self):
        """ test get_report_results() """
        # 1. create_report(), create_result()
        resp = self.test_create_result()

        # 2. get_report_results
        report_id = int(json.loads(resp.content).get('report'))
        resp = self.reporter.get_report_results(report_id)
        expected_code = 200
        actual_code = resp.status_code
        failure_msg = ("get_report_results(): Expected response status code to "
                       "be {0} but it was {1}".format(
                           expected_code, actual_code))
        assert actual_code == expected_code, failure_msg


if __name__ == '__main__':
    unittest.main(failfast=True)
