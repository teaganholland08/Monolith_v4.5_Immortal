"""
MEMORY ENGINE - Best-in-World 2026 Standard
Implements: Episodic Memory, Semantic Memory, Selective Forgetting
Purpose: Enable agents to learn, remember, and improve over time.
"""

import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import math

# --- Configuration ---
MEMORY_DIR = Path(__file__).parent.parent.parent / "Brain" / "Memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class MemoryEntry:
    """A single memory unit"""
    id: str
    content: str
    memory_type: str  # "episodic" or "semantic"
    timestamp: str
    importance: float = 1.0
    access_count: int = 0
    last_accessed: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None  # For future vector search


class EpisodicMemory:
    """
    Stores specific events and experiences (what happened when).
    Features time-based decay and recency weighting.
    """
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.memory_file = MEMORY_DIR / f"{agent_name}_episodic.json"
        self.entries: List[MemoryEntry] = []
        self._load()
    
    def _load(self):
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = [
                        MemoryEntry(**entry) for entry in data
                    ]
            except:
                self.entries = []
    
    def _save(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(e) for e in self.entries], f, indent=2)
    
    def _generate_id(self, content: str) -> str:
        return hashlib.md5(f"{content}{time.time()}".encode()).hexdigest()[:12]
    
    def store(self, content: str, importance: float = 1.0, metadata: Dict = None) -> str:
        """Store a new episodic memory"""
        entry = MemoryEntry(
            id=self._generate_id(content),
            content=content,
            memory_type="episodic",
            timestamp=datetime.now().isoformat(),
            importance=importance,
            metadata=metadata or {}
        )
        self.entries.append(entry)
        self._save()
        return entry.id
    
    def recall(self, query: str, limit: int = 5) -> List[MemoryEntry]:
        """Recall relevant memories (simple keyword matching for now)"""
        scored = []
        query_words = set(query.lower().split())
        
        for entry in self.entries:
            # Calculate relevance score
            content_words = set(entry.content.lower().split())
            overlap = len(query_words & content_words)
            
            # Factor in recency
            age_hours = (datetime.now() - datetime.fromisoformat(entry.timestamp)).total_seconds() / 3600
            recency_score = 1.0 / (1.0 + math.log1p(age_hours))
            
            # Combined score
            score = (overlap * entry.importance * recency_score)
            
            if score > 0:
                scored.append((score, entry))
                entry.access_count += 1
                entry.last_accessed = datetime.now().isoformat()
        
        # Sort by score and return top matches
        scored.sort(key=lambda x: x[0], reverse=True)
        self._save()
        return [entry for score, entry in scored[:limit]]
    
    def forget_old(self, max_age_days: int = 30, min_importance: float = 0.5):
        """Selective forgetting: remove old, unimportant memories"""
        cutoff = datetime.now() - timedelta(days=max_age_days)
        original_count = len(self.entries)
        
        self.entries = [
            e for e in self.entries
            if (datetime.fromisoformat(e.timestamp) > cutoff or 
                e.importance >= min_importance or
                e.access_count > 3)
        ]
        
        forgotten = original_count - len(self.entries)
        if forgotten > 0:
            self._save()
        return forgotten


