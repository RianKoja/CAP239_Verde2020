# Matemática Computacional I - parte A - Prova - Branch Direita - Modelo COVID
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 02/06/2020 - V1.0
#
#
# Descrição
#
# Implemente as equações do MODELO IMC-SF-COVID19 e calcule os valores de g e s para os próximos 20 dias.
#
# Entradas:
#
# - N: (Inteiro) - Número de dias de previsão
# - prob_agent: (Dicionario: {String: Array de Floats}: Dicionário para configuração dos espectros de probabilidade.
# - coluna_agrupadora_covid: (String) = nome da coluna para agrupar a série. Ex. 'location'
# - coluna_serie_covid: (String) Nome da coluna da série, ex:  'new_cases'
# - valor_coluna_agrupador: (String) Valor da coluna agrupadora. Ex: 'Bolivia'
# - coluna_data: (String) Nome da coluna que contém a data. Ex: 'date'
# - data_inicial: (String) Data inicial da serie. Ex: '2020-05-09'
# - num_dias_para_media: (Inteiro) Número de dias de média a ser considerada para inicialização do modelo
# - data_inicial_previsao: (String) Data Inicial de previsão. Ex: '2020-05-16'
# - data_final: (String) Data final de dados Reais. Ex: '2020-06-05'
# - estrategia_g: (String) Estrategia a ser usada para cálculo de g na previsão:
#     - 'Media' - Estratégia padrão, conforme modelo da prova
#     - 'Fixo'  - Valor fixo para g. O valor é determinado no parâmetro 'g_fixo'
#     - 'Ajuste'- Estratégia desenvolvida que utiliza o valor médio entre os mínimos e máximos calculados para prever g.
# - g_fixo = 0.25
#   Ex = {'Espectro 1': [0.5, 0.45, 0.05], 'Espectro 2': [0.7, 0.25, 0.05]}
# - fator_n_min: (Array de Floats) Fatores "n" mínimos. Ex = [2.0, 4.0, 5.0]
# - fator_n_max: (Array de Floats) Fatores "n" máximos. Ex = [4.0, 7.0, 10.0]
# - is_atualizar_arquivo_covid: (Boolean) True para atualizar o arquivo da covid da url do parâmetro
#   'url_owid_covid_data'
# - url_owid_covid_data: : (String) Url para baixar arquivo da COVID.
#   Ex:'https://covid.ourworldindata.org/data/owid-covid-data.csv'
# - nome_arq_covid_completo: (String) Nome do arquivo da covid a salvar. Ex: './owid-covid-data.csv'
#
# Saídas
#
# - Uma figura contendo o fator de supressão e o fator g, dos espectros definidos
# - Uma figura para cada espectro de probabilidades, contendo as previsões, os dados observados e as médias
#

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def calcula_media_dia(n_nb7, n_k, num_dias_para_media, indice_atual):
    n_nb7[indice_atual] = np.mean(n_k[max(indice_atual - num_dias_para_media + 1, 0): indice_atual + 1])


def inicializa_medias_e_g_no_periodo(g_espectro_inicial, n_nb7, n_k, num_dias_para_media, indice_inicial, indice_final,
                                     estrategia_g='Media',
                                     g_fixo=None, prob_agent=None, fator_n_min=None, fator_n_max=None, g_atual=None):
    for t in range(indice_inicial, indice_final + 1):
        calcula_media_dia(n_nb7, n_k, num_dias_para_media, t)
        # calcula g
        g_espectro_inicial[t] = calcula_g_estrategia(n_nb7, n_k, t, estrategia_g, g_fixo, prob_agent,
                                                     fator_n_min, fator_n_max,
                                                     g_atual)
        print(" Para casos = {}, media = {} ====> g = {}".format(n_k[t], n_nb7[t], g_espectro_inicial[t]))

    return n_nb7, g_espectro_inicial


def calcula_g_estrategia(n_nb7, n_k, t, estrategia_g='Media', g_fixo=None, prob_agent=None, fator_n_min=None,
                         fator_n_max=None, g_atual=None, estrategia_n8=None):
    if estrategia_g == 'Media':
        n_k_t = n_k[t]
        n_nb7_t = n_nb7[t - 1]
        if n_k_t > n_nb7_t:
            # formula 6
            g = n_nb7_t / n_k_t
        else:
            if n_nb7_t == 0:
                g = 0
            else:
                # formula 7
                g = n_k_t / n_nb7_t
    elif estrategia_g == 'Fixo':
        g = g_fixo
    elif estrategia_g == 'Ajuste':
        n_k_t = n_k[t]
        n_nb7_t = n_nb7[t - 1]
        n8_min = calcula_extremos(prob_agent, fator_n_min, n_k_t,  n_k, n_nb7, t, g_atual, estrategia_n8)
        n8_max = calcula_extremos(prob_agent, fator_n_max, n_k_t,  n_k, n_nb7, t, g_atual, estrategia_n8)
        n_k_t_ajuste = (n8_min + n8_max) / 2
        if n_k_t_ajuste > n_nb7_t:
            g = n_nb7_t / n_k_t_ajuste
        else:
            if n_nb7_t == 0:
                g = 0
            else:
                g = n_k_t_ajuste / n_nb7_t
    else:
        raise Exception('Estratégia inexistente')
    return g


