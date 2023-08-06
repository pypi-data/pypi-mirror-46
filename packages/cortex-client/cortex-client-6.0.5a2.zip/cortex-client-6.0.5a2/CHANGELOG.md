This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Upgrades from major to major versions, such a change from version `5.6.0` to `6.0.0`, might require local configuration updates to ensure compatibility with your current scripts. Make sure you have the latest version of the SDK using `pip install -U cortex-client`.

## [6.0.4] - 2019-05-01
### Removed
* Notebooks and templates are no longer part of the Python SDK. You can still download example notebooks and templates from the [Cortex documentation](https://docs.cortex-dev.insights.ai/docs/cortex-tools/get-started-sdk/#sdk-example-notebooks-and-templates).
### Added
* User can now specify Docker base image to use when building Actions via iPython magics.

## [6.0.3] - 2019-04-23
### Fixed
* `build_agentclient()` now correctly returns an `AgentClient`.
### Added
* User can now specify Docker base image to use when building Actions via `ActionBuilder.with_base_image()`.

## [6.0.2] - 2019-04-17
### Fixed
* Fixed issue with LocalDataset.to_camel() method. 
### Added
* Added `cleaning_pipeline.ipynb` template notebook.
### Changed
* Changed required description field for sessions client.

## [6.0.1] - 2019-03-16
### Added
* `ActionsClient.send_message()` to send Synapse message.
* `ConnectionClient.upload_directory()` walks a directory and uploads all files to managed content.

## [6.0.0] - 2019-03-11
### Changed
* `from_model` in `ActionBuilder` is no longer limited to scikit-learn models.

  `from_model` used to only support scikit-learn models, and it implicitly installed scikit-learn as a dependency. The method no longer does so and the user is required to add dependencies explicitly via `with_requirements()`. e.g.,
  ```
  builder.action('kaggel/ames-housing-predict') \
    .with_requirements(['scikit-learn>=0.20.0,<1']) \
    .from_model(model, x_pipeline=x_pipe, y_pipeline=y_pipe, target='SalePrice') \
    .build()
  ```


## [5.6.0] - 2019-02-27
### Added

* Added notebook with a deployment example
* New `Cortex.login()` method for interactive (prompt based) login to Cortex.

## [5.5.4] - 2019-02-08
### Added

* `Client.message()` Message constructor method.
* Bug fixes for experiments & runs

## [5.5.3] - 2019-01-31
### Added

* Jupyter notebook example for experiments
* `ActionBuilder.from_model()` now sets numpy dependency to range `>=1.16,<2`


## [5.5.1] - 2019-01-24
### Added

* ConnectionsClient: Added retry logic for `upload`, `uploadStreaming` and `download`. See [Managed Content Retry](#managed-content-retry) for details.
* Jupyter notebook examples for pipelines and datasets.

### Managed Content Retry

Because there is a probability that functions may fail on the initial try but will succeed upon a subsequent try, an automatic retry feature has been added to the `uploadStreaming` and `download` methods.

The automatic retry feature is set to one retry by default. The number of retries is, however, configurable, so you can set the retry variable to any number.

**uploadStreaming method**

The uploadStreaming method is called when a data scientist wants to pull curated data into a managed content (S3) file.

If you do not specify <retries> as retries=<#>, the function will automatically retry once. If you specify a number the function will be retried that number of times.

In the example below the parts of the function are as follows:

- **cc** = an instance of the ConnectionClient, which is instantiated as `cc = ConnectionClient(CORTEX_URL, 2, CORTEX_TOKEN)`
- **`uploadStreaming`** = the method that is being called to pull in data from a data source and store it as managed content
- **key name** = the path where the file is to be stored
- **stream** = the file object being store
- **content type** = the type of file to store (e.g. _text/csv_)
- **retries** = the number of times to retry the function

**Command**: `cc.uploadStreaming(<key name>, <stream>, <content type>, <retries>)`

**Example**: `cc.uploadStreaming(path/to/datafile, dataFile1, text/csv, retries=5)`

**download method**

The `download` method is called when a data scientist wants to download data from a managed content (S3) file to be used in a workbook or pipeline.

The `download` method also has the retry feature.

In the example below the parts of the function are as follows:

- **cc** = an instance of the ConnectionClient, which is instantiated as `cc = ConnectionClient(CORTEX_URL, 2, CORTEX_TOKEN)`
- **`download`** = the method that is being called to pull in data from a data source and store it as managed content in Skill Lab
- **key name** = the path where the file is stored
- **retries** = the number of times to retry the function


**Command**: `cc.download(<key name>, <retries>)`

**Example**: `cc.download(path/to/datafile, retries = 10)`

For more details about the `uploadStreaming` and `download` methods see the **`connectionClient` Class** in the [Cortex Python Lib reference guide](https://docs.cortex.insights.ai/docs/reference-guides/cortex-python-lib/#clients).


### Changed

* Namespace validation on resource creation. You must specify a namespace when creating:
    * datasets
    * skills
    * actions
    * connections
* `RemoteRun.get_artifact()` now returns a deserialized object by default, instead of the serialized object. The function now also has an optional `deserializer` parameter.