class SemanticMemory:
    """
    Stores facts, concepts, and learned knowledge.
    More permanent than episodic, organized by topic.
    """
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.memory_file = MEMORY_DIR / f"{agent_name}_semantic.json"
        self.knowledge: Dict[str, List[Dict]] = {}
        self._load()
    
    def _load(self):
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.knowledge = json.load(f)
            except:
                self.knowledge = {}
    
    def _save(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def learn(self, topic: str, fact: str, confidence: float = 1.0, source: str = None):
        """Learn a new fact about a topic"""
        if topic not in self.knowledge:
            self.knowledge[topic] = []
        
        # Check for duplicates
        for existing in self.knowledge[topic]:
            if existing["fact"] == fact:
                # Update confidence if higher
                if confidence > existing.get("confidence", 0):
                    existing["confidence"] = confidence
                    existing["updated"] = datetime.now().isoformat()
                    self._save()
                return
        
        self.knowledge[topic].append({
            "fact": fact,
            "confidence": confidence,
            "source": source,
            "learned": datetime.now().isoformat()
        })
        self._save()
    
    def query(self, topic: str, min_confidence: float = 0.5) -> List[Dict]:
        """Query knowledge about a topic"""
        if topic not in self.knowledge:
            return []
        
        return [
            fact for fact in self.knowledge[topic]
            if fact.get("confidence", 1.0) >= min_confidence
        ]
    
    def get_all_topics(self) -> List[str]:
        """List all known topics"""
        return list(self.knowledge.keys())
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        total_facts = sum(len(facts) for facts in self.knowledge.values())
        return {
            "topics": len(self.knowledge),
            "total_facts": total_facts,
            "avg_facts_per_topic": total_facts / max(1, len(self.knowledge))
        }


class MemoryEngine:
    """
    Unified Memory Engine combining Episodic and Semantic memory.
    Each agent gets its own memory namespace.
    """
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.episodic = EpisodicMemory(agent_name)
        self.semantic = SemanticMemory(agent_name)
    
    def remember_event(self, description: str, importance: float = 1.0, **metadata) -> str:
        """Store an episodic memory (what happened)"""
        return self.episodic.store(description, importance, metadata)
    
    def learn_fact(self, topic: str, fact: str, confidence: float = 1.0, source: str = None):
        """Store a semantic memory (learned knowledge)"""
        self.semantic.learn(topic, fact, confidence, source)
    
    def recall_events(self, query: str, limit: int = 5) -> List[MemoryEntry]:
        """Recall relevant past events"""
        return self.episodic.recall(query, limit)
    
    def query_knowledge(self, topic: str) -> List[Dict]:
        """Query learned knowledge"""
        return self.semantic.query(topic)
    
    def consolidate(self):
        """
        Memory consolidation: promote frequently-accessed episodic memories
        to semantic knowledge (like sleep consolidation in humans).
        """
        high_access = [e for e in self.episodic.entries if e.access_count >= 5]
        
        for entry in high_access:
            # Extract topic from metadata or use "general"
            topic = entry.metadata.get("topic", "general_knowledge")
            self.semantic.learn(
                topic,
                entry.content,
                confidence=min(1.0, entry.access_count / 10),
                source="consolidated_from_episodic"
            )
    
    def maintenance(self, forget_days: int = 30):
        """Run memory maintenance (forgetting, consolidation)"""
        self.consolidate()
        forgotten = self.episodic.forget_old(max_age_days=forget_days)
        return {"forgotten_episodes": forgotten}
    
    def get_full_stats(self) -> Dict:
        """Get complete memory statistics"""
        return {
            "agent": self.agent_name,
            "episodic_count": len(self.episodic.entries),
            "semantic": self.semantic.get_stats(),
            "timestamp": datetime.now().isoformat()
        }


# Factory function
_engines: Dict[str, MemoryEngine] = {}

def get_memory(agent_name: str) -> MemoryEngine:
    """Get or create a memory engine for an agent"""
    if agent_name not in _engines:
        _engines[agent_name] = MemoryEngine(agent_name)
    return _engines[agent_name]


if __name__ == "__main__":
    # Demo
    mem = get_memory("demo_agent")
    
    # Episodic memories
    mem.remember_event("User asked about tax optimization", importance=0.8, topic="taxes")
    mem.remember_event("Successfully executed investment analysis", importance=0.9, topic="finance")
    mem.remember_event("System startup completed", importance=0.3)
    
    # Semantic learning
    mem.learn_fact("tax_rules", "RRSP contribution limit is 18% of earned income", confidence=0.95)
    mem.learn_fact("tax_rules", "TFSA limit for 2026 is $7,000", confidence=0.95)
    mem.learn_fact("crypto", "Bitcoin halving occurred in April 2024", confidence=1.0)
    
    # Recall
    print("Recalling 'tax' events:")
    for entry in mem.recall_events("tax"):
        print(f"  - {entry.content}")
    
    print("\nKnowledge about tax_rules:")
    for fact in mem.query_knowledge("tax_rules"):
        print(f"  - {fact['fact']} (confidence: {fact['confidence']})")
    
    print(f"\nStats: {mem.get_full_stats()}")
