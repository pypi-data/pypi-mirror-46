import pandas as pd


def fix_month_format(element):
    meses = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'sept': 8,
         'oct': 8, 'nov': 8, 'dic': 12}
    for word, initial in meses.items():
        element = element.replace(word, '0' + str(initial))
    return element


def fix_date_format(df_, date_format='%d %m %Y %H:%M'):
    if len(df_.hour[0]) == 33:
        df2 = df_['hour'].map(lambda x: fix_month_format(str(x)[5:-11]))
    else:
        df2 = df_.hour
    df2 = pd.to_datetime(df2, format=date_format)
    # cambio las columnas
    df_ = df_.drop(columns=['hour'])
    df_['date_time'] = df2
    return df_


def df_casa_sensor(df_, house_number, sensor_):
    df_grouped = df_.groupby(['casa', 'sensor'])
    df_dates = pd.DataFrame(df_grouped['date_time'].apply(list).values.tolist(), index=df_grouped.groups)
    df_weights = pd.DataFrame(df_grouped['value'].apply(list).values.tolist(), index=df_grouped.groups)

    df_dates.columns = df_dates.columns * 2
    df_weights.columns = df_weights.columns * 2 + 1

    res = pd.concat([df_dates, df_weights], axis=1).sort_index(1)

    if type(sensor_) == str:
        df_one_row = res.loc[str(house_number)].T[sensor_].values
    else:
        # empezando por el sensor 0
        df_one_row = res.loc[str(house_number)].iloc[sensor_].values
    date_time = [df_one_row[i] for i in range(len(df_one_row)) if i % 2 == 0]
    values = [df_one_row[i] for i in range(len(df_one_row)) if i % 2 == 1]

    return pd.DataFrame({'date_time': date_time, 'values': values})


def new_frecuency(df_, frecuency=60, start_date=None, end_date=None):
    # frecuency in minutes

    #     df_['date_time'] = pd.to_datetime((df_['date_time'].
    #                                   astype(np.int64)//10**9 * 10**9).astype('datetime64[ns]'))
    if start_date == None:
        start_date = df_.dropna().date_time[0]
    if end_date == None:
        end_date = df_.dropna().date_time.values[-1]
    new_range = pd.date_range(start_date, end_date, freq=str(frecuency) + 'min')
    df_new_range = pd.DataFrame(data=new_range, columns=['date_time'])
    df_new_range['0'] = ''

    df2_ = pd.concat([df_, df_new_range], sort=True).sort_values(by='date_time')
    return df2_.interpolate().dropna().drop(['0'], axis=1).set_index('date_time')  # PODRIA SER MULTIHILO


def get_df_casa(df_, house_number, frecuency=60):
    if str(house_number) not in df_.casa.unique():
        return 'House data not available'
    sensors = df_[df_.casa == str(house_number)].sensor.unique()
    casa_df = pd.DataFrame()
    start_date = df_[df_.casa==str(house_number)].dropna()['date_time'].iloc[0]
    end_date = df_[df_.casa==str(house_number)].dropna()['date_time'].iloc[-1]
    for sensor_ in sensors:
        new_df = new_frecuency(df_casa_sensor(df, house_number, sensor_), frecuency, start_date, end_date)
        new_df.columns = [sensor_]
        casa_df = pd.concat([new_df, casa_df], axis=1)
    return casa_df.dropna()