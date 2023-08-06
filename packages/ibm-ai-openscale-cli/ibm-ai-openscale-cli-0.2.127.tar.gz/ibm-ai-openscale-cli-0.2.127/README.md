# ibm-ai-openscale-cli
![Status](https://img.shields.io/badge/status-beta-yellow.svg)
[![Latest Stable Version](https://img.shields.io/pypi/v/ibm-ai-openscale-cli.svg)](https://pypi.python.org/pypi/ibm-ai-openscale-cli)

IBM Watson Openscale "fastpath" configuration tool. This tool allows the user to get started quickly with Watson OpenScale.
* If needed, provision a Lite plan instance for IBM Watson OpenScale
* If needed, provision a Lite plan instance for IBM Watson Machine Learning
* Drop and re-create the IBM Watson OpenScale datamart instance and datamart database schema
* Optionally, deploy a sample machine learning model to the WML instance
* Configure the sample model instance to OpenScale, including payload logging, fairness checking, feedback, quality checking, and explainability
* Optionally, store up to 7 days of historical payload, fairness, and quality data for the sample model

## What's new in this release
* Added `--protect-datamart` option, which if specified, exits the setup in case an existing datamart is found, to prevent accidentaly overwriting it
* Other bug fixes and stability improvements

## Before you begin
* You need an [IBM Cloud][ibm_cloud] account.
* Create an [IBM Cloud API key](https://console.bluemix.net/docs/iam/userid_keys.html#userapikey)
* If you already have a Watson Machine Learning (WML) instance, ensure it's RC-enabled, learn more about this in the [migration instructions](https://console.bluemix.net/docs/resources/instance_migration.html#migrate).

## Installation

To install, use `pip` or `easy_install`:

```bash
pip install -U ibm-ai-openscale-cli
```

or

```bash
easy_install -U ibm-ai-openscale-cli
```

## Usage

```
ibm-ai-openscale-cli --help

usage: ibm-ai-openscale-cli [-h] (-a APIKEY | -i IAM_TOKEN)
                            [--env {ypprod,ypqa,ys1dev,icp}]
                            [--resource-group RESOURCE_GROUP]
                            [--postgres POSTGRES]
                            [--postgres-json POSTGRES_JSON] [--icd ICD]
                            [--icd-json ICD_JSON] [--db2 DB2]
                            [--db2-json DB2_JSON] [--wml WML]
                            [--wml-json WML_JSON] [--azure AZURE]
                            [--azure-json AZURE_JSON] [--spss SPSS]
                            [--spss-json SPSS_JSON] [--custom CUSTOM]
                            [--custom-json CUSTOM_JSON] [--aws AWS]
                            [--aws-json AWS_JSON]
                            [--deployment-name DEPLOYMENT_NAME]
                            [--keep-schema] [--username USERNAME]
                            [--password PASSWORD] [--url URL]
                            [--datamart-name DATAMART_NAME]
                            [--history HISTORY] [--history-only]
                            [--model {all,GermanCreditRiskModel,DrugSelectionModel,GolfModel}]
                            [--custom-model CUSTOM_MODEL]
                            [--custom-model-directory CUSTOM_MODEL_DIRECTORY]
                            [--extend] [--protect-datamart]
                            [--reset {metrics,monitors,datamart,model,all}]
                            [--verbose] [--version]

IBM Watson Openscale "fastpath" configuration tool. This tool allows the user
to get started quickly with Watson OpenScale: 1) If needed, provision a Lite
plan instance for IBM Watson OpenScale 2) If needed, provision a Lite plan
instance for IBM Watson Machine Learning 3) Drop and re-create the IBM Watson
OpenScale datamart instance and datamart database schema 4) Optionally, deploy
a sample machine learning model to the WML instance 5) Configure the sample
model instance to OpenScale, including payload logging, fairness checking,
feedback, quality checking, and explainability 6) Optionally, store up to 7
days of historical payload, fairness, and quality data for the sample model

optional arguments:
  -h, --help            show this help message and exit
  --env {ypprod,ypqa,ys1dev,icp}
                        Environment. Default "ypprod"
  --resource-group RESOURCE_GROUP
                        Resource Group to use. If not specified, then
                        "default" group is used
  --postgres POSTGRES   Path to postgres credentials file for the datamart
                        database. If --postgres, --icd, and --db2 all are not
                        specified, then the internal Watson OpenScale database
                        is used
  --postgres-json POSTGRES_JSON
                        Postgres credentials in JSON format
  --icd ICD             Path to IBM Cloud Database credentials file for the
                        datamart database
  --icd-json ICD_JSON   IBM Cloud Database credentials for the datamart
                        database in JSON format
  --db2 DB2             Path to IBM DB2 credentials file for the datamart
                        database
  --db2-json DB2_JSON   IBM DB2 credentials for the datamart database in JSON
                        format: '{ "username": "<USERNAME>", "password":
                        "<PASSWORD>", "hostname": "<hostname>", "port":
                        "<port>", "db": "<db>" }'
  --wml WML             Path to IBM WML credentials file
  --wml-json WML_JSON   IBM WML credentials in JSON format
  --azure AZURE         Path to Microsoft Azure credentials file
  --azure-json AZURE_JSON
                        Microsoft Azure credentials in JSON format: '{
                        "client_id": "<CLIENT_ID", "client_secret":
                        "<CLIENT_SECRET", "tenant": "<TENANT>",
                        "subscription_id": "<SUBSCRIPTION_ID" }'
  --spss SPSS           Path to SPSS credentials file
  --spss-json SPSS_JSON
                        SPSS credentials in JSON format: '{ "username":
                        "<USERNAME>", "password": "<PASSWORD", "url": "<URL>"
                        }'
  --custom CUSTOM       Path to Custom Engine credentials file
  --custom-json CUSTOM_JSON
                        Custom Engine credentials in JSON format: '{ "url":
                        "<URL>" }'
  --aws AWS             Path to Amazon Web Services credentials file
  --aws-json AWS_JSON   Amazon Web Services credentials in JSON format: '{
                        "access_key_id": "<ACCESS_KEY_ID",
                        "secret_access_key": "<SECRET_ACCESS_KEY", "region":
                        "<REGION>" }'
  --deployment-name DEPLOYMENT_NAME
                        Name of the existing deployment to use. Required for
                        Azure ML Studio, SPSS Engine and Custom ML Engine, but
                        optional for Watson Machine Learning. Required for
                        custom models
  --keep-schema         Use pre-existing datamart schema, only dropping all
                        tables. If not specified, datamart schema is dropped
                        and re-created
  --username USERNAME   ICP username. Required if "icp" environment is chosen,
                        not required if --iam-token is specified
  --password PASSWORD   ICP password. Required if "icp" environment is chosen,
                        not required if --iam-token is specified
  --url URL             ICP url. Required if "icp" environment is chosen
  --datamart-name DATAMART_NAME
                        Specify data mart name and database schema, default is
                        the datamart database connection username. For
                        internal database, the default is "wosfastpath"
  --history HISTORY     Days of history to preload. Default is 7
  --history-only        Store history only for existing deployment and
                        datamart. Requires --extend and --deployment-name also
                        be specified
  --model {all,GermanCreditRiskModel,DrugSelectionModel,GolfModel}
                        Sample model to set up with Watson OpenScale (default
                        "GermanCreditRiskModel")
  --custom-model CUSTOM_MODEL
                        Name of custom model to set up with Watson OpenScale.
                        If specified, overrides the value set by --model. Also
                        requires that --custom-model-directory
  --custom-model-directory CUSTOM_MODEL_DIRECTORY
                        Directory with model configuration and metadata files.
                        Also requires that --custom-model be specified
  --extend              Extend existing datamart, instead of deleting and
                        recreating it
  --protect-datamart    If specified, the setup will exit if an existing
                        datamart setup is found
  --reset {metrics,monitors,datamart,model,all}
                        Reset existing datamart and/or sample models then exit
  --verbose             verbose flag
  --version             show program's version number and exit

required arguments (only one needed):
  -a APIKEY, --apikey APIKEY
                        IBM Cloud platform user APIKey. If "--env icp" is also
                        specified, APIKey value is not used.
  -i IAM_TOKEN, --iam-token IAM_TOKEN
                        IBM Cloud authentication IAM token, or IBM Cloud
                        private authentication IAM token. Format can be
                        (--iam-token "Bearer <token>") or (--iam-token
                        <token>)
```

## Examples

In this example, if a WML instance already exists it is used, but if not a new Lite plan instance is provisioned and used.
If an OpenScale instance exists, its datamart is dropped and recreated along with its datamart internal database schema.
Otherwise, a Lite plan OpenScale instance is provisioned.
The GermanCreditRiskModel is stored and deployed in WML, configured to OpenScale, and 7 days' historical data stored.

```sh
export APIKEY=<PLATFORM_API_KEY>
ibm-ai-openscale-cli --apikey $APIKEY
```

In this example, assume the user already has provisioned instances of WML, OpenScale, IBM Cloud Database for Postgres (ICD), and has selected a schema for the OpenScale datamart database.
The OpenScale datamart is dropped and recreated, and the datamart's database schema is dropped and recreated.
An already-deployed instance of the DrugSelectionModel is configured to OpenScale, and 7 days' historical data stored.

```sh
export APIKEY=<PLATFORM_API_KEY>
export WML=<WML instance credentials JSON file>
export ICD=<ICD instance credentials JSON file>
export SCHEMA=<ICD database schema>
ibm-ai-openscale-cli --apikey $APIKEY --wml $WML --model DrugSelectionModel --deployment-name DrugSelectionModelDeployment --icd $ICD --datamart-name $SCHEMA
```

In this example, assume the user already has provisioned an Entry plan instance of IBM DB2 Warehouse on Cloud.
The OpenScale datamart's tables within the user's existing DB2 schema are dropped and recreated.
The GermanCreditRiskModel is stored and deployed in WML, configured to OpenScale, and 7 days' historical data stored.

```sh
export APIKEY=<PLATFORM_API_KEY>
export DB2=<DB2 instance credentials JSON file>
export SCHEMA=<user's DB2 database schema>
ibm-ai-openscale-cli --apikey $APIKEY --db2 $DB2 --datamart-name $SCHEMA --keep-schema
```

In this example, assume the user has their own custom model named MyBusinessModel stored in WML and deployed as MyBusinessModelDeployment.
Also assume they already have a provisioned instance of OpenScale which has not yet been configured.
In the custom model directory, the user has provided a `configuration.json` file with the required model configuration details.
The OpenScale datamart and datamart database schema are created, and the MyBusinessModelDeployment is configured to OpenScale.
```sh
export APIKEY=<PLATFORM_API_KEY>
export WML=<WML instance credentials JSON file>
export MODELPATH=<path to custom model directory>
ibm-ai-openscale-cli --apikey $APIKEY --wml $WML --custom-model MyBusinessModel --deployment-name MyBusinessModelDeployment --custom-model-directory $MODELPATH
```

## FAQ

### Q: What is the GermanCreditRiskModel sample model?

A. The GermanCreditRiskModel sample model is taken from the "Watson Studio, Watson Machine Learning and Watson OpenScale samples"
[GitHub repo](https://github.com/pmservice/), specifically the IBM Watson OpenScale [tutorials](https://github.com/pmservice/ai-openscale-tutorials).
When you run fastpath to deploy and configure the GermanCreditRiskModel, the result will be as if you had run the tutorial notebook appropriate
for your machine learning engine.

### Q: How do the reset options work?

A: The reset options each affect a different level of data in the datamart:

* `--reset metrics` : Clean up the payload logging table, monitoring history tables etc, so that it restores the system to a fresh state with datamart configured, model deployments added, all monitors configured, but no actual metrics in the system yet. The system is ready to go. Not supported for Watson OpenScale internal databases.
* `--reset monitors` : Remove all configured monitors and corresponding metrics and history, but leave the actual model deployments (if any) in the datamart. User can proceed to configure the monitors via user interface, API, or fastpath.
* `--reset datamart` : "Factory reset" the datamart to a fresh state as if there was not any configuration.
* `--reset model` : Delete the sample models and deployments from WML. Not yet supported for non-WML engines. Does not affect the datamart.
* `--reset all` : Reset both the datamart and sample models.

### Q: Can I use SSL for connecting to the datamart DB2 database?

A: Yes. DB2 Warehouse on Cloud databases automatically support SSL, using the VCAP json file generated on the "Service Credentials" page.
For on-prem or ICP4D DB2 databases, you can specify the path on the local client machine to a copy of the DB2 server's SSL certificate "arm" file,
using an "ssldsn" connection string in the VCAP json file:

```
{
  "hostname": "<ipaddr>",
  "host": "<ipaddr>",
  "username": "<uid>",
  "password": "<pw>",
  "port": 50000,
  "jdbcurl": "jdbc:db2://<ipaddr>:50000/<dbname>",
  "uri": "db2://<uid>:<pw>@<ipaddr>:50000/<dbname>",
  "db": "<dbname>",
  "dsn": "DATABASE=<dbname>;HOSTNAME=<ipaddr>;PORT=50000;PROTOCOL=TCPIP;UID=<uid>;PWD=<pw>",
  "ssldsn": "DATABASE=<dbname>;HOSTNAME=<ipaddr>;PORT=50001;PROTOCOL=TCPIP;UID=<uid>;PWD=<pw>;Security=ssl;SSLServerCertificate=/path_on_local_client_machine_to/db2server_instance.arm;"
}
```

If SSL connections are not needed, or not configured on the DB2 server, you can remove the "ssldsn" tag and ibm-ai-openscale-cli will use the non-SSL "dsn" tag instead.
If the VCAP has both dsn and ssldsn tags, ibm-ai-openscale-cli will use "ssldsn" tag to create an SSL connection.

### Q: What are the contents of a custom model directory?

A: These files are used to configure a custom model to IBM Watson OpenScale:

Required
*  `configuration.json`: the model configuration details

Optional
*  `model_content.gzip`: exported model file from WML, loaded and deployed in WML if `--deployment-name` is not specified
*  `model_meta.json`: exported model metadata from WML (required if model gzip is provided)
*  `pipeline_content.gzip`: exported model pipeline file from WML, loaded and deployed in WML if `--deployment-name` is not specified
*  `pipeline_meta.json`: exported model pipeline metadata from WML (required if pipeline gzip is provided)

#### Syntax of configuration.json

A JSON file that specifies the OpenScale configuration for the model. The key components are:
*  `asset_metadata` (required): top-level model specification elements
*  `training_data_reference` (required): reference to the model training data csv in COS
*  `training_data_type` (optional): required if there are any numeric-valued model features
*  `quality_configuration` (optional): if applicable for the model
*  `fairness_configuration` (optional): if applicable for the model

Valid values for parameters in `asset_metadata`:
*  `problem_type`: `REGRESSION`, `BINARY_CLASSIFICATION`, `MULTICLASS_CLASSIFICATION`
*  `input_data_type`: `STRUCTURED`

Here is an example:

```
{
    "asset_metadata": {
        "problem_type": "BINARY_CLASSIFICATION",
        "input_data_type": "STRUCTURED",
        "label_column": "Risk",
        "prediction_column": "Scored Labels",
        "probability_column": "Scored Probabilities",
        "categorical_columns": [ "CheckingStatus" ],
        "feature_columns": [ "CheckingStatus", "LoanDuration", "Age" ]
    },
    "training_data_reference": {
        "credentials" : {<IBM Cloud COS credentials>},
        "path" : "<path within COS to training data csv file (bucket name + / + filename)>",
        "firstlineheader": "True"
    },
    "training_data_type": { "LoanDuration": "int", "Age": "int" },
    "quality_configuration": { "threshold": 0.95, "min_records": 40 },
    "fairness_configuration": {
        "features": [
            {
                "feature": "Age",
                "majority": [[ 26, 75 ]],
                "minority": [[ 18, 25 ]],
                "threshold": 0.98
            }
        ],
        "favourable_classes": [ "No Risk" ],
        "unfavourable_classes": [ "Risk" ],
        "min_records": 100
    }
}
```

#### Syntax of `training_data.csv`

A CSV file of the data used to train the model.
This data is also used by live scoring requests to the model using the range of actual values for each feature from the training data.
A header row is required, with column names that match the model's feature names.
Any column with numeric values must be included in the `training_data_type` specification in the `configuration.json`.
A typical example:
```
CheckingStatus,LoanDuration,Age,Risk
no_checking,28,30,Risk
0_to_200,28,27,No Risk
. . .
```


## Python version

Tested on Python 3.5, 3.6, and 3.7.

## Contributing

See [CONTRIBUTING.md][CONTRIBUTING].

## License

This library is licensed under the [Apache 2.0 license][license].

[ibm_cloud]: https://cloud.ibm.com
[responses]: https://github.com/getsentry/responses
[requests]: http://docs.python-requests.org/en/latest/
[CONTRIBUTING]: ./CONTRIBUTING.md
[license]: http://www.apache.org/licenses/LICENSE-2.0
