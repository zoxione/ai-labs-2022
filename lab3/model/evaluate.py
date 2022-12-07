import argparse
import json
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.metrics import confusion_matrix
np.seterr(divide='ignore', invalid='ignore')


parser = argparse.ArgumentParser()
parser.add_argument('--ground_truth', type=str, default='', help='Путь к набору данных')
parser.add_argument('--predictions', type=str, default='', help='Путь к предсказанным данным')
args = parser.parse_args()


# def exitMode():
#     input('\nНажмите Enter для выхода...');


# ./evaluate.py --ground_truth ./train.csv  --predictions ./result_to_commit.csv
if __name__ == '__main__':
    try:
        print('[1] Чтение обучающих данных из файла', args.ground_truth);
        dfTrain = pd.read_csv(args.ground_truth);
        print('[2] Чтение предсказанных данных из файла', args.predictions);
        dfPredict = pd.read_csv(args.predictions);
        print('[3] Обучающие данные и предсказанные данные обработаны');

        X = dfTrain['Price'];
        Y = dfPredict['Price'];
        result = {}

        # Mean Absolute Error
        result['MAE'] = mean_absolute_error(X, Y);
        print('[4] Mean Absolute Error:', result['MAE']);

        # Accuracy
        result['Accuracy'] = accuracy_score(X, Y);
        print('[5] Accuracy:', result['Accuracy']);

        # Confusion Matrix
        # result["confusion_matrix"] = confusion_matrix(X, Y)
        # print("[5] Confusion Matrix: " + str(result["confusion_matrix"]))

        with open('result_metrics.json', 'w') as fp:
            json.dump(result, fp)

    except Exception as e:
        print(e)
    # finally:
    #     exitMode();
