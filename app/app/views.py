import pandas as pd

# fungsi untuk menentukan feature dan target
def Feature_Target(dataset):
    df = dataset
    
    type_ = pd.DataFrame(df.dtypes).reset_index()
    
    objek = []
    value = []
    for x in range(len(type_)):
        n = type_.iloc[x]
        if n[0] == 'O' or n[0] == 'str':
            objek.append(n['index'])
        elif n[0] == 'int' or n[0] == 'float':
            value.append(n['index'])
        else:
            None
    
    objek_value = []
    for x in objek:
        for y in value:
            name = x + ' to ' + y
            feature_target = [x, y]
            a = {'kode':name, 'option':feature_target}
            objek_value.append(a)
            
    return objek_value