"""R-2 axiom:interpersonal_transparency; correct-forward #98, sensor protection kept."""

import hashlib
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _axiom():
    data = yaml.safe_load((ROOT / "axioms/registry.yaml").read_text())
    return next(a for a in data["axioms"] if a["id"] == "interpersonal_transparency")


def test_registry_matches_reviewed_council_text_and_subject_rights():
    axiom = _axiom()
    # Council b130753fff: the reviewed prime text, including the mixed-sensor repair.
    expected = "1a5dbe91cb4bd55173444dcbdecd88476867031310c8c61a3c400ef01243f36c"  # pragma: allowlist secret (reviewed text SHA-256)
    assert hashlib.sha256(axiom["text"].encode()).hexdigest() == expected
    text = " ".join(axiom["text"].split())
    for clause in (
        "users of this system and household or studio sensor subjects",
        "zero jurisdiction over public conduct and discourse of persons of public interest",
        "Household or studio sensor data stays protected whoever the subject is",
        "including persons of public interest",
        "Modeling or understanding behavior and outcomes does not remove this protection",
        "explicit opt-in",
        "inspection access",
        "revocable",
        "purges",
    ):
        assert clause in text
    assert axiom["weight"] == 88 and axiom["status"] == "active"
    assert axiom["purview"] == {
        "type": "subject-data-context-v1",
        "subjects": ["system_user", "household_sensor_subject", "studio_sensor_subject"],
        "data": ["system_user", "household_sensor", "studio_sensor"],
        "outside_subjects": ["public_interest_person", "non_person"],
        "outside_data": ["public_discourse", "behavior_outcome_model", "non_personal"],
        "mixed": "protected_data_prevails",
    }


def test_98_predecessor_is_retained_verbatim_and_other_fields_preserved():
    current = _axiom()
    path, anchor = current["supersedes"].split("#")
    assert anchor == "superseded-registry-text"
    blocks = re.findall(r"```yaml\n(.*?)```", (ROOT / path).read_text(), re.S)
    (block,) = [b for b in blocks if b.startswith("  - id: interpersonal_transparency\n")]
    expected = "885f56cc239935ef2dac5367fdd1177dd107092fed91b16cf0bdf4111a6134a9"  # pragma: allowlist secret (predecessor SHA-256)
    assert hashlib.sha256(block.encode()).hexdigest() == expected
    (prior,) = yaml.safe_load(block)
    changed = {"text", "supersedes", "purview"}
    assert {k: v for k, v in current.items() if k not in changed} == {
        k: v for k, v in prior.items() if k not in changed
    }
