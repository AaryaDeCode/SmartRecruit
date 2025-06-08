from typing import List, Dict

def create_resume_document(file_name: str, text: str, scores: list, keywords: list, parsed_entities: dict):
    return {
        "file_name": file_name,
        "raw_text": text,
        "scores": {
            "semantic": scores[0],
            "graph": scores[1],
            "rule_based": scores[2],
            "cultural_fit": scores[3],
            "final": scores[4],
        },
        "keywords_matched": keywords,
        "entities": parsed_entities,
    }

