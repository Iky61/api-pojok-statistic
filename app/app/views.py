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
            objek.append(n['index'])
    
    objek_value = []
    for x in objek:
        for y in value:
            name = (x + y).lower()
            feature_target = [x, y]
            a = {'kode':name, 'option':feature_target}
            objek_value.append(a)
            
    return objek_value

# Fungsi untuk konversi minggu
def Week_Transform(x):
    a = x%4
    if a == 0:
        a = 4
        return a
    else:
        return a

# Fungsi untuk mewargling data waktu lebih rinci
def Time_Enginering(dataset):
    df = dataset

    df['Tahun'] = pd.to_datetime(df.Tanggal).dt.year
    df['No_Bulan'] = pd.to_datetime(df.Tanggal).dt.month
    df['Bulan'] = pd.to_datetime(df.Tanggal).dt.month_name()
    df['Week'] = pd.to_datetime(df.Tanggal).dt.week
    df['Week'] = df.Week.apply(lambda x: Week_Transform(x))
    df['Tgl'] = pd.to_datetime(df.Tanggal).dt.day
    df['Hari'] = pd.to_datetime(df.Tanggal).dt.day_name()
    df['Nomor'] = 1

    return df