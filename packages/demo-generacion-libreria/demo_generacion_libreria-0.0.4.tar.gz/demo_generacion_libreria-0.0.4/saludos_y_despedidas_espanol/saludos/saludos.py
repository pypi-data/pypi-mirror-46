import pandas as pd


def buenos_dias_print(nombre_persona: str):
    """
    Da los buenos días a la persona indicada
    :param nombre_persona: Nombre de la persona a la que se quieren dar los buenos días
    :return:
    """
    print('Buenos días ' + nombre_persona + '!')


def print_hola_mundo():
    """
    Printea el hola mundo
    :return: None
    """
    print('Hola mundo')


def df_con_todos_los_saludos():
    """
    Devuelve varios saludos
    :return: Devuelve varios saludos en un dataframe
    """
    df_con_saludos = pd.DataFrame({'SALUDOS': ['Buenos dias', 'Qué vas a hacer hoy?']})
    return df_con_saludos
