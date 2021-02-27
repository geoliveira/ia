import numpy as np

'''
funcao logistica/ funcao de ativacao
    z representa w.T*x
    valor retornado pertence ao internvalo (0,1)
    sigmoid(z) representa probabilidade de ser uma das duas classes, mas principalmente a classe 1
    Classe 1 
        se sigmoid(w.T*x) = 0.5 c/ w.T*x = 0 (threeshold)
        se sigmoid(w.T*x) tende a + infinito (w.T*x >= 0.5)
    Classe 2 (i.e, nao classe 1)
        se sigmoid(w.T*x) tende a - infinito (w.T*x < 0.5)

'''
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

'''
binary cross entropy (funcao de erro/custo) 
    (y = 1)
        -log(y_hat)
        obs: y_hat/sigmoid retorna sempre valores (0,1) e o log desses valores sao sempre negativos, por isso o sinal de menos
    (y = 0)
        -log(1-y_hat)

    -y*log(y_hat) - (1-y)*log(1-y_hat)
'''
def cost(w, X, y):
    linhas,colunas = X.shape
    return -(np.sum(y * np.log(sigmoid(X.dot(w))) + (1 - y) * np.log(1 - sigmoid(X.dot(w)))) / linhas)

def gradient(w, X, y):
    linhas,colunas = X.shape
    return 1/linhas * (X.T).dot( sigmoid(X.dot(w)) - y )

def normalize(X):
    X_norm = X
    mu = np.zeros(X.shape[1])
    sigma = np.zeros(X.shape[1])

    mu =    np.vstack((X[0].mean(), X[1].mean()))
    sigma = np.vstack((X[0].std(ddof=1), X[1].std(ddof=1)))
    X_norm = (np.subtract(X, mu).T / sigma.T)

    return [X_norm.T, mu, sigma]

def accuracy(z, threshold=0.5):
    p = sigmoid(z) >= threshold
    return p, sigmoid(z)