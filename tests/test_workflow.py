from micro_traversal.workflow import validate_workflow

def test_valid_goto():
    doc = {"steps": [{"type": "goto", "url": "https://example.com"}]}
    assert validate_workflow(doc) == []

def test_invalid_goto_missing_url():
    doc = {"steps": [{"type": "goto"}]}
    assert validate_workflow(doc)

def test_valid_click_selector():
    doc = {"steps": [{"type": "click", "selector": "#login"}]}
    assert validate_workflow(doc) == []

def test_valid_click_template_only():
    doc = {"steps": [{"type": "click", "template": "login.png"}]}
    assert validate_workflow(doc) == []

def test_invalid_click_missing_both():
    doc = {"steps": [{"type": "click"}]}
    assert validate_workflow(doc)

def test_valid_fill():
    doc = {"steps": [{"type": "fill", "selector": "#user", "value": "alice"}]}
    assert validate_workflow(doc) == []

def test_invalid_fill_missing_value():
    doc = {"steps": [{"type": "fill", "selector": "#user"}]}
    assert validate_workflow(doc)

def test_valid_wait():
    doc = {"steps": [{"type": "wait", "timeout": 1000}]}
    assert validate_workflow(doc) == []

def test_invalid_wait_missing_timeout():
    doc = {"steps": [{"type": "wait"}]}
    assert validate_workflow(doc)

def test_invalid_type():
    doc = {"steps": [{"type": "unknown"}]}
    errs = validate_workflow(doc)
    assert errs and isinstance(errs, list)