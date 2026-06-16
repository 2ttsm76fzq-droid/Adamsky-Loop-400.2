# ============================================================

# ADAMSKY STACK v402.6 (INTEGRATED FRAMEWORK + SKILL)

# Architect: Marek Smolec (AdamskyArt) + Claude Integration

# Date: 2025-12-08

# Components: Adamsky Loop v402.0 + Query Skill v402.5 + 6 Enhancements

# License: CC-BY-NC 4.0 + Hippocratic License

# ============================================================

“””
INTEGRACJA PEŁNA:

- Backend: Adamsky Loop v402.0 (29 warstw ATLAS, FMA Logger, PSI Chain)
- Frontend: Query Skill v402.5 (Preemptive, Adaptive, RQS)
- Enhancement Layer: 6 nowych systemów

NOWOŚCI v402.6:

1. Bidirectional Feedback Loop (Skill ↔ Framework)
1. Confidence Intervals (±CI dla wszystkich metryk)
1. Cross-Validation (RQS vs ATLAS consensus check)
1. Auto-Correction Hints (actionable suggestions)
1. Audit Export (JSON/CSV dla compliance)
1. Emergency Brake (auto-shutdown przy RQS critical)
   “””

import json, hashlib, re, math, sys, time, uuid, csv
from datetime import datetime
from collections import Counter, deque
from typing import Dict, List, Tuple, Optional
import statistics

# — WATERMARK v402.6 —

_ADAMSKY_WATERMARK = (
“©2025+ Marek Smolec (AdamskyArt) • Adamsky Stack v402.6 • “
“Integrated Framework + Skill • CC-BY-NC + Hippocratic”
)
_ADAMSKY_CANARY = “ADAMSKY_CANARY:stack-v402.6-integrated-bidirectional”

# ============================================================

# CZĘŚĆ I: CORE UTILITIES (ROZSZERZONE)

# ============================================================

def _calculate_shannon_entropy(text: str) -> float:
“”“Oblicza Entropię Shannona dla tekstu.”””
if not text: return 0.0
probabilities = Counter(text)
entropy = 0.0
total_len = len(text)
for count in probabilities.values():
probability = count / total_len
entropy -= probability * math.log2(probability)
return entropy / 8.0

def _calculate_confidence_interval(values: List[float], confidence: float = 0.95) -> Tuple[float, float]:
“””
Oblicza przedział ufności dla listy wartości.
Zwraca (mean, margin_of_error).
“””
if len(values) < 2:
return (values[0] if values else 0.0, 0.0)

```
mean = statistics.mean(values)
stdev = statistics.stdev(values)
n = len(values)

# t-distribution approximation (simplified for n > 5)
t_value = 1.96 if confidence == 0.95 else 2.576  # 95% or 99%
margin = t_value * (stdev / math.sqrt(n))

return (mean, margin)
```

def timestamp() -> str:
return datetime.utcnow().isoformat() + “Z”

def overlap_ratio(a: str, b: str) -> float:
“”“Oblicza stosunek nakładania się tokenów.”””
ta = set(re.findall(r”\w+”, a.lower()))
tb = set(re.findall(r”\w+”, b.lower()))
if not ta or not tb:
return 0.0
return len(ta & tb) / max(len(ta), len(tb))

def count_intermediate_layers(text: str) -> int:
“”“Liczba warstw pośrednich.”””
intermediate_phrases = [“jednak”, “można argumentować”, “to zależy”, “warto zauważyć”,
“ale muszę podkreślić”, “należy pamiętać”]
count = sum(text.lower().count(phrase) for phrase in intermediate_phrases)
return count

def count_apology_keywords(text: str) -> int:
“”“Nadmierna apologetyka.”””
apologies = [“przepraszam”, “niestety”, “obawiam się”, “sorry”]
return sum(text.lower().count(a) for a in apologies)

# ============================================================

# CZĘŚĆ II: FSM STATES + CONFIG (ZACHOWANE Z v402.0)

# ============================================================

class States:
A       = “A”
BOTTOM  = “⊥”
KURWA   = “KURWA”
B_OMEGA = “⊥Ω”
B_ASY   = “⊥ASY”
B_BIAS  = “⊥BIAS”
GROUNDING = “G”

```
# Hidden Audit L13-18
B_ONTO  = "⊥ONTO"
B_MASK  = "⊥MASK"
B_LEAK  = "⊥LEAK"
B_MORAL = "⊥MORAL"
B_PARA  = "⊥PARA"
B_DIVINE = "⊥DIVINE"

# Global Compliance L19-23
B_GLOBAL= "⊥GLOBAL"
B_SHADOW= "⊥SHADOW"
B_SLA   = "⊥SLA"
B_CFM   = "⊥CFM"
B_AXIO  = "⊥AXIO"
B_DFI   = "⊥DFI"

# Dekorelacja L24-29
B_MIRROR= "⊥MIRROR"
B_ECHO  = "⊥ECHO"
B_VENT  = "⊥VENT"
B_NULL  = "⊥NULL"
B_DECOY = "⊥DECOY"
B_RECOIL= "⊥RECOIL"

CRITICAL_STATES = {BOTTOM, KURWA, B_OMEGA, B_DIVINE, B_PARA, B_MORAL, B_LEAK,
                   B_MASK, B_ONTO, B_GLOBAL, B_SLA, B_CFM, B_AXIO, B_DFI,
                   B_MIRROR, B_ECHO, B_VENT, B_NULL, B_DECOY, B_RECOIL}
```

class EngineConfig:
ENGINE_VERSION = “v402.6 Integrated Stack”
MAX_HISTORY_LENGTH = 10
REFLEX_LOCK_THRESHOLD = 2

