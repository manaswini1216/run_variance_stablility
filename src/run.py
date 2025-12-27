import json
import os
from matcher import match_objects, consolidate_runs
from metrics import agreement_rate, polarity_flip_rate, bucket_drift_rate

DATA_DIR = "../data"
OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(os.path.join(DATA_DIR, "journals.jsonl")) as f:
    journals = [json.loads(line) for line in f]
runs_by_journal = {}
for journal in journals:
    jid = journal['journal_id']
    runs = []
    for run_num in range(1, 4):
        run_path = os.path.join(DATA_DIR, f"llm_runs/{jid}/run_{run_num}.json")
        with open(run_path) as rf:
            runs.append(json.load(rf))
    runs_by_journal[jid] = runs

stability_report = {}
stable_all_journals = {}

for jid, runs in runs_by_journal.items():
    print(f"Processing {jid}...")
    matches_12 = match_objects(runs[0]['items'], runs[1]['items'])
    matches_13 = match_objects(runs[0]['items'], runs[2]['items'])
    
    report = {
        'agreement_run1_vs_run2': agreement_rate(matches_12, len(runs[0]['items'])),
        'agreement_run1_vs_run3': agreement_rate(matches_13, len(runs[0]['items'])),
        'polarity_flip_run1_vs_run2': polarity_flip_rate(matches_12),
        'polarity_flip_run1_vs_run3': polarity_flip_rate(matches_13),
        'bucket_drift_run1_vs_run2': bucket_drift_rate(matches_12),
        'bucket_drift_run1_vs_run3': bucket_drift_rate(matches_13)
    }
    stability_report[jid] = report
    
    stable_items = consolidate_runs(runs)
    stable_all_journals[jid] = stable_items
    
    with open(os.path.join(OUTPUT_DIR, f"{jid}_stable.json"), "w") as f:
        json.dump(stable_items, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "stable_all_journals.json"), "w") as f:
    json.dump(stable_all_journals, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "stability_report.json"), "w") as f:
    json.dump(stability_report, f, indent=2)

print("✅ Done! Outputs saved in:", OUTPUT_DIR)
