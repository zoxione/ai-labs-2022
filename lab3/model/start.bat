@echo off
python ./model.py --mode train --dataset ./train.csv --model ./model_linearRegression.pkl
python ./model.py --mode inference --model ./model_linearRegression.pkl --input ./train.csv --output ./result_to_commit.csv
python ./evaluate.py --ground_truth ./train.csv  --predictions ./result_to_commit.csv