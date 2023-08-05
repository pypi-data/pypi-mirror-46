This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [6.0.1] - 2019-02-27
### Added
* Added send message input in cortex actions client

## [5.6.0] - 2019-02-27
### Added

* Added notebook with a deployment example
* from_model in action_builder no longer allows only sklearn models
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

* ConnectionsClient: Added retry logic for `upload`, `uploadStreaming` and `download`.
* Jupyter notebook examples for pipelines and datasets

### Changed

* Namespace validation on resource creation. You must specify a namespace when creating:
    * datasets
    * skills
    * actions
    * connections
* `RemoteRun.get_artifact()` now returns a deserialized object by default, instead of the serialized object. The function now also has an optional `deserializer` parameter.


### Removed
