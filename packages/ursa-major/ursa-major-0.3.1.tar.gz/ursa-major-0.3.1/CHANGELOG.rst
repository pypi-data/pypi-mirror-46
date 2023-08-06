Change Logs
===========

0.2.2 (2019-03-26)
------------------

* For adding tag, allow filtering on buildrequires to find out koji_tags from
  tag inheritance (Chenxiong Qi)

0.2.1 (2019-03-20)
------------------

* Make setup_method/teardown_method compatible with newer version of pytest (Chenxiong Qi)
* Add missing file CHANGELOG.rst to sdist package (Chenxiong Qi)

0.2.0 (2019-03-20)
------------------

* Add tests for AddModuleHandler methods (Chenxiong Qi)
* Avoid long modulemd embedded into fake data for tests (Chenxiong Qi)
* Fixes according to review comments (Chenxiong Qi)
* Command check-config supports filtering modules on buildrequires (Chenxiong Qi)
* Command add-module supports buildrequires now (Chenxiong Qi)
* Command remove-module supports filtering modules on buildrequires (Chenxiong Qi)
* Allow passing buildrequires to MBS.get_modules_with_requires (Chenxiong Qi)
* Reword remove-module help and --tag option help text (Chenxiong Qi)
* Allow filtering on buildrequires (Chenxiong Qi)

