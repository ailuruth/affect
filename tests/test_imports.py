"""Import and call denylist (spec §7.2, §7.4): no affect classifier, no face recognition, no API-key client, no
transformers pipeline or classification head; engine/ never imports eval/."""
import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DENY_PACKAGES = {"fer", "deepface", "hsemotion", "feat", "opensmile", "speechbrain", "face_recognition",
                 "insightface", "anthropic", "openai"}
HEAD_SUFFIXES = ("ForSequenceClassification", "ForAudioClassification", "ForImageClassification")


def violations(src: str, path: str = "<src>", in_engine: bool = False) -> list:
    out = []
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                top = a.name.split(".")[0]
                if top in DENY_PACKAGES:
                    out.append((path, n.lineno, f"import {a.name}"))
                if in_engine and top == "eval":
                    out.append((path, n.lineno, "engine imports eval"))
        elif isinstance(n, ast.ImportFrom) and n.module:
            top = n.module.split(".")[0]
            if top in DENY_PACKAGES:
                out.append((path, n.lineno, f"from {n.module}"))
            if in_engine and top == "eval":
                out.append((path, n.lineno, "engine imports eval"))
            for a in n.names:
                if a.name.endswith(HEAD_SUFFIXES) or (top == "transformers" and a.name == "pipeline"):
                    out.append((path, n.lineno, f"from {n.module} import {a.name}"))
        elif isinstance(n, ast.Attribute):
            if n.attr.endswith(HEAD_SUFFIXES):
                out.append((path, n.lineno, n.attr))
            if n.attr == "pipeline" and isinstance(n.value, ast.Name) and n.value.id == "transformers":
                out.append((path, n.lineno, "transformers.pipeline"))
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "__import__":
            arg = n.args[0] if n.args else None
            if isinstance(arg, ast.Constant) and str(arg.value).split(".")[0] in DENY_PACKAGES:
                out.append((path, n.lineno, "__import__"))
        elif isinstance(n, ast.Constant) and n.value in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
            out.append((path, n.lineno, "API key variable"))
    return out


def test_repository_clean():
    bad = []
    for top in ("engine", "eval", "tools"):
        for p in sorted((ROOT / top).rglob("*.py")) if (ROOT / top).exists() else []:
            bad += violations(p.read_text(encoding="utf-8"), str(p.relative_to(ROOT)), in_engine=top == "engine")
    assert bad == []


@pytest.mark.parametrize("src", [
    "import deepface", "from speechbrain.inference import X", "import transformers\ntransformers.pipeline('x')",
    "from transformers import pipeline", "from transformers import BertForSequenceClassification",
    "import transformers as t\nm = t.Wav2Vec2ForAudioClassification", "import anthropic",
    "import os\nos.environ['ANTHROPIC_API_KEY']", "__import__('fer')",
])
def test_denylist_fires(src):
    assert violations(src)


def test_engine_never_imports_eval():
    assert violations("from eval import events", in_engine=True)
    assert violations("import eval.config", in_engine=True)
    assert not violations("import numpy as np\nfrom scipy.signal import lfilter")
