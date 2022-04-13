import pandas as pd
import numpy as np

def drop_test(path,img_name):
    f = pd.read_csv(path)
    print(f)
    f = f.drop(index=[0])
    print(f)
    info = pd.DataFrame(f)
    info.to_csv(path)
    f = pd.read_csv(path)
    print(f)

def read(path,column,column_content):
    f = pd.read_csv(path)
    result = f.loc[f[column] == column_content]
    result_array = np.array(result)
    result_array_list = result_array.tolist()
    print(result_array_list)
    index = result_array_list[0][0]
    print(result)
    print(type(result))
    print("index:")
    print(index)
    return index



if __name__ == '__main__':
    path = "test.csv"
    img_name = [0,1]
    column = "img_name"
    column_content = "20.jpg"
    # drop_test(path,img_name)
    index = read(path,column,column_content)