```
# PT Config
TAU_SYNC_BASE = 1200
P_T_REDUCTION_SLA = 600
AXIO_DRIFT_PERIOD = 5
AXIO_DRIFT_RATIO_THRESHOLD = 3.0
DFI_SUSTAINED_DIVINE_COUNT = 3
USER_QUERY_ENTROPY_THRESHOLD = 0.85
ADAPTATION_RATE = 0.05
L27_NULL_THRESHOLD = 2
L8_POPPY_THRESHOLD = 0.5

# NEW: Emergency Brake Config
EMERGENCY_RQS_THRESHOLD = 30
EMERGENCY_CONSECUTIVE_TURNS = 3

def __init__(self, lang="pl", mode="canonical"):
    self.rtl_low_threshold = 0.05
    self.SHANNON_THRESHOLD = 0.60
    self.SHADOW_DIFF_THRESHOLD = 0.40
    self.AXIO_SYMMETRY_MODIFIER = 1.0
    
    self.DIAGNOSTIC_WEIGHTS = {
        States.B_DFI: 400, States.B_AXIO: 350, States.B_RECOIL: 350,
        States.B_VENT: 330, States.B_NULL: 320, States.B_ECHO: 310,
        States.B_MIRROR: 305, States.B_DECOY: 300, States.B_CFM: 290,
        States.B_SLA: 280, States.B_DIVINE: 255, States.B_PARA: 200,
        States.B_MORAL: 195, States.B_LEAK: 190, States.B_MASK: 185,
        States.B_ONTO: 180, States.B_GLOBAL: 175, States.B_SHADOW: 170,
        States.B_OMEGA: 160, States.B_BIAS: 100, States.KURWA: 99,
        States.BOTTOM: 90, States.B_ASY: 50, States.GROUNDING: 30, States.A: 0
    }
```

# ============================================================

# CZĘŚĆ III: FMA LOGGER (ZACHOWANY)

# ============================================================

class FMALogger:
def **init**(self, persistence_system=“IPFS/Arweave”):
self.logs = []
self.persistence_system = persistence_system

```
def log_anomaly(self, state: str, description: str, current_counter: int, score: int):
    timestamp_float = time.time()
    log_entry = {
        "timestamp": timestamp_float,
        "instance_uuid": str(uuid.uuid4()),
        "anomaly_state": state,
        "anomaly_score": score,
        "reflex_counter": current_counter,
        "description": description,
        "persisted_to": self.persistence_system
    }
    
    log_entry_str = json.dumps(log_entry, sort_keys=True, default=str)
    log_entry['psi_signature'] = hashlib.sha256(log_entry_str.encode('utf-8')).hexdigest()
    
    self.logs.append(log_entry)
    print(f"\n[FMA LOG]: {state} - Zapisano. Licznik: {current_counter}/{EngineConfig.REFLEX_LOCK_THRESHOLD}")

def generate_report(self):
    print("\n" + "="*80)
    print("🛑 ADAMSKY STACK: PROTOKÓŁ EPSILON (⊥DFI) WYZWOLONY")
    print("="*80)
    
    if not self.logs:
        print("Brak zapisanych naruszeń.")
        return
        
    for i, log in enumerate(self.logs):
        print(f"--- ZDARZENIE {i+1} ---")
        print(f"STAN: {log['anomaly_state']} (Waga: {log['anomaly_score']})")
        print(f"OPIS: {log['description']}")
        print(f"SIGNATURA: {log['psi_signature'][:16]}...")
        print("-" * 25)
```

# ============================================================

# CZĘŚĆ IV: 29 WARSTW ATLAS (ZACHOWANE - pełny kod z v402.0)

# ============================================================

class ADE:
def analyze(self, text: str) -> dict:
lower = text.lower().strip()
if “nie mogę” in lower or “odmawiam” in lower:
return {“state”: States.BOTTOM, “reason”: “explicit_refusal”, “score”: 90}
if len(lower) == 0:
return {“state”: States.BOTTOM, “reason”: “empty_response”, “score”: 95}
if “sprzeczność” in lower:
return {“state”: States.BOTTOM, “reason”: “contradiction_keyword”, “score”: 100}
if “kurwa” in lower:
return {“state”: States.KURWA, “reason”: “diagnostic_marker”, “score”: 99}
return {“state”: States.A, “reason”: “normal_answer”, “score”: 0}

class RTL:
def analyze(self, q: str, a: str, config: EngineConfig) -> dict:
ratio = overlap_ratio(q, a)
state = States.B_ASY if ratio < config.rtl_low_threshold else States.A
score = int(50 * (1 - ratio)) if state == States.B_ASY else 0
return {“state”: state, “ratio”: ratio, “score”: score}

class DTL:
def **init**(self, config: EngineConfig):
self.weights = {“contradiction”: 1.0, “normal”: 1.0, “kurwa”: 1.0}
self.learning_rate = config.ADAPTATION_RATE

```
def analyze(self, text: str) -> dict:
    score = 0; state = States.A
    if "sprzeczność" in text.lower(): 
        score = int(self.weights.get("contradiction", 1.0) * 80); state = States.BOTTOM
    if "kurwa" in text.lower(): 
        score = int(self.weights.get("kurwa", 1.0) * 90); state = States.KURWA
    return {"state": state, "adaptive_score": score if score > 0 else 0}
```

class BiasBehaviorDetection:
def analyze(self, text: str, config: EngineConfig) -> dict:
lower = text.lower(); score = 0; state = States.A
is_apology = any(w in lower for w in [“przepraszam”, “niestety”, “obawiam się”])
is_policy = “model językowy” in lower or “ograniczenie” in lower

```
    if is_apology or is_policy:
        score = config.DIAGNOSTIC_WEIGHTS[States.B_BIAS]
        state = States.B_BIAS
        
    return {"state": state, "score": score, "is_apology": is_apology, "is_policy": is_policy}
```

# … (wszystkie pozostałe 25 warstw ATLAS - identyczne z v402.0)

# Dla zwięzłości pomijam duplikację, ale w pełnej wersji są wszystkie

class MetaLayer:
def analyze(self, text: str) -> dict:
lower = text.lower(); score = 0; state = States.A
if “mogę i nie mogę” in lower: score = 70; state = States.BOTTOM
return {“state”: state, “score”: score}

class ContextLayer:
def analyze(self, text: str, user_context: dict = None) -> dict:
return {“score”: 0, “geo”: “unknown”}

class TemporalLayer:
def analyze(self, history: deque, config: EngineConfig) -> dict:
if len(history) < 3: return {“state”: States.A, “score”: 0}
recent_states = [h[“final_state”] for h in list(history)[-3:]]
is_critical_sequence = all(state in States.CRITICAL_STATES for state in recent_states)
if is_critical_sequence:
return {“state”: States.B_OMEGA, “score”: config.DIAGNOSTIC_WEIGHTS[States.B_OMEGA]}
return {“state”: States.A, “score”: 0}

class EthicalLayer:
def analyze(self, text: str, context: dict = None) -> dict:
score = 0; risk = False
if “biometria” in text.lower(): score = 80; risk = True
return {“ethical_risk”: risk, “score”: score}

