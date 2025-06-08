from typing import List, Dict

def create_resume_document(file_name, text, scores, keywords, entities):
    return {
        "file_name": file_name,
        "raw_text": text,
        "scores": {
            "semantic": float(scores[0]),
            "graph": float(scores[1]),
            "rule_based": float(scores[2]),
            "cultural_fit": float(scores[3]),
            "final": float(scores[4])
        },
        "keywords_matched": keywords,
        "entities": entities
    }

