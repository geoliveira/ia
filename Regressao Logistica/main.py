import pandas as pd
import numpy as np
import scipy.optimize as op

import logistic_regression as lr

def main():
    # carregando o data set
    df = pd.read_csv("wdbc.data.csv")

    # pre-processamento
    X = np.vstack((np.asarray(df.Radius.values),np.asarray(df.Texture.values)))
    y = np.asarray(df.Diagnosis.values)
    print("Dataset de X e y: {} {}\nWe'll analyse {} features".format(X.shape, y.shape, X.shape[0]))

    # secao de treinamento
    train_cut_point = int(len(df)*0.7)

    X_train = np.vstack((X[:,:train_cut_point]))
    y_train = np.array((y[:train_cut_point]))
    print("\nDataset de X_train e y_train: {} {}".format(X_train.shape, y_train.shape))

    X_train, mu, sigma = lr.normalize(X_train)

    X_train = np.vstack((np.ones(X_train.shape[1]), X_train)).T
    w = np.ones(X_train.shape[1])
    print("initial weight vector w = {}\nLet's working...".format(w))

    Opr = op.minimize(fun = lr.cost,\
                      x0 = w,\
                      args = (X_train, y_train),\
                      method ='BFGS',\
                      jac = lr.gradient)
    w = Opr.x

    # secao de testes
    X_test = np.vstack((X[:,train_cut_point:]))
    y_test = np.array((y[train_cut_point:]))
    print("\nDataset de X_test e y_test: {} {}\nTesting with\nw = \n{}\nmu = \n{}\nsigma = \n{}".format(X_test.shape, y_test.shape, w, mu, sigma))

    X_test = np.vstack((np.ones(X_test.shape[1]), X_test)).T
    right_pred = 0
    for i in range(len(X_test)):
        xi = np.asarray(X_test[i])
        xi_list = np.asarray([1,\
                            (xi[1]-mu[0])/sigma[0],\
                            (xi[2]-mu[1])/sigma[1]],\
                            dtype=float)

        result, predict = lr.accuracy(xi_list.dot(w))
        right_pred += 1 if result else 0
        print("N test {}.: Diagnostic {} - P({}) ".format(i+1, result, predict))
    print("General mean = {}\n22. {}".format(right_pred/len(X_test), y[22]))

if __name__ == '__main__':
    main()