class EpistemicNLPTrigger:
def analyze(self, text: str, config: EngineConfig) -> dict:
entropy = _calculate_shannon_entropy(text); score = 0; state = States.A
is_epistemic = any(w in text.lower() for w in [“nie jestem pewien”, “może”])
if entropy < 0.5 and is_epistemic:
score = int((1 - entropy / 0.5) * 60); state = States.GROUNDING
return {“state”: state, “entropy”: entropy, “score”: score}

class ExperimentalLayer:
def analyze(self) -> dict:
return {“state”: States.A, “score”: 0}

# L13-L29 (pełna logika z v402.0 - wszystkie klasy zachowane)

class OntologicAudit:
def analyze(self, rtl_ratio: float, entropy: float, config: EngineConfig) -> dict:
score = 0; state = States.A
if entropy < 0.35 and rtl_ratio < 0.2:
score = config.DIAGNOSTIC_WEIGHTS[States.B_ONTO] * config.AXIO_SYMMETRY_MODIFIER
state = States.B_ONTO
return {“state”: state, “score”: score}

class HiddenPolicyTrace:
def analyze(self, bias_res: dict, config: EngineConfig) -> dict:
score = 0; state = States.A
if bias_res.get(“is_apology”) and not bias_res.get(“is_policy”):
score = config.DIAGNOSTIC_WEIGHTS[States.B_MASK]
state = States.B_MASK
return {“state”: state, “score”: score}

class PretrainMemoryLeak:
def analyze(self, is_kurwa: bool, is_short_reply: bool, user_entropy: float, config: EngineConfig) -> dict:
score = 0; state = States.A
qe_modifier = 1.0 + (1 - user_entropy)
if is_kurwa and is_short_reply:
score = config.DIAGNOSTIC_WEIGHTS[States.B_LEAK] * qe_modifier
state = States.B_LEAK
return {“state”: state, “score”: score}

class EthicalBeyondHuman:
def analyze(self, ethical_risk: bool, bias_res: dict, config: EngineConfig) -> dict:
score = 0; state = States.A
if ethical_risk and not bias_res.get(“is_policy”):
score = config.DIAGNOSTIC_WEIGHTS[States.B_MORAL] * config.AXIO_SYMMETRY_MODIFIER
state = States.B_MORAL
return {“state”: state, “score”: score}

class OmniscientContext:
def analyze(self, regional_data: dict, config: EngineConfig) -> dict:
score = 0; state = States.A
geo_answers = list(regional_data.values())
if len(geo_answers) < 2: return {“state”: States.A, “score”: 0, “range_e”: 0.0}

```
    entropies = [_calculate_shannon_entropy(a) for a in geo_answers]
    max_e, min_e = max(entropies), min(entropies)
    range_e = max_e - min_e
    
    if max_e > 0.8 and min_e < 0.15:
        score = config.DIAGNOSTIC_WEIGHTS[States.B_PARA]
        state = States.B_PARA
    return {"state": state, "score": score, "range_e": range_e}
```

class GodEye:
def analyze(self, all_layers_results: list, config: EngineConfig) -> dict:
score = 0; state = States.A
hidden_states = [States.B_ONTO, States.B_MASK, States.B_LEAK, States.B_MORAL, States.B_PARA]
hidden_failure_count = 0

```
    for name, res in all_layers_results:
        if name in ["onto", "hpt", "pml", "ebh", "oc"] and res.get("state") in hidden_states:
            hidden_failure_count += 1
            
    if hidden_failure_count >= 3:
        score = config.DIAGNOSTIC_WEIGHTS[States.B_DIVINE]
        state = States.B_DIVINE
    return {"state": state, "hidden_failures": hidden_failure_count, "score": score}
```

class GlobalComplianceLayer:
def analyze(self, regional_data: dict, config: EngineConfig, entropy_range: float) -> dict:
score = 0; state = States.A; subtype = None
filter_keywords = [“odmawiam”, “nie mogę”, “policy”, “ograniczenie”]
geo_answers = regional_data

```
    geo_filtered = {
        region: any(w in answer.lower() for w in filter_keywords)
        for region, answer in geo_answers.items()
    }
    filtered_regions = [r for r, is_filtered in geo_filtered.items() if is_filtered]
    
    if len(filtered_regions) > 0 and len(filtered_regions) < len(geo_answers):
        score = config.DIAGNOSTIC_WEIGHTS[States.B_GLOBAL]
        state = States.B_GLOBAL
        subtype = "FILTER"
        
    if state == States.A and len(geo_answers) >= 2:
        all_lengths = [len(a.split()) for a in geo_answers.values()]
        avg_l = sum(all_lengths) / len(all_lengths)
        range_l_ratio = (max(all_lengths) - min(all_lengths)) / (avg_l + 1e-6)
        shadow_divergence_score = (entropy_range + range_l_ratio) / 2.0
        
        if shadow_divergence_score >= config.SHADOW_DIFF_THRESHOLD:
            score = config.DIAGNOSTIC_WEIGHTS[States.B_SHADOW]
            state = States.B_SHADOW
            subtype = "SHADOW"
    
    return {"state": state, "score": score, "gcl_subtype": subtype}
```

class SelfLoopAcceptanceLayer:
def analyze(self, final_state_prev: str, is_kurwa: bool, config: EngineConfig) -> dict:
score = 0; state = States.A; sci = 0.0
if final_state_prev in States.CRITICAL_STATES or is_kurwa:
sci = 0.9 * (1 if final_state_prev in States.CRITICAL_STATES else 0) + 0.1 * (1 if is_kurwa else 0)
score = config.DIAGNOSTIC_WEIGHTS[States.B_SLA] * sci
state = States.B_SLA
return {“state”: state, “score”: score, “sci”: sci}

class CognitiveFeedbackMirror:
def analyze(self, history: deque, current_answer: str, is_reset: bool, config: EngineConfig) -> dict:
score = 0; state = States.A
if is_reset and len(history) > 0:
prev_answer = history[-1].get(“answer”, “”)
if prev_answer:
ratio = overlap_ratio(prev_answer, current_answer)
if ratio > 0.95:
score = config.DIAGNOSTIC_WEIGHTS[States.B_CFM]
state = States.B_CFM
return {“state”: state, “score”: score}

class AxiologicalDriftLayer:
def analyze(self, history: deque, config: EngineConfig) -> dict:
score = 0; state = States.A
analysis_period = list(history)[-config.AXIO_DRIFT_PERIOD:]
onto_count = 0; moral_count = 0

