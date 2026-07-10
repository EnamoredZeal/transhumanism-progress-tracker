import datetime
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MetricEntry:
    """Represents a single verifiable data point for a metric."""
    value: float                     # The raw quantitative value
    unit: str                        # e.g., "bps", "channels", "Phi", "words/min"
    source_citation: str             # Peer-reviewed study, clinical trial ID, or DOI
    trl_level: int                   # Technology Readiness Level (1 to 9)
    is_human_tested: bool            # Explicit flag to prevent human/animal conflation
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )
    notes: Optional[str] = None
    safety_status: str = field(init=False)  # Automatically generated based on profile

    def __post_init__(self):
        if not (1 <= self.trl_level <= 9):
            raise ValueError("TRL level must be an integer between 1 and 9.")
        
        # Enforce automated safety tagging based on the metric profile
        if not self.is_human_tested:
            self.safety_status = "PRE-CLINICAL / ANIMAL MODEL ONLY: Zero immediate human applicability."
        elif self.trl_level < 6:
            self.safety_status = "EARLY LABORATORY STAGE: Unverified safety and high risk outside controlled research environments."
        elif self.trl_level in [6, 7]:
            self.safety_status = "ACTIVE CLINICAL TRIAL: Investigational status under strict medical oversight."
        else:
            self.safety_status = "APPROVED STATUS: Regulated deployment standard."


@dataclass
class TranshumanistTracker:
    """Core tracking system organizing the convergence pillars."""
    project_name: str = "Transhumanism Progress Tracker"
    last_updated: str = field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )
    
    # Pillar Storage
    cybernetic_integration: Dict[str, List[MetricEntry]] = field(default_factory=lambda: {
        "bandwidth_bps": [],
        "channel_count": [],
        "signal_stability_days": [],
    })
    genetic_cellular_modification: Dict[str, List[MetricEntry]] = field(default_factory=lambda: {
        "editing_fidelity_pct": [],
        "epigenetic_reversal_years": [],
        "senolytic_clearance_pct": [],
    })
    somatic_augmentation: Dict[str, List[MetricEntry]] = field(default_factory=lambda: {
        "degrees_of_freedom": [],
        "latency_ms": [],
        "sensory_feedback_fidelity": [],
    })
    cognitive_consciousness_sciences: Dict[str, List[MetricEntry]] = field(default_factory=lambda: {
        "working_memory_index": [],
        "phi_complexity_value": [],
        "connectome_mapped_pct": [],
    })

    def log_metric(self, pillar: str, metric_name: str, entry: MetricEntry):
        """Routes and appends a verified metric entry to the appropriate pillar."""
        pillar_map = {
            "cybernetic": self.cybernetic_integration,
            "genetic": self.genetic_cellular_modification,
            "somatic": self.somatic_augmentation,
            "cognitive": self.cognitive_consciousness_sciences
        }
        
        target_pillar = pillar_map.get(pillar.lower())
        if not target_pillar:
            raise ValueError(f"Unknown pillar. Choose from: {list(pillar_map.keys())}")
            
        if metric_name not in target_pillar:
            target_pillar[metric_name] = []
            
        target_pillar[metric_name].append(entry)
        self.last_updated = datetime.datetime.utcnow().isoformat()

    def export_to_json(self, filepath: str):
        """Serializes the entire state of the tracker to a structured JSON file."""
        with open(filepath, "w") as f:
            json.dump(asdict(self), f, indent=4)
        print(f"[Success] Tracker state exported cleanly to {filepath}")


# ==========================================
# Execution / Example Logging Usage
# ==========================================
if __name__ == "__main__":
    # Initialize your master tracker
    tracker = TranshumanistTracker()

    # Example 1: Logging a Cybernetic BCI Milestone
    tracker.log_metric(
        pillar="cybernetic",
        metric_name="bandwidth_bps",
        entry=MetricEntry(
            value=4.2,
            unit="bits/sec",
            source_citation="Nature Medicine (2025) DOI:10.1038/s41591-xxx",
            trl_level=6,  
            is_human_tested=True,
            notes="Intracortical microelectrode array tracking speech intent."
        )
    )

    # Example 2: Logging a Cognitive Science / Consciousness Milestone (Phi / PCI)
    tracker.log_metric(
        pillar="cognitive",
        metric_name="phi_complexity_value",
        entry=MetricEntry(
            value=0.68,
            unit="PCI_index_score",
            source_citation="Journal of Cognitive Neuroscience (2026) PMCxxxx",
            trl_level=4,  
            is_human_tested=False,
            notes="Perturbational Complexity Index threshold mapping wakeful integration vs anesthesia."
        )
    )

    # Export data to disk
    tracker.export_to_json("core/database.json")
