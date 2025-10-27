# Few-Shot Clustering Notebooks for MOZAIC Grafana Logs

This directory contains Jupyter notebooks for implementing few-shot clustering on Grafana logs as part of the MOZAIC (Multi-Source Orchestrated Zephyr Anomaly Intelligent Coordinator) project.

## 📚 Overview

The notebooks implement a complete pipeline for:
1. **Data Exploration**: Understanding the structure and patterns in Grafana logs
2. **Feature Engineering**: Extracting and normalizing features from raw logs
3. **Few-Shot Clustering**: Applying semi-supervised clustering with domain knowledge
4. **Evaluation**: Comprehensive analysis and quality metrics

## 🎯 Objectives

- Demonstrate **few-shot learning** approach for log clustering
- Use **semantic embeddings** (Sentence-BERT) for log representation
- Apply **HDBSCAN** for density-based clustering
- Leverage **FAISS** for efficient similarity search
- Achieve **high clustering quality** (Silhouette Score > 0.85 target)
- Enable **interpretable clusters** with domain-guided labels

## 📁 Notebook Structure

### 1. Data Exploration (`1_data_exploration.ipynb`)

**Purpose**: Understand the Grafana log dataset

**Key Activities**:
- Load and parse JSONL logs
- Analyze temporal patterns
- Examine service and dashboard distributions
- Identify metric types and queries
- Generate statistical summaries

**Outputs**:
- `exploration_summary.json`: Dataset statistics
- Various visualization plots

**Run Time**: ~2-3 minutes for 140K logs

---

### 2. Feature Engineering (`2_feature_engineering.ipynb`)

**Purpose**: Prepare features for clustering

**Key Activities**:
- Extract text features (dashboard, panel, service, queries)
- Apply semantic placeholders for normalization
- Engineer temporal features (hour, day, business hours)
- Extract metric value features
- Create composite feature vectors

**Outputs**:
- `engineered_features.parquet`: Full feature set
- `clustering_features.parquet`: Clustering-ready data
- `normalized_texts.txt`: Normalized log texts

**Run Time**: ~3-5 minutes for 140K logs

---

### 3. Few-Shot Clustering (`3_fewshot_clustering.ipynb`)

**Purpose**: Apply few-shot clustering approach

**Key Activities**:
- Generate embeddings using Sentence-BERT
- Define few-shot examples (7 categories)
- Match logs to few-shot examples
- Build FAISS index for similarity search
- Apply HDBSCAN clustering
- Assign labels to clusters
- Visualize clusters with UMAP

**Few-Shot Categories**:
1. Memory Monitoring
2. Performance Metrics
3. Database Monitoring
4. Cache Metrics
5. Infrastructure Health
6. JVM Metrics
7. Availability/Uptime

**Outputs**:
- `clustered_logs.parquet`: Logs with cluster assignments
- `embeddings.npy`: Sentence-BERT embeddings
- `faiss_index.bin`: FAISS similarity search index
- `cluster_summary.json`: Clustering summary
- `cluster_visualization_umap.png`: UMAP visualization

**Run Time**: ~10-15 minutes for 140K logs

---

### 4. Evaluation and Analysis (`4_evaluation_and_analysis.ipynb`)

**Purpose**: Comprehensive evaluation of clustering results

**Key Activities**:
- Calculate quality metrics (Silhouette, Davies-Bouldin, Calinski-Harabasz)
- Per-cluster silhouette analysis
- Cluster coherence evaluation
- Confusion matrix between few-shot labels and clusters
- Cluster size distribution analysis
- Generate comprehensive reports

**Quality Metrics**:
- **Silhouette Score**: Measures cluster separation (target: > 0.85)
- **Davies-Bouldin Index**: Measures cluster compactness (lower is better)
- **Calinski-Harabasz Score**: Variance ratio criterion
- **Cluster Balance Score**: Distribution uniformity

**Outputs**:
- `evaluation_report.json`: Comprehensive metrics
- `silhouette_analysis.png`: Per-cluster quality
- `cluster_coherence.png`: Coherence metrics
- `confusion_matrix.png`: Few-shot vs clusters
- `cluster_size_distribution.png`: Size analysis

**Run Time**: ~5-7 minutes for 140K logs

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install required packages
pip install -r requirements_notebooks.txt
```

### Running the Notebooks

**Option 1: Sequential Execution**

Run notebooks in order (1 → 2 → 3 → 4):

```bash
jupyter notebook
# Open and run each notebook in sequence
```

**Option 2: JupyterLab**

```bash
jupyter lab
```

**Option 3: Command Line Execution**

```bash
# Convert to Python scripts and run
jupyter nbconvert --to script 1_data_exploration.ipynb
python 1_data_exploration.py

# Or use papermill for parameterized execution
papermill 1_data_exploration.ipynb output_1.ipynb
```

### Expected Outputs

After running all notebooks, the `output/grafana/` directory will contain:

```
output/grafana/
├── logs_2024-01-01.jsonl              # Original logs (input)
├── exploration_summary.json           # Dataset statistics
├── engineered_features.parquet        # Processed features
├── clustering_features.parquet        # Clustering-ready data
├── normalized_texts.txt               # Normalized log texts
├── embeddings.npy                     # Sentence-BERT embeddings
├── faiss_index.bin                    # FAISS similarity index
├── clustered_logs.parquet             # Final clustered data
├── cluster_summary.json               # Clustering summary
├── evaluation_report.json             # Evaluation metrics
├── cluster_visualization_umap.png     # UMAP visualization
├── silhouette_analysis.png            # Silhouette scores
├── cluster_coherence.png              # Coherence metrics
├── confusion_matrix.png               # Label confusion matrix
└── cluster_size_distribution.png      # Size distribution
```

---

## 🔧 Configuration and Customization

### Adjust Embedding Model

In `3_fewshot_clustering.ipynb`:

```python
# Fast model (default)
model_name = 'all-MiniLM-L6-v2'  # 384 dimensions, ~40MB

