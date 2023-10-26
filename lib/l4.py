from random import gauss, sample, choice
from pandas import DataFrame, Index, Series
from numpy import nan, array
from faker import Faker

def create_df():

    fake = Faker()

    N_ROWS = 1000
    N_NANS = int(N_ROWS * gauss(0.15, 0.03))
    JOBS_POPULARITY = [6, 4, 1, 2, 5, 3]

    alph = list("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890")
    body_mass_indexes = [gauss(23, 3) for i in range(N_ROWS)]

    jobs = Series({"Software developer" : (0.9, 0.1), 
                "Full stack developer" : (1.1, 0.1), 
                "Project manager" : (1.1, 0.2), 
                "AI architect" : (1.2, 0.16), 
                "Data scientist" : (1.3, 0.2), 
                "Blockchain developer" : (1.1, 0.3)})

    ids = [''.join(sample(alph, k=8, counts=[5] * (len(alph) - 10) + [11] * 10)) for i in range(N_ROWS)]
    heights = [round(gauss(175, 13), 1) for i in range(N_ROWS)]
    weights = [round(body_mass_indexes[i] * (heights[i] / 100) ** 2, 1) for i in range(N_ROWS)]
    jobs_col = sample(list(jobs.index), k=N_ROWS, counts=map(int, array(JOBS_POPULARITY) * N_ROWS))

    df = DataFrame({"name"   : [fake.name() for i in range(N_ROWS)],
                    "birth" : [fake.date() for i in range(N_ROWS)],
                    "height" : heights,
                    "weight" : weights,
                    "job"    : jobs_col,
                    "salary" : [nan] * N_ROWS},
                index=ids)

    nans = sample(list(df.index), k=N_NANS)

    for i in df.index:
        df.at[i, "salary"] = int(gauss(100000, 5000) * gauss(jobs[df.at[i, "job"]][0], jobs[df.at[i, "job"]][1]))
        
        if i in nans:
            df.at[i, choice(df.columns)] = nan
        
        
    return df
