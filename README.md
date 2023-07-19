# EDPOP collection ontology

RDF ontology for the [EDPOP VRE](https://github.com/UUDigitalHumanitieslab/EDPOP). This ontology defines the relationships for managing collections of records and making annotation on them.

The interface uses the collection ontology in combination with a record ontology. In the scope of the EDPOP project, this is the [edop record ontology](https://github.com/UUDigitalHumanitieslab/edpop-record-ontology). The project's goal is to manage and annotate collections of library catalogues, which are described by the record ontology. The collection ontology is implemented separately as it is designed to be model-agnostic: it makes minimal assumptions about the data structure of records.

### Repository contents

This repository contains:

- [ontology.ttl](/ontology.ttl): A formal, machine-readable description of the ontology
- [guidelines](/documentation/guidelines.md): A lengthy description of how the ontology can be used in a research environment.
- [example.tt](/documentation/example.ttl): An small graph that implements the ontology.
- [test_validate.py](/tests/test_validate.py): A python test that verifies the turtle files in the repository are valid.

### Unit tests

Validation tests are implemented using pytest and are included in the /tests/ directory. Python 3.x is required for this.

Install requirements with

```bash
pip install tests/requirements.txt
```

Run tests with 

```bash
pytest
```

