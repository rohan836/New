# ARC-AGI Research Project

- Trains a standard transformer model for ARC-AGI-1
- 75M parameters
- Reported performance: **44%** on the ARC-AGI-1 public evaluation
- Reported training cost: **~$0.67** using 2 hours on a 5090

## Deployment

1) Rent a 5090 and ensure CUDA >12.8, ideally >13.0  
2) Create a virtual environment and install `torch`, `numpy`, `numba`, `matplotlib` and `flash-attn`  
3) Download and build the dataset  
4) (optional) delete raw data, solutions file and dataset scripts to test for data leakage  
5) Run the training and inference script  

This script takes care of (3)-(5):

```bash
git clone https://github.com/rohan836/New.git
cd New

# download and build the datasets
cd dataset_building_scripts
python download_and_group.py
python build_datasets.py arc1 --add-conceptarc --with-filtered
cd ..

# prove no data leakage (optional, uncomment to run)
# rm -r assets_tmp # deletes raw data
# rm assets/solutions.json # deletes solutions file
# rm -r dataset_building_scripts # deletes dataset related files

# run the training + inference script
python run_script.py high # Choose between 3 modes: low, medium, high
```

Note: To get the best speed, logging loss values is disabled.

## Citation

```bibtex
@misc{bhise2026arcagi,
  author       = {Rohan bhise},
  title        = {ARC-AGI Research Project},
  year         = {2026},
  url          = {https://github.com/rohan836/New},
}
```
