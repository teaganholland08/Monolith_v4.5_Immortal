"""
LEARNING AGENT - Continuous Skill Development & Knowledge Acquisition
Purpose: Self-improvement through online courses, research, and skill building.
"""

import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List


class LearningAgent:
    """
    The Continuous Improvement Engine.
    - Tracks learning goals and progress
    - Monitors skill development
    - Suggests courses and resources
    - Measures knowledge growth
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.data_dir = Path(__file__).parent.parent.parent / "Brain" / "Knowledge"
        
        self.sentinel_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.progress_file = self.data_dir / "learning_progress.json"
        self.load_progress()
    
    def load_progress(self):
        """Load learning progress"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        else:
            # Initialize with example learning paths
            self.progress = {
                "active_courses": [
                    {
                        "name": "Advanced Python for AI Agents",
                        "platform": "Coursera",
                        "progress": 45,
                        "target_completion": "2026-03-01"
                    },
                    {
                        "name": "Post-Quantum Cryptography",
                        "platform": "edX",
                        "progress": 20,
                        "target_completion": "2026-04-15"
                    }
                ],
                "completed_courses": [],
                "reading_list": [
                    {"title": "Designing Data-Intensive Applications", "pages_read": 150, "total_pages": 600},
                    {"title": "The Pragmatic Programmer", "pages_read": 320, "total_pages": 352}
                ],
                "skills": {
                    "Python": {"level": 8, "target": 10},
                    "AI/ML": {"level": 7, "target": 10},
                    "Cryptography": {"level": 5, "target": 9},
                    "System Design": {"level": 7, "target": 10}
                },
                "learning_hours_this_month": 12
            }
            self.save_progress()
    
    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def suggest_resources(self) -> List[Dict]:
        """Suggest learning resources based on skill gaps"""
        suggestions = []
        
        # Identify skill gaps
        for skill, data in self.progress["skills"].items():
            gap = data["target"] - data["level"]
            if gap >= 2:
                suggestions.append({
                    "skill": skill,
                    "gap": gap,
                    "recommended_courses": self._get_course_recommendations(skill),
                    "priority": "HIGH" if gap >= 3 else "MEDIUM"
                })
        
        return suggestions
    
    def _get_course_recommendations(self, skill: str) -> List[str]:
        """Get course recommendations for a skill"""
        course_db = {
            "Python": [
                "Advanced Python Patterns - Udemy",
                "Python for Data Science - Coursera",
                "Async Programming Masterclass - Real Python"
            ],
            "AI/ML": [
                "Deep Learning Specialization - Coursera",
                "MLOps Engineering - AWS Training",
                "Advanced LLM Applications - Fast.ai"
            ],
            "Cryptography": [
                "Post-Quantum Cryptography - edX",
                "Applied Cryptography - Stanford Online",
                "Zero-Knowledge Proofs - MIT OCW"
            ],
            "System Design": [
                "Designing Distributed Systems - Pluralsight",
                "Microservices Architecture - Udemy",
                "Cloud Architecture Patterns - AWS"
            ]
        }
        
        return course_db.get(skill, [])
    
    def update_course_progress(self, course_name: str, new_progress: int):
        """Update progress on an active course"""
        for course in self.progress["active_courses"]:
            if course["name"] == course_name:
                course["progress"] = new_progress
                
                # Mark as complete if 100%
                if new_progress >= 100:
                    self.progress["completed_courses"].append({
                        **course,
                        "completed_date": datetime.now().isoformat()
                    })
                    self.progress["active_courses"].remove(course)
                break
        
        self.save_progress()
    
    def log_learning_session(self, hours: float, topic: str):
        """Log a learning session"""
        self.progress["learning_hours_this_month"] += hours
        
        # Increment skill level based on learning time
        if topic in self.progress["skills"]:
            # Every 10 hours = +0.5 skill level
            level_gain = hours / 20.0
            current = self.progress["skills"][topic]["level"]
            target = self.progress["skills"][topic]["target"]
            
            new_level = min(target, current + level_gain)
            self.progress["skills"][topic]["level"] = round(new_level, 1)
        
        self.save_progress()
    
    def get_learning_report(self) -> Dict:
        """Generate learning progress report"""
        total_courses = len(self.progress["active_courses"]) + len(self.progress["completed_courses"])
        avg_progress = sum(c["progress"] for c in self.progress["active_courses"]) / max(1, len(self.progress["active_courses"]))
        
        # Calculate skill average
        skill_levels = [s["level"] for s in self.progress["skills"].values()]
        avg_skill = sum(skill_levels) / len(skill_levels) if skill_levels else 0
        
        return {
            "active_courses": len(self.progress["active_courses"]),
            "completed_courses": len(self.progress["completed_courses"]),
            "average_course_progress": round(avg_progress, 1),
            "learning_hours_this_month": self.progress["learning_hours_this_month"],
            "average_skill_level": round(avg_skill, 1),
            "skill_gaps": [
                {"skill": k, "gap": v["target"] - v["level"]}
                for k, v in self.progress["skills"].items()
                if v["target"] > v["level"]
            ]
        }
    
    def run(self):
        print("[LEARNING] Running learning progress analysis...")
        
        # 1. Get report
        report = self.get_learning_report()
        
        # 2. Suggest resources
        suggestions = self.suggest_resources()
        
        # 3. Determine status
        if report["average_skill_level"] >= 8.5:
            status = "GREEN"
        elif report["average_skill_level"] >= 7.0:
            status = "YELLOW"
        else:
            status = "RED"
        
        # 4. Write sentinel
        sentinel_data = {
            "agent": "learning_agent",
            "message": f"Skills: {report['average_skill_level']}/10 | Courses: {report['active_courses']} active, {report['completed_courses']} done",
            "status": status,
            "report": report,
            "suggestions": suggestions[:3],  # Top 3
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "learning_agent.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[LEARNING] Status: {status} | Avg Skill: {report['average_skill_level']}/10")
        print(f"[LEARNING] {len(suggestions)} skill gaps identified")


if __name__ == "__main__":
    LearningAgent().run()