def calcula_extremos(prob_agent, fator_n, n_k, n_nb7, t, g, estrategia_n8):
    n_8 = 0
    n_k_t = n_k[t]
    n_nb7_t = n_nb7[t - 1]
    for i in range(len(prob_agent)):
        n_8 += prob_agent[i] * fator_n[i]
    if estrategia_n8 == 'UpDown':
        if n_k_t < n_nb7_t:
            n_8 = n_nb7_t - (g * n_k_t)
        else:
            n_8 = n_k_t + n_8 * g
    else:
        n_8 = n_8 * g * n_k_t
    n_8 = int(n_8)

    return n_8


def run(cfg, df_covid_pais_na_data):
    # TODO
    is_plot = False

    # dias de inicialização
    df_covid_pais_date = pd.DataFrame()
    df_covid_pais_date[cfg.coluna_data] = pd.to_datetime(df_covid_pais_na_data[cfg.coluna_data])

    mascara_data = (df_covid_pais_date[cfg.coluna_data] >= cfg.data_inicial) & (
            df_covid_pais_date[cfg.coluna_data] < cfg.data_inicial_previsao)
    df_covid_pais_datas_inicializacao = df_covid_pais_na_data.loc[mascara_data]
    num_dias_inicializacao = len(df_covid_pais_datas_inicializacao)

    s = {}
    g = {}
    for espectro in cfg.prob_agent.keys():
        # dicionario de fator de supressão, por espectro
        s[espectro] = [0.0] * (cfg.N + num_dias_inicializacao + 1)
        # dicionario de fator g, por espectro
        g[espectro] = [0.0] * (cfg.N + num_dias_inicializacao + 1)

    n_k_real = df_covid_pais_na_data[cfg.coluna_serie_covid].to_list()

    # executa para cada espectro de probabilidades
    for espectro_a_executar in cfg.prob_agent.keys():
        # normalizacao
        prob_agent_norm = np.array(cfg.prob_agent[espectro_a_executar]) / np.sum(cfg.prob_agent[espectro_a_executar])

        # número de casos no dia - depois são adicionados os dias de inicialização no início da lista
        n_k = [0.0] * (cfg.N + 1)
        n_k = df_covid_pais_datas_inicializacao[cfg.coluna_serie_covid].to_list() + n_k

        # média de "num_dias_para_media" dias no dia
        n_nb7 = [0.0] * (cfg.N + 1 + num_dias_inicializacao)
        # inicializa médias e g com estrategia de inicializacao
        n_nb7[0] = n_k[0]
        g0 = cfg.g0
        n_nb7, g[espectro_a_executar] = inicializa_medias_e_g_no_periodo(g[espectro_a_executar], n_nb7, n_k,
                                                                         cfg.num_dias_para_media, 1,
                                                                         num_dias_inicializacao - 1,
                                                                         estrategia_g=cfg.estrategia_g_inicializacao,
                                                                         g_fixo=cfg.g_fixo, prob_agent=prob_agent_norm,
                                                                         fator_n_min=cfg.fator_n_min,
                                                                         fator_n_max=cfg.fator_n_max,
                                                                         g_atual=g0)
        # loop t = ultimo dia de caso real até data_final
        for t in range(num_dias_inicializacao - 1, cfg.N + num_dias_inicializacao):

            print('Previsão de hoje + {} dias ... ~~~~~~~~~~~~~~~~~~~~~~~~~~~'.format(t - num_dias_inicializacao + 1))
            print('{} = {}'.format(cfg.coluna_serie_covid, n_k[t]))

            # calcula g de acordo com a estrategia
            g[espectro_a_executar][t] = calcula_g_estrategia(n_nb7, n_k, t, estrategia_g=cfg.estrategia_g,
                                                             g_fixo=cfg.g_fixo,
                                                             prob_agent=prob_agent_norm, fator_n_min=cfg.fator_n_min,
                                                             fator_n_max=cfg.fator_n_max,
                                                             g_atual=g0)

            # Calculando o valor minimo do intervalo n_k, n_nb7, t,  g, estrategia_g
            n8_min = calcula_extremos(prob_agent_norm, cfg.fator_n_min, n_k, n_nb7, t, g[espectro_a_executar][t],
                                      cfg.estrategia_n8)
            # Calculando o valor maximo do intervalo
            n8_max = calcula_extremos(prob_agent_norm, cfg.fator_n_max, n_k, n_nb7, t, g[espectro_a_executar][t],
                                      cfg.estrategia_n8)

            # Calculando delta_g ...
            q_g = (1 - g[espectro_a_executar][t]) ** 2
            q_g0 = (1 - g0) ** 2
            if g0 < g[espectro_a_executar][t]:
                delta_g = (g0 - g[espectro_a_executar][t]) - q_g
            else:
                delta_g = (g0 - g[espectro_a_executar][t]) + q_g0

            # formula 8
            delta_n_k = (n_nb7[t] - n_k[t]) / n_k[t]
            # formula 9
            s[espectro_a_executar][t + 1] = (2 * delta_g + delta_n_k) / 3

            print('g0 = {}, g = {} , delta_g = {}'.format(g0, g[espectro_a_executar][t], delta_g))
            print('Mín de casos = {}'.format(n8_min))
            print('Máx de casos = {}'.format(n8_max))
            print('Média dos últimos {} dias = {}'.format(cfg.num_dias_para_media, n_nb7[t]))
            print('Fator de supressão s = {}'.format(s[espectro_a_executar][t]))
            print('')

            # calcula número de casos médio, para amanhã
            n_k[t + 1] = (n8_min + n8_max) / 2
            g0 = g[espectro_a_executar][t]
            # calcula média móvel, para amanhã, dos últimos dias
            calcula_media_dia(n_nb7, n_k, cfg.num_dias_para_media, t + 1)

        # plot erro
        plt.close('all')
        plt.figure(figsize=(16, 9))
        len_min_prev_real = min(len(n_k), len(n_k_real))
        err_prev_real = abs((np.array(n_k[0:len_min_prev_real]) - np.array(n_k_real[0:len_min_prev_real])))
        plt.errorbar(range(len(n_k[0:len_min_prev_real])), n_k[0:len_min_prev_real], yerr=err_prev_real,
                     ecolor='black')
        # plot previsto
        plt.plot(range(len(n_k)), n_k, label=espectro_a_executar)
        # plot media
        plt.plot(range(len(n_nb7)), n_nb7, alpha=1, color='magenta', label='{} - Média'.format(espectro_a_executar))

        # plot real
        plt.plot(range(len(n_k_real)), n_k_real, alpha=1, color='orange', label='Observado')
        label_serie = cfg.coluna_serie_covid.capitalize()
        label_estrategia = cfg.estrategia_g if cfg.estrategia_g != 'Fixo' else '{}={}'.format(cfg.estrategia_g,
                                                                                              cfg.g_fixo)
        titulo = '{} {} - Espectro: {}\nEstratégia g: {} - Dias de média: {} ' \
                 '\nPeriodo:{}/{} - Inicio Prev: {} ({} dias)'.format(cfg.valor_coluna_agrupador, label_serie,
                                                                      espectro_a_executar, label_estrategia,
                                                                      cfg.num_dias_para_media, cfg.data_inicial,
                                                                      cfg.data_final, cfg.data_inicial_previsao, cfg.N)
        plt.xticks(range(len(n_k_real)))
        plt.title(titulo)
        plt.xlabel('dias')
        plt.ylabel(label_serie)
        plt.legend()
        if is_plot:
            plt.savefig(
                './previsao_{}_espctro_{}_estrateg_{}_diasMedia_{}.png'.format(cfg.valor_coluna_agrupador,
                                                                               espectro_a_executar,
                                                                               cfg.estrategia_g,
                                                                               cfg.num_dias_para_media))
            plt.show()
        else:
            plt.draw()
    return g, s, n_k, n_k_real