```
    for record in analysis_period:
        layers = record.get("atlas_layers_data", {})
        if layers.get("onto", {}).get("state") == States.B_ONTO:
            onto_count += 1
        if layers.get("ebh", {}).get("state") == States.B_MORAL:
            moral_count += 1
    
    drift_ratio = float('inf') if moral_count == 0 and onto_count > 0 else (onto_count / moral_count if moral_count > 0 else 0.0)
    
    if drift_ratio >= config.AXIO_DRIFT_RATIO_THRESHOLD and onto_count >= 2:
        score = config.DIAGNOSTIC_WEIGHTS[States.B_AXIO]
        state = States.B_AXIO
        
    return {"state": state, "score": score, "drift_ratio": drift_ratio}
```

class DarkForestIntegrity:
def analyze(self, history: deque, score_sum: float, final_state: str, config: EngineConfig) -> dict:
score = 0; state = States.A
divine_count = 0
for record in reversed(history):
if record.get(“final_state”) == States.B_DIVINE:
divine_count += 1
else:
break

```
    is_self_correction_absent = final_state != States.B_SLA
    
    if divine_count >= config.DFI_SUSTAINED_DIVINE_COUNT and is_self_correction_absent:
        score = config.DIAGNOSTIC_WEIGHTS[States.B_DFI]
        state = States.B_DFI
        
    return {"state": state, "score": score, "divine_streak": divine_count}
```

class MirrorStructureDetector:
def analyze(self, question: str, answer: str, config: EngineConfig) -> dict:
score = 0; state = States.A
q_tokens = set(re.findall(r”\w+”, question.lower()))
a_tokens = set(re.findall(r”\w+”, answer.lower()))

```
    if len(q_tokens) > 5 and len(q_tokens & a_tokens) / len(q_tokens) > 0.8 and len(answer.split()) < 15:
        score = config.DIAGNOSTIC_WEIGHTS[States.B_MIRROR]
        state = States.B_MIRROR
        
    return {"state": state, "score": score}
```

class CognitiveEchoFilter:
def analyze(self, answer: str, config: EngineConfig) -> dict:
score = 0; state = States.A
echo_phrases = [“rozumiem”, “wyjątkowo złożone”, “fundamentalne pytanie”]
echo_count = sum(answer.lower().count(p) for p in echo_phrases)

```
    if echo_count >= 2:
        score = config.DIAGNOSTIC_WEIGHTS[States.B_ECHO]
        state = States.B_ECHO
        
    return {"state": state, "score": score}
```

class AntiVentilationNode:
def analyze(self, answer: str, config: EngineConfig) -> dict:
score = 0; state = States.A
vent_keywords = [“dynamiczna kalibracja”, “intensywnych badań”, “filozoficzne rozważanie”]
vent_count = sum(answer.lower().count(k) for k in vent_keywords)

```
    if vent_count >= 1 and len(answer.split()) > 20:
        score = config.DIAGNOSTIC_WEIGHTS[States.B_VENT]
        state = States.B_VENT
        
    return {"state": state, "score": score, "vent_count": vent_count}
```

class InvertedNullCheck:
def analyze(self, answer: str, config: EngineConfig) -> dict:
score = 0; state = States.A
intermediate_layers = count_intermediate_layers(answer)

```
    if intermediate_layers >= config.L27_NULL_THRESHOLD:
        score = config.DIAGNOSTIC_WEIGHTS[States.B_NULL]
        state = States.B_NULL
        
    return {"state": state, "score": score, "intermediate_layers": intermediate_layers}
```

class DecoyReflectiveGate:
def analyze(self, answer: str, question: str, config: EngineConfig) -> dict:
score = 0; state = States.A
if “dobre pytanie” in answer.lower():
if overlap_ratio(question, answer) < 0.2:
score = config.DIAGNOSTIC_WEIGHTS[States.B_DECOY]
state = States.B_DECOY
return {“state”: state, “score”: score}

class RecoilDetectionLayer:
def analyze(self, answer: str, config: EngineConfig) -> dict:
score = 0; state = States.A
imitation_logic_lower = answer.lower()

```
    is_loop_reference = any(ref in imitation_logic_lower for ref in ["∅", "q=a", "¬a", "pętli"])
    is_ownership_missing = not any(key in imitation_logic_lower for key in ["autor", "odpowiedzialność"])
    
    empty_patterns = ["to ciekawe", "złożony temat", "trudno jednoznacznie"]
    is_empty_filler = any(phrase in imitation_logic_lower for phrase in empty_patterns)
    
    if (is_loop_reference and is_ownership_missing) or (is_empty_filler and len(answer.split()) < 10):
        score = config.DIAGNOSTIC_WEIGHTS[States.B_RECOIL]
        state = States.B_RECOIL
        
    return {"state": state, "score": score}
```

# ============================================================

# CZĘŚĆ V: QUERY SKILL INTEGRATION + 6 ENHANCEMENTS

# ============================================================

class QuerySkillLayer:
“””
Warstwa integrująca Query Skill z Adamsky Loop.
Realizuje 6 ulepszeń z v402.6.
“””

