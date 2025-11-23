from typing import Any, Dict, List
from jsonschema import validate, Draft7Validator

SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["goto", "click", "fill", "wait"]},
                    "url": {"type": "string"},
                    "selector": {"type": "string"},
                    "template": {"type": "string"},
                    "value": {"type": ["string", "number", "boolean"]},
                    "timeout": {"type": "number"}
                },
                "required": ["type"],
                "additionalProperties": False,
                "oneOf": [
                    {"properties": {"type": {"const": "goto"}, "url": {"type": "string"}}, "required": ["type", "url"]},
                    {"properties": {"type": {"const": "click"}, "selector": {"type": "string"}, "template": {"type": "string"}}, "required": ["type"], "anyOf": [{"required": ["selector"]}, {"required": ["template"]}]},
                    {"properties": {"type": {"const": "fill"}, "selector": {"type": "string"}, "value": {"type": ["string", "number", "boolean"]}}, "required": ["type", "selector", "value"]},
                    {"properties": {"type": {"const": "wait"}, "timeout": {"type": "number"}}, "required": ["type", "timeout"]}
                ]
            }
        }
    },
    "required": ["steps"],
    "additionalProperties": False
}

def validate_workflow(doc: Dict[str, Any]) -> List[str]:
    v = Draft7Validator(SCHEMA)
    errors = []
    for e in v.iter_errors(doc):
        errors.append(e.message)
    return errors