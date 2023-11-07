from numpy import nan, sqrt, array
from pandas import Series, DataFrame
from random import uniform, gauss, randint, random, seed

def gen(N_AXES=2, N_CLUSTERS=3, N_ROWS=1000, s=57):
    
    seed(s)

    sigmas = array([randint(5, 10) for i in range(N_CLUSTERS)])
    centers = array([[random() * 100 for i in range(N_AXES)] for i in range(N_CLUSTERS)])

    df = DataFrame([[0 for i in range(N_AXES + 1)] for i in range(N_ROWS)])
    df.rename(columns = {N_AXES : "cluster"}, inplace=True)

    s = "abcdefghijklmnopqrstuvwxyz"
    for i in range(N_AXES):
        df.rename(columns = {i : s[i]}, inplace=True)

    for i in range(N_ROWS):
        row = df.loc[i].copy()
        row["cluster"] = randint(0, N_CLUSTERS - 1)

        for j in range(N_AXES):
            row[j] = gauss(centers[int(row["cluster"])][j], sigmas[int(row["cluster"])])

        df.loc[i] = row
    return df

def distance(a, b): # a, b - Series
    if "cluster" in a.index:
        a = a.drop("cluster")
    
    if "cluster" in b.index:
        b = b.drop("cluster")
    
    if a.size != b.size:
        print("Distance: sizes do not match")
        print(a, b)
        return 0
    
    s = 0
    for i in range(a.size):
        s += (a[i] - b[i]) ** 2
    
    return sqrt(s)

def create_centers(df, n_rows): # df - DataFrame, n - int
    if "cluster" in df.columns:
        df.drop("cluster", axis=1, inplace=True)
        
    centers = DataFrame(columns=df.columns)
    description = df.describe()
    n_columns = df.columns.size
    columns = df.columns
    
    for i in range(n_rows):
        centers.loc[i] = Series({columns[j] : uniform(description.loc["min"][j], description.loc["max"][j]) 
                             for j in range(n_columns)})
    
    return centers

def get_closest_center(a, centers): # a - Series, centers – DataFrame
    distances = [distance(a, centers.iloc[i]) for i in range(centers.shape[0])]
    
    min_index = 0
    min_d = distances[min_index]
    
    for i in range(len(distances)):
        if distances[i] < min_d:
            min_d = distances[i]
            min_index = i
    
    return min_index

def move_centers(df, centers): # df - DataFrame, centers - DataFrame
    df["cluster"] = Series([nan] * df.shape[0])
    
    res_vectors = DataFrame(columns=centers.columns)
    
    for i in range(centers.shape[0]):
        res_vectors.loc[i] = Series({centers.columns[i] : 0 for i in range(centers.columns.size)})
    
    for i in range(df.shape[0]):
        df.at[i, "cluster"] = get_closest_center(df.iloc[i, :-1], centers)
        
        for col in res_vectors.columns:
            res_vectors.at[df.loc[i, "cluster"], col] += df.loc[i, col] - centers.loc[df.loc[i, "cluster"], col]

    
    for cluster, n_values in df.value_counts("cluster").items():
        for col in res_vectors.columns:
            res_vectors.at[cluster, col] /= n_values
        
    return centers + res_vectors

def clusterize(df, centers): # df - DataFrame, centers - DataFrame
    df["cluster"] = Series([nan] * df.shape[0])
        
    for i in range(df.shape[0]):
        df.at[i, "cluster"] = get_closest_center(df.iloc[i], centers)
    df["cluster"] = df["cluster"].astype("int")
    return df

def get_centers(df, n, iter=10):
    centers = create_centers(df, n)
    for i in range(iter):
        centers = move_centers(df, centers)
    return centers
    


