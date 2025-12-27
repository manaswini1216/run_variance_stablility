def agreement_rate(matches, total_objects):
    """Fraction of matched objects over total objects."""
    if total_objects == 0:
        return 0.0
    return len(matches) / total_objects

def polarity_flip_rate(matches):
    """Number of flips (present ↔ absent) / total matches"""
    flips = 0
    for obj1, obj2 in matches:
        if obj1['polarity'] != obj2['polarity']:
            flips += 1
    if len(matches) == 0:
        return 0.0
    return flips / len(matches)

def bucket_drift_rate(matches):
    """Compute drift in intensity/arousal/time buckets"""
    drift_count = 0
    for obj1, obj2 in matches:
        for field in ['intensity_bucket', 'arousal_bucket', 'time_bucket']:
            if obj1.get(field) != obj2.get(field):
                drift_count += 1
                break  
    if len(matches) == 0:
        return 0.0
    return drift_count / len(matches)
