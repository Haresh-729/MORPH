# Quick Start Guide: Few-Shot Clustering for Grafana Logs

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd synthetic-log-generator/notebooks
pip install -r requirements_notebooks.txt
```

This installs all required packages including:
- `sentence-transformers` for embeddings
- `hdbscan` for clustering
- `faiss-cpu` for similarity search
- Standard ML libraries (pandas, scikit-learn, etc.)

### Step 2: Verify Log Files

Ensure you have generated Grafana logs:

```bash
ls -lh ../output/grafana/logs_2024-01-01.jsonl
```

Expected: ~80MB JSONL file with 140K+ log entries

### Step 3: Run the Pipeline

**Option A: Run All Notebooks (Recommended)**

```bash
python run_clustering_pipeline.py
```

This executes all 4 notebooks sequentially:
1. Data Exploration (2-3 min)
2. Feature Engineering (3-5 min)
3. Few-Shot Clustering (10-15 min)
4. Evaluation and Analysis (5-7 min)

**Total Time**: ~25-30 minutes

**Option B: Run Individual Notebooks**

```bash
jupyter notebook
# Open and run notebooks 1 → 2 → 3 → 4 in sequence
```

**Option C: JupyterLab**

```bash
jupyter lab
# Open notebooks and run interactively
```

### Step 4: Check Outputs

After successful execution:

```bash
ls -lh ../output/grafana/

# You should see:
# - clustered_logs.parquet          (Clustered dataset)
# - embeddings.npy                  (Log embeddings)
# - faiss_index.bin                 (Similarity index)
# - cluster_summary.json            (Clustering results)
# - evaluation_report.json          (Quality metrics)
# - cluster_visualization_umap.png  (Visualization)
# - Multiple other analysis PNGs
```

### Step 5: Review Results

Open the evaluation report:

```bash
cat ../output/grafana/evaluation_report.json
```

Key metrics to check:
- **Silhouette Score**: Target > 0.85 (excellent), > 0.5 (acceptable)
- **Number of Clusters**: Typically 10-20 semantic groups
- **Noise Percentage**: Target < 15%

---

## 📊 What Each Notebook Does

### Notebook 1: Data Exploration
- Loads 140K Grafana logs
- Analyzes temporal patterns, services, dashboards
- Generates statistical summaries
- **Output**: `exploration_summary.json`

### Notebook 2: Feature Engineering
- Extracts text features from logs
- Applies semantic normalization
- Creates composite feature vectors
- **Output**: `engineered_features.parquet`, `normalized_texts.txt`

### Notebook 3: Few-Shot Clustering
- Generates Sentence-BERT embeddings
- Defines 7 few-shot categories
- Applies HDBSCAN clustering
- Builds FAISS index
- **Output**: `clustered_logs.parquet`, `embeddings.npy`, `faiss_index.bin`

### Notebook 4: Evaluation
- Calculates quality metrics
- Analyzes cluster coherence
- Generates visualizations
- **Output**: `evaluation_report.json`, multiple PNGs

---

## 🎯 Expected Results

### Sample Output

```json
{
  "clustering_results": {
    "n_clusters": 15,
    "cluster_size_mean": 8932,
    "cluster_size_std": 2341
  },
  "quality_metrics": {
    "silhouette_score": 0.72,
    "davies_bouldin_score": 0.85,
    "cluster_balance_score": 0.78
  }
}
```

### Interpretation

- **Silhouette 0.72**: Good clustering quality ✅
- **15 clusters**: Reasonable number of semantic groups ✅
- **Balance 0.78**: Well-distributed clusters ✅

---

## 🔧 Troubleshooting

### Issue: Import Error for sentence-transformers

```bash
pip install sentence-transformers torch
```

### Issue: FAISS not found

```bash
# For CPU
pip install faiss-cpu

# For GPU (if CUDA available)
pip install faiss-gpu
```

### Issue: Memory Error

Reduce batch size in notebook 3:

```python
# Change from:
batch_size = 256
# To:
batch_size = 64
```

### Issue: Low Silhouette Score (< 0.5)

Try adjusting HDBSCAN parameters in notebook 3:

```python
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=100,  # Increase from 50
    min_samples=20,         # Increase from 10
    metric='cosine'         # Try cosine instead of euclidean
)
```

---

## 💡 Tips for Best Results

1. **Use GPU if Available**: Speeds up embedding generation
   ```python
   model = SentenceTransformer(model_name, device='cuda')
   ```

2. **Experiment with Models**: Try different embedding models
   - Fast: `all-MiniLM-L6-v2` (384 dim)
   - Quality: `all-mpnet-base-v2` (768 dim)

3. **Add Custom Few-Shot Examples**: Tailor to your domain
   ```python
   few_shot_examples.append({
       'label': 'custom_metric',
       'keywords': ['keyword1', 'keyword2'],
       'description': 'My custom category'
   })
   ```

4. **Save Intermediate Results**: All notebooks save outputs - you can restart from any point

5. **Iterate on Parameters**: Re-run notebook 3 with different HDBSCAN settings without re-computing embeddings

---

## 📚 Next Steps

After completing the clustering pipeline:

1. **Explore Clusters**: Open `clustered_logs.parquet` to see cluster assignments
2. **Use FAISS Index**: Query for similar logs using the saved index
3. **Integrate with MOZAIC**: Use clusters for incident correlation
4. **Extend to Other Sources**: Apply same approach to Kubernetes, Sentry, CloudWatch logs

---

## ✅ Success Checklist

- [ ] All dependencies installed
- [ ] Log file exists (140K+ entries)
- [ ] All 4 notebooks executed successfully
- [ ] Output files generated
- [ ] Silhouette score > 0.5
- [ ] Visualizations reviewed
- [ ] Evaluation report shows good metrics

---

## 🆘 Need Help?

- **Read**: Full README.md in this directory
- **Check**: Inline comments in notebooks
- **Review**: Troubleshooting section above
- **Examine**: Error messages in notebook outputs

---

**Happy Clustering! 🎉**

*Part of the MOZAIC project - Multi-Source Orchestrated Zephyr Anomaly Intelligent Coordinator*