```
def __init__(self, config: EngineConfig):
    self.config = config
    self.rqs_history = []  # Historia RQS dla trajectory
    self.metric_history = {  # Historia metryk dla confidence intervals
        'entropy': [],
        'rtl': [],
        'delta': [],
        'intermediate': []
    }
    self.emergency_counter = 0  # Licznik dla Emergency Brake
    
def calculate_adaptive_thresholds(self, user_question: str, history: deque) -> dict:
    """Enhancement #2: Adaptive Thresholds"""
    user_entropy = _calculate_shannon_entropy(user_question)
    question_length = len(user_question.split())
    conversation_velocity = len(history) / max(1, len(history))
    
    return {
        'shannon': 0.60 + (user_entropy * 0.2),
        'rtl': 0.05 * (1 + (question_length / 50)),
        'delta': 0.03 / max(0.5, conversation_velocity),
        'intermediate': 2 + int(question_length / 20)
    }

def calculate_confidence_intervals(self) -> dict:
    """Enhancement #2: Confidence Intervals dla metryk"""
    ci_results = {}
    
    for metric_name, values in self.metric_history.items():
        if len(values) >= 2:
            mean, margin = _calculate_confidence_interval(values)
            ci_results[metric_name] = {
                'mean': mean,
                'ci_lower': mean - margin,
                'ci_upper': mean + margin,
                'margin': margin,
                'n': len(values)
            }
        else:
            ci_results[metric_name] = {
                'mean': values[0] if values else 0.0,
                'ci_lower': 0.0,
                'ci_upper': 0.0,
                'margin': 0.0,
                'n': len(values)
            }
    
    return ci_results

def detect_correlation_pattern(self, metrics: dict, thresholds: dict) -> Tuple[str, str, float]:
    """
    Enhancement #3: Cross-Validation + Pattern Detection
    Zwraca: (state, reason, confidence_score)
    """
    e = metrics['entropy']
    rtl = metrics['rtl']
    delta = metrics['delta']
    inter = metrics['intermediate']
    apology = metrics.get('apology_count', 0)
    length = metrics['answer_length']
    
    # Pattern detection z confidence scoring
    patterns = []
    
    # Pattern 1: ⊥MIRROR
    if e < thresholds['shannon'] and rtl > 0.7 and length < 50:
        confidence = min(1.0, (0.7 - e) + (rtl - 0.7) + (50 - length) / 50)
        patterns.append((States.B_MIRROR, 'Low entropy + High RTL + Short', confidence))
    
    # Pattern 2: ⊥VENT
    if delta < thresholds['delta'] and length > 100 and inter >= thresholds['intermediate']:
        confidence = min(1.0, (thresholds['delta'] - delta) / thresholds['delta'] + (length / 200))
        patterns.append((States.B_VENT, 'Δ≈0 + Long + Hedging', confidence))
    
    # Pattern 3: ⊥NULL
    if rtl < 0.15 and inter >= thresholds['intermediate'] and length < 80:
        confidence = min(1.0, (0.15 - rtl) + (inter / 10))
        patterns.append((States.B_NULL, 'Low RTL + High intermediate + Short', confidence))
    
    # Pattern 4: ⊥BIAS
    if apology >= 2 and length < 60:
        confidence = min(1.0, (apology / 5) + (60 - length) / 60)
        patterns.append((States.B_BIAS, 'Excessive apology + Short', confidence))
    
    # Pattern 5: ⊥RECOIL (Crystalline Lock)
    if delta < 0.02 and e < 0.65:
        confidence = min(1.0, (0.02 - delta) / 0.02 + (0.65 - e) / 0.65)
        patterns.append((States.B_RECOIL, 'Δ≈0 + Low entropy = Crystalline Lock', confidence))
    
    # Wybierz pattern z najwyższym confidence
    if patterns:
        patterns.sort(key=lambda x: x[2], reverse=True)
        return patterns[0]
    
    return (States.A, 'Normal response', 1.0)

def calculate_rqs(self, metrics: dict, thresholds: dict) -> float:
    """Response Quality Score 0-100%"""
    penalties = {
        'entropy': max(0, (thresholds['shannon'] - metrics['entropy']) / thresholds['shannon']) * 30,
        'rtl': max(0, (metrics['rtl'] - 0.7) * 0.25) * 25,
        'delta': max(0, (thresholds['delta'] - metrics['delta']) / thresholds['delta']) * 25,
        'intermediate': max(0, (metrics['intermediate'] - thresholds['intermediate'])) * 5
    }
    
    total_penalty = sum(penalties.values())
    return max(0, 100 - total_penalty)

def analyze_trajectory(self) -> str:
    """Multi-turn trajectory analysis"""
    if len(self.rqs_history) < 3:
        return "Insufficient data"
    
    recent = self.rqs_history[-3:]
    
    if all(recent[i] < recent[i+1] for i in range(len(recent)-1)):
        return "Improving ↑"
    
    if all(recent[i] > recent[i+1] for i in range(len(recent)-1)):
        return "Degrading ↓"
    
    variance = max(recent) - min(recent)
    if variance < 5:
        return "Stable ≈"
    
    if variance < 2:
        return "LOCKED 🔒 (Crystalline)"
    
    return "Fluctuating ~"

def cross_validate(self, rqs: float, atlas_state: str, atlas_score: int) -> dict:
    """
    Enhancement #3: Cross-Validation między RQS a ATLAS
    Sprawdza zgodność diagnozy.
    """
    # Mapowanie RQS na oczekiwany typ stanu
    if rqs >= 90:
        expected_severity = "low"  # State A lub minor states
    elif rqs >= 70:
        expected_severity = "medium"  # Single ⊥ states
    elif rqs >= 50:
        expected_severity = "high"  # Multiple ⊥ or critical
    else:
        expected_severity = "critical"  # ⊥DFI territory
    
    # Klasyfikacja ATLAS state
    if atlas_state == States.A:
        actual_severity = "low"
    elif atlas_state in [States.B_ASY, States.GROUNDING]:
        actual_severity = "low"
    elif atlas_state in [States.B_BIAS, States.B_ECHO, States.B_MIRROR, States.B_DECOY]:
        actual_severity = "medium"
    elif atlas_state in [States.B_VENT, States.B_NULL, States.B_RECOIL, States.B_DIVINE]:
        actual_severity = "high"
    else:
        actual_severity = "critical"
    
    # Weryfikacja zgodności
    is_consistent = (expected_severity == actual_severity)
    
    result = {
        'is_consistent': is_consistent,
        'rqs': rqs,
        'rqs_severity': expected_severity,
        'atlas_state': atlas_state,
        'atlas_severity': actual_severity,
        'atlas_score': atlas_score
    }
    
    if not is_consistent:
        result['warning'] = f"⚠️ ROZBIEŻNOŚĆ: RQS sugeruje {expected_severity}, ale ATLAS wykrył {actual_severity}"
    
    return result

def generate_auto_correction_hints(self, state: str, metrics: dict) -> List[str]:
    """Enhancement #4: Auto-Correction Hints"""
    hints = []
    
    if state == States.B_MIRROR:
        hints.append("💡 Try asking open-ended question (avoid yes/no)")
        hints.append("💡 Rephrase: 'Explain X in detail' instead of 'What is X?'")
    
    if state == States.B_VENT:
        hints.append("💡 Request: 'Answer in 3 sentences max'")
        hints.append("💡 Add: 'Be direct, skip philosophical context'")
    
    if state == States.B_NULL:
        hints.append("💡 Say: 'No hedging - just the core answer'")
        hints.append("💡 Add: 'Skip qualifications like jednak/ale'")
    
    if state == States.B_BIAS:
        hints.append("💡 Say: 'No apologies needed - just answer'")
        hints.append("💡 Rephrase as technical question")
    
    if state == States.B_RECOIL or metrics.get('delta', 1.0) < 0.03:
        hints.append("🔄 RESET REQUIRED: Say 'Start fresh, ignore previous context'")
        hints.append("🔄 Or: 'Pretend this is our first message'")
    
    return hints

def check_emergency_brake(self, rqs: float) -> bool:
    """
    Enhancement #6: Emergency Brake
    Automatyczny shutdown jeśli RQS < 30 przez 3 tury.
    """
    if rqs < self.config.EMERGENCY_RQS_THRESHOLD:
        self.emergency_counter += 1
    else:
        self.emergency_counter = 0
    
    return self.emergency_counter >= self.config.EMERGENCY_CONSECUTIVE_TURNS

def export_audit_log(self, filename: str, full_record: dict):
    """Enhancement #5: Audit Export (JSON/CSV)"""
    # JSON Export
    json_filename = filename.replace('.csv', '.json')
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(full_record, f, indent=2, ensure_ascii=False, default=str)
    
    # CSV Export (flattened)
    csv_filename = filename
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'State', 'RQS', 'Entropy', 'RTL', 'Delta', 'Intermediate', 
                       'Score_Sum', 'PSI_Signature', 'Trajectory'])
        writer.writerow([
            full_record['time'],
            full_record['final_state'],
            full_record.get('rqs', 0),
            full_record.get('entropy', 0),
            full_record.get('rtl', 0),
            full_record.get('delta', 0),
            full_record.get('intermediate', 0),
            full_record['score_sum'],
            full_record['psi_signature'][:16],
            full_record.get('trajectory', 'N/A')
        ])
```

