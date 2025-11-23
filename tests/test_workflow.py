from micro_traversal.workflow import validate_workflow

def test_valid_workflow():
    doc = {"steps": [{"type": "goto", "url": "https://example.com"}]}
    errs = validate_workflow(doc)
    assert errs == []

def test_invalid_type():
    doc = {"steps": [{"type": "unknown"}]}
    errs = validate_workflow(doc)
    assert errs and isinstance(errs, list)