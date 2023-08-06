## README

Python API wrapper for the 'Crackle Automation Reporter Web Service'

The API is used to take the result of test scenarios and generate different types of analytics reports from that data.
Typical client flow is:
1. Create a Report object at the start of a test run
2. Create a Result object for each new test scenario result and associate it with the Report
3. Reports get generated at the web service
4. Get the desired reports from the API and use them in Test Reporting

## Installation
`pip install crackle-automation-api-client`

## Usage

1. `python3`
2. `from crackle_automation_api_client.api_wrapper import Reporter`
3. `reporter = Reporter(host=host, username=username, password=password)`
4. `response = reporter.list_reports()`
5. `...`

## Available API methods:

Report:
- list_reports()
- get_report(report_id)
- create_report(testrail_base_url, testrail_test_run, platform, environment, name, publish_html_report)
- delete_report(report_id)
- publish_html_master_report(report_id)
- get_report_results(report_id)

Result:
- list_results()
- get_result(result_id)
- get_result_single_report(result_id)
- create_result(result_id)

## Unit tests

To run unit tests:

1. `pip install crackle_automation_api_client` or with `pipenv` if in the virtualenv
2. `cd crackle_automation_api_client`
2. `reporting_service_url='<url_to_api_root>' reporting_service_user=<username> reporting_service_password=<password> python tests.py Tests`

- reporting_service_url - the full url of the API root (no trailing slash)
- reporting_service_user - the username of a user at the API
- reporting_service_password - the password of the user at the API

### Development

Use pipenv to enter a virtualenv with:
`pipenv --python 3.6 install && pipenv shell`

Verify changes with pylint:
`pylint_runner`

Finally run all unit tests



### Deploying this package to PyPi (pip)

When changes are made to this package you must deploy it as a new version to PyPi in order for it to be made available to pip.

1. Delete all files under dist/
2. Bump the version in setup.py and make any other changes to this file
3. Commit all changes to the repo
4. run `python3 setup.py sdist bdist_wheel` to create the new package
5. run `twine upload dist/*` to upload the package to PyPi (pip)


### Configuring Twine for deployment to PyPi

Note twine may need to be configured on your machine to point to production PyPi, refer to the
Python packaging documentation here: https://packaging.python.org/tutorials/packaging-projects/
The configured user account must be owner of the package on PyPi.

Example ~/.pypirc file:

```
[distutils]
index-servers =
    pypi
    pypitest

[pypi]
username:<username>
password:<password>

[pypitest]
repository=https://testpypi.python.org/pypi
username=<username>
password=<password>
```

Package URL: https://pypi.org/manage/project/crackle-automation-api-client/
