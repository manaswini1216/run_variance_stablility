# src/matcher.py
from collections import defaultdict
from difflib import SequenceMatcher

def evidence_overlap(a, b):
    """Check if evidence spans overlap significantly."""
    return a in b or b in a

def semantic_similarity(text1, text2, threshold=0.8):
    """Optional fallback similarity measure."""
    ratio = SequenceMatcher(None, text1, text2).ratio()
    return ratio >= threshold

def match_objects(run1_items, run2_items):
    """
    Matches objects between two runs.
    Primary: evidence span overlap
    Fallback: semantic similarity
    Returns a list of tuples: (obj_run1, obj_run2)
    """
    matches = []
    used = set()
    for obj1 in run1_items:
        for i, obj2 in enumerate(run2_items):
            if i in used:
                continue
            if evidence_overlap(obj1['evidence_span'], obj2['evidence_span']):
                matches.append((obj1, obj2))
                used.add(i)
                break
            elif semantic_similarity(obj1['text'], obj2['text']):
                matches.append((obj1, obj2))
                used.add(i)
                break
    return matches

def consolidate_runs(runs):
    """
    Produces a stable output from multiple runs using majority vote.
    Fields: polarity, time_bucket, intensity_bucket/arousal_bucket
    If tie → mark 'uncertain'
    """
    from collections import Counter
    grouped = defaultdict(list)
    for run in runs:
        for item in run['items']:
            key = (item['domain'], item['evidence_span'])
            grouped[key].append(item)
    
    stable_items = []
    for key, items in grouped.items():
        stable_item = {
            'domain': key[0],
            'evidence_span': key[1],
            'text': items[0]['text'],  
        }
        for field in ['polarity', 'time_bucket', 'intensity_bucket', 'arousal_bucket']:
            values = [i.get(field, 'unknown') for i in items]
            most_common = Counter(values).most_common()
            if len(most_common) == 0:
                stable_item[field] = 'uncertain'
            elif len(most_common) == 1 or most_common[0][1] > most_common[1][1]:
                stable_item[field] = most_common[0][0]
            else:
                stable_item[field] = 'uncertain'
        stable_items.append(stable_item)
    return stable_items
