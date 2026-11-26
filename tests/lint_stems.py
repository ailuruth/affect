"""The label lint's own stem table (spec §7.4) and the situation-word list (spec §3.3, A15).

This file is on the lint's allowlist (spec §7.4 item iv): it has to spell the words it refuses. Nothing imports
it except the lint (tools/lint_labels.py) and the tests. Adding or removing a stem is a reviewed change.
Every pattern is matched against one whole lower-case token (re.fullmatch); a trailing ".*" makes it a stem.
"""

STEMS = (
    r"emotion.*", r"emotiv.*", r"happ(y|ier|iest|ily|iness)", r"unhapp.*", r"sad", r"sadd.*", r"sadly", r"sadness",
    r"joy.*", r"enjoy.*", r"grief.*", r"griev.*", r"anger.*", r"angr.*", r"fear.*", r"afraid", r"disgust.*",
    r"contempt.*", r"shame.*", r"asham.*", r"guilt.*", r"pride", r"proud.*", r"worr.*", r"anxi.*", r"sympath.*",
    r"empath.*", r"concern.*", r"mood.*", r"distress.*", r"relief.*", r"reliev.*", r"hurt.*", r"glad.*",
    r"surprise", r"surprised", r"surprises", r"surprising", r"surprisingly",
    r"love", r"loved", r"loves", r"loving", r"hate", r"hated", r"hates", r"hatred", r"lonel.*", r"bored",
    r"boredom", r"upset.*", r"frustrat.*", r"nervous.*", r"scare.*", r"scary", r"calm.*",
    r"excite", r"excited", r"excitement", r"exciting",
    r"sentiment.*", r"valence.*", r"arous.*", r"feeling.*", r"care", r"cares", r"caring", r"affective",
    r"affection.*",
)

# Lint self-test (spec §7.4): each spelling class must fail; the near misses must pass.
MUST_FAIL = ("is_sad", "fearLevel", "joy-gain", "Emotions", "moods", "go_emotions", "relievedFlag",
             "roberta-base-go_emotions", "HTTPMoodX2", "isHappy", "SADNESS", "care", "unhappyCount", "calm2")
MUST_PASS = ("career", "feature", "surprisal", "excitation", "glove", "affect", "sadhu", "caret", "excitation_source")

# Situation words (spec §3.3): no INNATE.lock key, unit or comment may contain one, nor an emotion stem above.
# Multi-word entries match consecutive tokens; single words match as stems (token prefix).
SITUATION_WORDS = (
    "arrival", "arrive", "mourn", "mourning", "funeral", "death", "bereave", "grief", "griev", "joke", "tease",
    "bad_news", "news", "greeting", "greet", "goodbye", "farewell", "welcome", "insult", "apology", "compliment",
    "flirt", "argument", "fight", "crisis", "illness", "sick", "stranger", "child", "elderly", "user_type", "scene",
    "situation",
)
SITUATION_MUST_FAIL = ("greeting_flash", "arrivalGain", "bad-news-mask", "mourner_delay", "user_type_prior")
SITUATION_MUST_PASS = ("ledger_kappa", "drive_terms", "contact_known_min", "nested_tokens")
