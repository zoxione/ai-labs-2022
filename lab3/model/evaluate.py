import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.metrics import confusion_matrix
np.seterr(divide='ignore', invalid='ignore')


parser = argparse.ArgumentParser()
parser.add_argument('--ground_truth', type=str, default='', help='Путь к набору данных')
parser.add_argument('--predictions', type=str, default='', help='Путь к предсказанным данным')
args = parser.parse_args()


def exitMode():
    input('\nНажмите Enter для выхода...');


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

        # Accuracy
        accuracy = accuracy_score(X, Y)
        print("[6] Accuracy: " + str(accuracy))

        # Confusion Matrix
        confusion_matrix = confusion_matrix(X, Y)
        print("[7] Confusion Matrix: " + str(confusion_matrix))

    except Exception as e:
        print(e)
    finally:
        exitMode();
