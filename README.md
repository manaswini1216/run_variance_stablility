# run_variance_stablility


> Note: The `src/` folder is optional for modular code. All functionality is fully implemented in the notebook.


## Implementation Details

### 1. Stability Definition
- Two outputs are considered the **same semantic object** if they share the **domain** and **evidence span**.  
- **Stable fields:** `polarity`, `domain`, `time_bucket`, `evidence_span`  
- **Allowed to drift:** `intensity_bucket` / `arousal_bucket` and `text` wording  

### 2. Matching Algorithm
- **Primary signal:** Evidence span overlap  
- **Fallback:** Optional semantic similarity or heuristic matching  
- Deterministic and reproducible across runs  

### 3. Stability Metrics
- **Agreement rate:** Fraction of matched objects across runs  
- **Polarity flip rate:** Number of high-risk flips (`present ↔ absent`)  
- **Bucket drift rate:** Changes in `intensity_bucket` / `arousal_bucket` / `time_bucket`  
- All metrics are computed and stored in `stability_report.json`  

### 4. Bonus: Stable Output
- Produces a single, final output per journal using **majority vote**  
- Fields with disagreements are marked as `uncertain`  
- Output saved in `outputs/stable_all_journals.json` and individual per-journal JSON files  

---

## Production Implications

**Run-to-run variance** affects downstream system reliability. Key implications:

- **Downstream nudges:** Stable objects ensure recommendations or alerts are consistent, avoiding confusing or conflicting advice to users.  
- **User trust:** No polarity flips → low risk of false positives/negatives; users experience consistent system behavior. Minor bucket drift is acceptable.  
- **Auditability:** Metrics provide reproducible, quantitative evidence of system stability, making the system easy to review and defend.  
- **Safety-first handling:** Ambiguous fields are marked as `uncertain` to prevent over-confident misclassifications, maintaining a safety buffer for sensitive health contexts.  

---

## How to Run
1. Open `notebook/explore.ipynb` in Jupyter Notebook.  
2. Run all cells sequentially:  
   - Load data  
   - Match semantic objects across runs  
   - Compute stability metrics  
   - Produce final stable output (bonus)  
3. Outputs are saved in `outputs/`.  

---

## Outputs
- **Per-journal stable JSON:** `B001_stable.json`, …  
- **Combined stable output:** `stable_all_journals.json`  
- **Stability metrics report:** `stability_report.json`  

---

## Key Skills Demonstrated
- Deterministic matching of LLM outputs  
- Quantitative stability analysis  
- Risk-aware, safety-first handling of non-deterministic models  
- Bonus: Production-ready stable output  
- Clear documentation and reproducible results  