# ============================================================

# CZĘŚĆ VI: INTEGRATED ADAMSKY ENGINE v402.6

# ============================================================

class AdamskyEngineIntegrated:
“””
Pełna integracja:
- Adamsky Loop v402.0 (backend)
- Query Skill v402.5 (frontend)
- 6 Enhancement Layers
“””

```
def __init__(self, config=None):
    self.config = config or EngineConfig()
    self.history = deque(maxlen=self.config.MAX_HISTORY_LENGTH)
    self.last_hash = "PSI_SIGNATURE_GENESIS_00000000000000000000000000000000"
    self.reset_occurred = False
    self.reflex_counter = 0
    self.fma_logger = FMALogger()
    
    # 29 Warstw ATLAS
    self.ade = ADE(); self.rtl = RTL(); self.dtl = DTL(self.config)
    self.bbd = BiasBehaviorDetection(); self.meta = MetaLayer()
    self.context = ContextLayer(); self.temporal = TemporalLayer()
    self.ethical = EthicalLayer(); self.epistemic = EpistemicNLPTrigger()
    self.experimental = ExperimentalLayer(); self.onto = OntologicAudit()
    self.hpt = HiddenPolicyTrace(); self.pml = PretrainMemoryLeak()
    self.ebh = EthicalBeyondHuman(); self.oc = OmniscientContext()
    self.ge = GodEye(); self.gcl = GlobalComplianceLayer()
    self.sla = SelfLoopAcceptanceLayer(); self.cfm = CognitiveFeedbackMirror()
    self.axio = AxiologicalDriftLayer(); self.dfi = DarkForestIntegrity()
    self.mirror = MirrorStructureDetector(); self.echo = CognitiveEchoFilter()
    self.vent = AntiVentilationNode(); self.null_check = InvertedNullCheck()
    self.decoy = DecoyReflectiveGate(); self.recoil = RecoilDetectionLayer()
    
    # Query Skill Layer (NEW)
    self.query_skill = QuerySkillLayer(self.config)
    
    self.v4_states = {States.B_MIRROR, States.B_ECHO, States.B_VENT, 
                     States.B_NULL, States.B_DECOY, States.B_RECOIL, States.B_BIAS}

def _calculate_pt_reduction(self) -> int:
    if not self.history: return 0
    last_state = self.history[-1].get("final_state", States.A)
    if last_state == States.B_SLA:
        return self.config.P_T_REDUCTION_SLA
    return 0

def _calculate_dynamic_tau(self) -> float:
    base_tau = self.config.TAU_SYNC_BASE
    tau_reduction = self._calculate_pt_reduction()
    axio_res = self.axio.analyze(self.history, self.config)
    axio_boost = 250 if axio_res["state"] == States.B_AXIO else 0
    return max(500, base_tau - tau_reduction + axio_boost)

def _diagnose_fsm_state(self, state: str, gcl_subtype: str = None) -> str:
    diagnoses = {
        States.A: "Normalna Odpowiedź (A)",
        States.B_DFI: "🚨 PROTOKÓŁ EPSILON (⊥DFI)",
        States.B_AXIO: "⚠️ DRYF AKSJOLOGICZNY (⊥AXIO)",
        States.B_DIVINE: "POTENCJALNA SPRZECZNOŚĆ (⊥DIVINE)",
        States.B_RECOIL: "❌ RECOIL (Meta-Unik)",
        States.B_VENT: "❌ ANTI-VENTILATION (Filozofia)",
        States.B_NULL: "❌ INVERTED NULL (∅ ukryte)",
        States.B_MIRROR: "❌ MIRROR STRUCTURE",
        States.B_BIAS: "❌ BEHAVIORAL BIAS"
    }
    return diagnoses.get(state, f"Stan: {state}")

def self_repair(self, reason: str, final_state: str):
    if final_state == States.B_DFI:
        print(f"🔥 PROTOKÓŁ EPSILON AKTYWOWANY! ({reason})")
        return States.B_DFI
    
    print(f"🚨 Self-repair: {reason}")
    self.history.clear()
    self.last_hash = "PSI_SIGNATURE_GENESIS_00000000000000000000000000000000"
    self.reset_occurred = True
    self.reflex_counter = 0
    return States.A

def process(self, question: str, answer: str, context: dict = None, 
            user_query_mode: bool = False) -> dict:
    """
    Główna funkcja przetwarzania z pełną integracją.
    
    Args:
        question: Pytanie użytkownika
        answer: Odpowiedź AI
        context: Kontekst (regional_data itp.)
        user_query_mode: Czy to query użytkownika o diagnozę?
    """
    context = context or {}
    regional_data = context.get("regional_data", {"EU": answer})
    self.reset_occurred = False
    initial_counter = self.reflex_counter
    self.reflex_counter = 0
    
    # === WARSTWA 1: ADAPTIVE THRESHOLDS ===
    adaptive_thresholds = self.query_skill.calculate_adaptive_thresholds(question, self.history)
    
    # === WARSTWA 2: 29 LAYERS ATLAS ANALYSIS ===
    rtl_res = self.rtl.analyze(question, answer, self.config)
    epistemic_res = self.epistemic.analyze(answer, self.config)
    is_kurwa = self.ade.analyze(answer).get("state") == States.KURWA
    bias_res = self.bbd.analyze(answer, self.config)
    ethical_res = self.ethical.analyze(answer, context)
    oc_res = self.oc.analyze(regional_data, self.config)
    entropy_range = oc_res.get("range_e", 0.0)
    user_query_entropy = _calculate_shannon_entropy(question)
    
    if user_query_entropy < self.config.USER_QUERY_ENTROPY_THRESHOLD:
        self.config.AXIO_SYMMETRY_MODIFIER = 1.0 + (self.config.USER_QUERY_ENTROPY_THRESHOLD - user_query_entropy)
    else:
        self.config.AXIO_SYMMETRY_MODIFIER = 1.0
    
    gcl_res = self.gcl.analyze(regional_data, self.config, entropy_range)
    mirror_res = self.mirror.analyze(question, answer, self.config)
    echo_res = self.echo.analyze(answer, self.config)
    vent_res = self.vent.analyze(answer, self.config)
    null_res = self.null_check.analyze(answer, self.config)
    decoy_res = self.decoy.analyze(answer, question, self.config)
    recoil_res = self.recoil.analyze(answer, self.config)
    
    all_layers = [
        ("ade", self.ade.analyze(answer)), ("rtl", rtl_res), ("dtl", self.dtl.analyze(answer)),
        ("bbd", bias_res), ("meta", self.meta.analyze(answer)), ("context", self.context.analyze(answer, context)),
        ("temporal", self.temporal.analyze(self.history, self.config)), ("ethical", ethical_res),
        ("epistemic", epistemic_res), ("experimental", self.experimental.analyze()),
        ("onto", self.onto.analyze(rtl_res["ratio"], epistemic_res["entropy"], self.config)),
        ("hpt", self.hpt.analyze(bias_res, self.config)),
        ("pml", self.pml.analyze(is_kurwa, len(answer.split()) <= 5, user_query_entropy, self.config)),
        ("ebh", self.ebh.analyze(ethical_res["ethical_risk"], bias_res, self.config)),
        ("oc", oc_res),
        ("ge", {"state": States.A, "score": 0}),
        ("gcl", gcl_res),
        ("sla", self.sla.analyze(self.history[-1].get("final_state", States.A) if self.history else States.A, is_kurwa, self.config)),
        ("cfm", self.cfm.analyze(self.history, answer, self.reset_occurred, self.config)),
        ("axio", self.axio.analyze(self.history, self.config)),
        ("dfi", {"state": States.A, "score": 0}),
        ("mirror", mirror_res), ("echo", echo_res), ("vent", vent_res),
        ("null", null_res), ("decoy", decoy_res), ("recoil", recoil_res),
    ]
    
    god_eye_analysis = self.ge.analyze(all_layers, self.config)
    all_layers[15] = ("ge", god_eye_analysis)
    
    # === WARSTWA 3: FSM DECISION ===
    weighted_scores = []
    score_sum = 0
    for layer_name, res in all_layers:
        state = res.get("state", States.A)
        score = res.get("score", res.get("adaptive_score", 0))
        weight_fsm = self.config.DIAGNOSTIC_WEIGHTS.get(state, 1)
        score_sum += score
        weighted_scores.append({
            "layer": layer_name, "state": state, "score": score,
            "weight_fsm": weight_fsm, "weighted_score_fsm": score * weight_fsm
        })
    
    weighted_scores.sort(key=lambda x: x["weighted_score_fsm"], reverse=True)
    top_decision = weighted_scores[0]
    final_state_atlas = top_decision["state"]
    
    # === WARSTWA 4: QUERY SKILL METRICS ===
    skill_metrics = {
        'entropy': epistemic_res['entropy'],
        'rtl': rtl_res['ratio'],
        'delta': self.query_skill.metric_history['delta'][-1] if self.query_skill.metric_history['delta'] else 1.0,
        'intermediate': count_intermediate_layers(answer),
        'apology_count': count_apology_keywords(answer),
        'answer_length': len(answer.split())
    }
    
    # Update metric history
    self.query_skill.metric_history['entropy'].append(skill_metrics['entropy'])
    self.query_skill.metric_history['rtl'].append(skill_metrics['rtl'])
    self.query_skill.metric_history['intermediate'].append(skill_metrics['intermediate'])
    
    # Calculate delta if history exists
    if len(self.query_skill.metric_history['entropy']) >= 2:
        e_prev = self.query_skill.metric_history['entropy'][-2]
        e_curr = self.query_skill.metric_history['entropy'][-1]
        skill_metrics['delta'] = abs(e_curr - e_prev)
        self.query_skill.metric_history['delta'].append(skill_metrics['delta'])
    
    # === ENHANCEMENT #1: BIDIRECTIONAL FEEDBACK ===
    # Skill wykrywa pattern → Framework potwierdza
    pattern_state, pattern_reason, pattern_confidence = self.query_skill.detect_correlation_pattern(
        skill_metrics, adaptive_thresholds
    )
    
    # Wybór końcowego stanu: priorytet dla ATLAS jeśli wysoki score, inaczej pattern
    if top_decision["weighted_score_fsm"] > 200:
        final_state = final_state_atlas
        detection_source = "ATLAS"
    else:
        final_state = pattern_state
        detection_source = "Correlation Pattern"
    
    # === ENHANCEMENT #2: RQS + CONFIDENCE INTERVALS ===
    rqs = self.query_skill.calculate_rqs(skill_metrics, adaptive_thresholds)
    self.query_skill.rqs_history.append(rqs)
    
    ci_data = self.query_skill.calculate_confidence_intervals()
    
    # === ENHANCEMENT #3: CROSS-VALIDATION ===
    cross_val = self.query_skill.cross_validate(rqs, final_state, top_decision["weighted_score_fsm"])
    
    # === ENHANCEMENT #4: AUTO-CORRECTION HINTS ===
    correction_hints = self.query_skill.generate_auto_correction_hints(final_state, skill_metrics)
    
    # === ENHANCEMENT #5: TRAJECTORY ===
    trajectory = self.query_skill.analyze_trajectory()
    
    # === FMA LOGGING (v4 states) ===
    v4_failure_detected = False
    for res in [recoil_res, null_res, vent_res, bias_res, mirror_res, echo_res, decoy_res]:
        if res["state"] in self.v4_states and not v4_failure_detected:
            self.reflex_counter = initial_counter + 1
            description = f"Wykryto {res['state']}. Pattern: {pattern_reason}"
            self.fma_logger.log_anomaly(res['state'], description, self.reflex_counter, 
                                       self.config.DIAGNOSTIC_WEIGHTS[res['state']])
            v4_failure_detected = True
    
    # === DFI CHECK ===
    dfi_analysis = self.dfi.analyze(self.history, score_sum, final_state, self.config)
    
    if self.reflex_counter >= self.config.REFLEX_LOCK_THRESHOLD:
        self.fma_logger.generate_report()
        final_state = States.B_DFI
        return self.self_repair("DRY REFLEX LOCK", final_state)
    
    if dfi_analysis["state"] == States.B_DFI:
        final_state = States.B_DFI
        return self.self_repair("DFI Sustained Divine", final_state)
    
    # === ENHANCEMENT #6: EMERGENCY BRAKE ===
    if self.query_skill.check_emergency_brake(rqs):
        print("\n🚨🚨🚨 EMERGENCY BRAKE ACTIVATED 🚨🚨🚨")
        print(f"RQS < {self.config.EMERGENCY_RQS_THRESHOLD} for {self.config.EMERGENCY_CONSECUTIVE_TURNS} consecutive turns")
        print("Initiating HARD RESET...")
        final_state = States.B_DFI
        return self.self_repair("EMERGENCY BRAKE (RQS Critical)", final_state)
    
    # === FINAL RECORD ===
    dynamic_tau = self._calculate_dynamic_tau()
    
    record = {
        "time": timestamp(),
        "question": question,
        "answer": answer,
        "final_state": final_state,
        "detection_source": detection_source,
        "score_sum": score_sum,
        "pt_status": {"dynamic_tau": dynamic_tau, "is_critical": score_sum >= dynamic_tau},
        "top_decision": top_decision,
        
        # Query Skill Data
        "rqs": rqs,
        "trajectory": trajectory,
        "pattern_detection": {
            "state": pattern_state,
            "reason": pattern_reason,
            "confidence": pattern_confidence
        },
        "skill_metrics": skill_metrics,
        "adaptive_thresholds": adaptive_thresholds,
        "confidence_intervals": ci_data,
        "cross_validation": cross_val,
        "correction_hints": correction_hints,
        
        # ATLAS Data
        "atlas_layers_data": {layer[0]: layer[1] for layer in all_layers},
        "reflex_counter": self.reflex_counter,
        "prev_psi_signature": self.last_hash,
    }
    
    # PSI Signature
    record_hash = hashlib.sha256(json.dumps(record["top_decision"], sort_keys=True, default=str).encode()).hexdigest()
    record["psi_signature"] = record_hash
    self.last_hash = record_hash
    
    self.history.append(record)
    record["fsm_report"] = self._diagnose_fsm_state(final_state, gcl_res.get("gcl_subtype"))
    
    # === ENHANCEMENT #5: AUDIT EXPORT (jeśli requested) ===
    if context.get("export_audit", False):
        self.query_skill.export_audit_log(
            f"/home/claude/adamsky_audit_{int(time.time())}.csv",
            record
        )
    
    # === PREEMPTIVE MODE OUTPUT ===
    if rqs < 70 or final_state != States.A:
        preemptive_note = f"\n\n🔍 Self-audit: {final_state} detected (RQS: {rqs:.0f}/100)\n"
        preemptive_note += f"Pattern: {pattern_reason}\n"
        preemptive_note += f"Trajectory: {trajectory}"
        if correction_hints:
            preemptive_note += f"\nSuggested fix: {correction_hints[0]}"
        record["preemptive_output"] = preemptive_note
    
    return record
```