# High quality model
model_name = 'all-mpnet-base-v2'  # 768 dimensions, ~400MB

# Domain-specific model (if available)
model_name = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
```

### Adjust HDBSCAN Parameters

In `3_fewshot_clustering.ipynb`:

```python
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=50,      # Increase for larger clusters
    min_samples=10,           # Increase for stricter clustering
    metric='euclidean',       # Try 'cosine' for semantic clustering
    cluster_selection_method='eom',  # Try 'leaf' for more balanced clusters
)
```

### Add Custom Few-Shot Examples

In `3_fewshot_clustering.ipynb`:

```python
few_shot_examples.append({
    'label': 'custom_category',
    'keywords': ['keyword1', 'keyword2', 'keyword3'],
    'description': 'Description of the category'
})
```

---

## 📊 Expected Results

### Target Metrics (MOZAIC Goals)

- **Silhouette Score**: > 0.85 (excellent clustering)
- **Clustering Accuracy**: > 85%
- **False Positive Rate**: < 15%
- **Response Time**: < 30 seconds

### Typical Results (140K logs)

- **Number of Clusters**: 10-20 semantic groups
- **Silhouette Score**: 0.6-0.8 (good to excellent)
- **Noise Ratio**: 5-15% (unclustered logs)
- **Processing Time**: ~25-30 minutes (total pipeline)

---

## 🧪 Testing and Validation

### Validate Clustering Quality

```python
# In notebook 4
silhouette_score > 0.5  # Minimum acceptable
davies_bouldin_score < 1.0  # Good separation
balance_score > 0.6  # Reasonably balanced
```

### Verify Few-Shot Effectiveness

```python
# Check how many logs matched few-shot examples
labeled_ratio = df['fewshot_label'].notna().sum() / len(df)
# Target: > 60% for good few-shot guidance
```

### Check Cluster Coherence

```python
# Dominant service ratio per cluster
# High ratio (>70%) indicates coherent clusters
coherence_df['dominant_service_ratio'].mean()
```

---

## 🐛 Troubleshooting

### Issue: Low Silhouette Score

**Solutions**:
- Increase `min_cluster_size` in HDBSCAN
- Try different embedding models
- Add more few-shot examples
- Use cosine metric instead of euclidean

### Issue: Too Many Noise Points

**Solutions**:
- Decrease `min_cluster_size`
- Decrease `min_samples`
- Use `cluster_selection_method='leaf'`

### Issue: Memory Error

**Solutions**:
- Use smaller batch size for embeddings
- Sample data for visualization
- Use dimensionality reduction before clustering

### Issue: Slow Execution

**Solutions**:
- Use faster embedding model (all-MiniLM-L6-v2)
- Reduce UMAP sample size
- Use GPU if available (set `device='cuda'`)

---

## 📚 Key Libraries and Versions

```
sentence-transformers >= 2.2.0  # Sentence embeddings
hdbscan >= 0.8.29               # Density-based clustering
faiss-cpu >= 1.7.4              # Similarity search
umap-learn >= 0.5.3             # Dimensionality reduction
scikit-learn >= 1.0.2           # ML utilities
pandas >= 1.5.0                 # Data manipulation
numpy >= 1.23.0                 # Numerical operations
matplotlib >= 3.5.0             # Visualization
seaborn >= 0.12.0               # Statistical visualization
```

---

## 🔬 Research Context

This few-shot clustering approach contributes to MOZAIC's objectives:

1. **Zero-Shot & Few-Shot Anomaly Detection**: Demonstrates clustering without extensive labeled data
2. **Cross-Source Correlation**: Establishes patterns for correlating Grafana logs with other telemetry sources
3. **Automated Incident Labeling**: Shows LLM-based cluster labeling approach
4. **Scalable Architecture**: Uses FAISS for production-scale similarity search

---

## 📖 References

- **HDBSCAN**: McInnes, L., Healy, J., & Astels, S. (2017). "hdbscan: Hierarchical density based clustering"
- **Sentence-BERT**: Reimers, N., & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
- **FAISS**: Johnson, J., et al. (2019). "Billion-scale similarity search with GPUs"
- **UMAP**: McInnes, L., Healy, J., & Melville, J. (2018). "UMAP: Uniform Manifold Approximation and Projection"

---

## 🤝 Contributing

To extend these notebooks:

1. Add new few-shot categories based on your domain
2. Experiment with different embedding models
3. Try alternative clustering algorithms (DBSCAN, Spectral Clustering)
4. Implement temporal correlation across logs
5. Add anomaly scoring based on cluster membership

---

## 📝 Notes

- Notebooks are designed to be run sequentially (1→2→3→4)
- Each notebook saves intermediate results for the next stage
- All visualizations are saved to `output/grafana/`
- Original log files are never modified
- Embeddings and indices can be reused for inference

---

## ✅ Checklist

Before running:
- [ ] Grafana logs exist in `output/grafana/logs_2024-01-01.jsonl`
- [ ] All required packages installed
- [ ] Sufficient memory (~8GB recommended)
- [ ] Sufficient disk space (~2GB for outputs)

After running:
- [ ] All 4 notebooks executed successfully
- [ ] Output files generated in `output/grafana/`
- [ ] Silhouette score reviewed
- [ ] Cluster labels make semantic sense
- [ ] Visualizations saved and reviewed

---

**Need Help?**
- Check troubleshooting section above
- Review inline comments in notebooks
- Refer to MOZAIC project documentation

**Happy Clustering! 🎉**