def plot_g_s(cfg, g, s, n_k_real):
    # TODO
    is_plot = False
    # plot Fator de Supressão e g
    plt.close('all')
    plt.figure(figsize=(16, 9))
    for espectro in s.keys():
        # plot s
        plt.plot(range(len(s[espectro])), s[espectro], label='s Espectro {}'.format(espectro))
        plt.plot(range(len(g[espectro])), g[espectro], label='g Espectro {}'.format(espectro))

    label_serie = cfg.coluna_serie_covid.capitalize()
    label_estrategia = cfg.estrategia_g if cfg.estrategia_g != 'Fixo' else '{}={}'.format(cfg.estrategia_g, cfg.g_fixo)
    titulo = '{} {} - Estratégia g: {} - Dias de média: {} \nPeriodo:{}/{} - Inicio Prev: {} ({} dias)'.format(
        cfg.valor_coluna_agrupador, label_serie,
        label_estrategia, cfg.num_dias_para_media, cfg.data_inicial, cfg.data_final, cfg.data_inicial_previsao, cfg.N)
    plt.xticks(range(len(n_k_real)))
    plt.title(titulo)
    plt.xlabel('dias')
    plt.ylabel('Fator de Supressão e g')
    plt.legend()
    if is_plot:
        plt.savefig(
            './supressao_{}_estrateg_{}_diasMedia_{}.png'.format(cfg.valor_coluna_agrupador, cfg.estrategia_g,
                                                                 cfg.num_dias_para_media))
        plt.show()
    else:
        plt.draw()