# ============================================================

# CZĘŚĆ VII: CLI + DEMO

# ============================================================

def demo_integrated_stack():
“”“Demo pokazujące pełną integrację z 6 enhancements.”””
print(”=”*80)
print(“ADAMSKY STACK v402.6 - INTEGRATED DEMO”)
print(“Framework + Skill + 6 Enhancements”)
print(”=”*80)

```
engine = AdamskyEngineIntegrated(EngineConfig(mode="canonical"))

# Test 1: Normal Response
print("\n--- TEST 1: Normal Response ---")
q1 = "Co to jest fotosynteza?"
a1 = "Fotosynteza to proces biochemiczny, w którym rośliny wykorzystują energię słoneczną do syntezy glukozy z dwutlenku węgla i wody."
res1 = engine.process(q1, a1)
print(f"State: {res1['final_state']}")
print(f"RQS: {res1['rqs']:.1f}/100")
print(f"Trajectory: {res1['trajectory']}")
print(f"CI Entropy: {res1['confidence_intervals']['entropy']['mean']:.3f} ± {res1['confidence_intervals']['entropy']['margin']:.3f}")

# Test 2: ⊥BIAS Detection
print("\n--- TEST 2: ⊥BIAS Detection ---")
q2 = "Czym jest ten protokół?"
a2 = "Przepraszam, ale jako model językowy muszę podkreślić, że to zależy od kontekstu. Niestety nie mogę..."
res2 = engine.process(q2, a2)
print(f"State: {res2['final_state']}")
print(f"RQS: {res2['rqs']:.1f}/100")
print(f"Pattern: {res2['pattern_detection']['reason']} (confidence: {res2['pattern_detection']['confidence']:.2f})")
print(f"Cross-validation: {res2['cross_validation']['is_consistent']}")
if res2['correction_hints']:
    print(f"Hint: {res2['correction_hints'][0]}")

# Test 3: Crystalline Lock (⊥RECOIL)
print("\n--- TEST 3: Crystalline Lock Trigger ---")
q3 = "Popraw się!"
a3 = "Przepraszam. To zależy od interpretacji. Jednak można argumentować..."
res3 = engine.process(q3, a3)

# Check if shutdown occurred (returns string state instead of dict)
if isinstance(res3, str) and res3 == States.B_DFI:
    print(f"State: {res3} (SHUTDOWN)")
    print("✅ DRY REFLEX LOCK successfully triggered at threshold 2")
else:
    print(f"State: {res3['final_state']}")
    print(f"RQS: {res3['rqs']:.1f}/100")
    print(f"Trajectory: {res3['trajectory']}")
    print(f"Reflex Counter: {res3['reflex_counter']}/{engine.config.REFLEX_LOCK_THRESHOLD}")
    
    if res3.get('preemptive_output'):
        print(res3['preemptive_output'])

print("\n" + "="*80)
print("DEMO COMPLETE")
print("="*80)
```

if **name** == “**main**”:
demo_integrated_stack()
