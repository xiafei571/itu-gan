# itu-gan

1. ITUGan.ipynb 
  - select type n as the original data
  - generate datetime_file list

2. TimeGAN.ipynb
  - Load data
  - Run TimeGAN for synthetic time-series data generation

3. extractTypeN.sh (option)
  - move typeN files to a folder

4. generate_json.py
  - Modify the parameters of `generate_json.py`, then run `generate_json.py`. This process will take a long time. You can use the following command:
  - `nohup python -u generate_json.py > generate.log 2>&1` 
