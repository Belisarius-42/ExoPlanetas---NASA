#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import plotly.express as px

df = pd.read_csv("Exoplanet_Dataset.csv")

columns_to_drop = [
    'hot_point_lon', 'star_magnetic_field', 'tzero_tr_sec_error_max',
    'tzero_tr_sec_error_min', 'tzero_tr_sec', 'tconj_error_max',
    'tconj_error_min', 'tconj', 'geometric_albedo_error_min',
    'geometric_albedo_error_max', 'tzero_vr_error_max', 'log_g',
    'geometric_albedo', 'tzero_vr', 'tzero_vr_error_min',
    'impact_parameter', 'impact_parameter_error_max', 'impact_parameter_error_min',
    'temp_calculated_error_max', 'lambda_angle', 'temp_calculated_error_min',
    'lambda_angle_error_min', 'lambda_angle_error_max', 'mag_i',
    'temp_measured', 'molecules', 'tzero_tr', 'tzero_tr_error_min',
    'tzero_tr_error_max', 'radius_error_max', 'radius_error_min',
    'temp_calculated', 'radius_measurement_type', 'star_detected_disc',
    'mag_h', 'mag_k', 'mag_j', 'inclination_error_max', 'inclination_error_min', 'mass_error_min', 'mass_error_max', 'mass_sini_error_min', 'mass_sini_error_max', 'semi_major_axis_error_min', 'semi_major_axis_error_max', 'eccentricity_error_min', 'eccentricity_error_max', 'omega', 'omega_error_min', 'omega_error_max', 'tperi', 'tperi_error_min', 'tperi_error_max','k', 'k_error_min', 'k_error_max','star_metallicity_error_min', 'star_metallicity_error_max', 'alternate_names', 'star_alternate_names'
]

df = df.drop(columns=columns_to_drop)

def add_novas_visoes(row):  #criação de uma função para criar novas colunas informativas e usar via .apply
    radius_jupiters = row['radius']
    earth_radius = radius_jupiters * 11.2

    distance_parsec = row['star_distance']
    distance_ly = distance_parsec * 3.26

    mass_mj = row['mass']   #classificar o tipo do planeta
    if pd.notna(mass_mj):
        if mass_mj <= 0.01:
            planet_type = 'Sub-Terra/Terra (< 0.01 MJ)'
        elif mass_mj <= 0.05:
            planet_type = 'Super-Terra/Mini-Netuno (0.01-0.05 MJ)'
        elif mass_mj <= 0.1:
            planet_type = 'Netuno-like (0.05-0.1 MJ)'
        elif mass_mj <= 13:
            planet_type = 'Gigante Gasoso (0.1-13 MJ)'
        else:
            planet_type = 'Anã Marrom (> 13 MJ)'
    else:
        planet_type = 'Tipo Desconhecido'

    #Status da Zona Habitável
    T_eff_sun = 5778
    R_inner_sun = 0.95
    R_outer_sun = 1.67
    
    habitable_zone_status = 'Desconhecido'
    if pd.notna(row['semi_major_axis']) and pd.notna(row['star_teff']) and pd.notna(row['star_radius']):
        stellar_luminosity_ratio = (row['star_radius'] / 1)**2 * (row['star_teff'] / T_eff_sun)**4
        inner_hz = R_inner_sun * np.sqrt(stellar_luminosity_ratio)
        outer_hz = R_outer_sun * np.sqrt(stellar_luminosity_ratio)
        
        if row['semi_major_axis'] >= inner_hz and row['semi_major_axis'] <= outer_hz:
            habitable_zone_status = 'Na Zona Habitável'
        else:
            habitable_zone_status = 'Fora da Zona Habitável'    

    #Idade da estrela (categorização)
    star_age = row['star_age']
    if pd.notna(star_age):
        if star_age <= 0.1:
            star_age_category = 'Recém formada (< 0.1 Gyr)'
        elif star_age <= 1:
            star_age_category = 'Estrelas jovens (0.1-1 Gyr)'
        elif star_age <= 10:
            star_age_category = 'Estrelas de idade média (1-10 Gyr)'
        else:
            star_age_category = 'Estrelas anciãs (>10 Gyr)'
    else:
        star_age_category = 'Desconhecido'        

    return pd.Series({
        'radius_jupiters': radius_jupiters,
        'earth_radius': earth_radius,
        'distance_parsec': distance_parsec,
        'distance_ly': distance_ly,
        'habitable_zone_status': habitable_zone_status,
        'planet_type_mass_category': planet_type,
        'star_age_category': star_age_category
    })    

df_processed = df.apply(add_novas_visoes, axis=1)
df = pd.concat([df, df_processed], axis=1)

df2 = df[[
    'name', 'planet_type_mass_category', 'habitable_zone_status', 'mass', 'earth_radius', 'orbital_period', 'discovered',
    'detection_type', 'star_name', 'distance_ly', 'star_mass',
    'star_radius', 'star_age', 'star_teff' 
]]

df2 = df2.rename(columns={
    'name': 'Nome_planeta',
    'planet_status': 'Status_planeta',
    'mass': 'Massa_planeta_xJupiter',
    'earth_radius': 'tamanho_comp_c/_Terra',
    'orbital_period': 'Periodo_orbita_dias',
    'discovered': 'Ano_descoberta',
    'detection_type': 'Metodo_detecção',
    'star_name': 'Nome_estrela',
    'distance_ly': 'Dist_anos_luz',
    'star_mass': 'Massa_estrela_c/_Sol',
    'star_radius': 'Raio_estrela_c/_Sol',
    'star_age': 'Idade_estrela_bilhao',
    'star_teff': 'Temperatura_estrela',
    'planet_type_mass_category' : 'categoria_planeta',
    'habitable_zone_status': 'Status_Zona_Habitavel' 
})

df2['Ano_descoberta'] = df2['Ano_descoberta'].astype('str').str.replace(',','')

#Inicio da parte grafica para ser exibida via plotly e streamlit

st.set_page_config(layout="wide") 
st.title("🌌Exploração de Exoplanetas catalogados pela NASA")
st.write("Uma análise interativa de dados de exoplanetas, incluindo sua massa e métodos de descoberta.")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)
col9, col10 = st.columns(2)
col11,col12 = st.columns(2)
with col1: 
    st.header("🔭 Métodos de Descoberta")
    df_descobertas = df['detection_type'].value_counts().reset_index()
    df_descobertas.columns = ['detection_type', 'count']

    fig_discovery = px.bar(df_descobertas,
        x='count',
        y='detection_type',
        title="Métodos de Descoberta dos Exoplanetas",
        labels={'detection_type' : 'Método de Descoberta', 'count': 'Número de Exoplanetas'},
        hover_data={'count':True},
        orientation='h', 
        color='count',
        color_continuous_scale=px.colors.sequential.Plasma 
    )
  
    st.plotly_chart(fig_discovery, use_container_width=True)
    st.write("A vasta maioria dos planetas foram descobertos via transito e, em menor escala, velocidade radial")

with col2:
    st.header("👽 Status da Zona Habitável")

    # Constantes Solares (aprox.)
    T_eff_sun = 5778 # Kelvin
    R_inner_sun = 0.95 # AU (limite interno conservador)
    R_outer_sun = 1.67 # AU (limite externo conservador)

    # Criar um DataFrame temporário para cálculo, removendo NaNs das colunas essenciais
    df_hz = df.dropna(subset=['semi_major_axis', 'star_teff', 'star_radius']).copy()

    if not df_hz.empty:
        # Calcular a luminosidade da estrela em relação ao Sol
        df_hz['stellar_luminosity_ratio'] = (df_hz['star_radius'] / 1)**2 * (df_hz['star_teff'] / T_eff_sun)**4

        # Calcular as bordas da zona habitável para cada estrela
        df_hz['inner_hz'] = R_inner_sun * np.sqrt(df_hz['stellar_luminosity_ratio'])
        df_hz['outer_hz'] = R_outer_sun * np.sqrt(df_hz['stellar_luminosity_ratio'])

        # Determinar se o planeta está na zona habitável
        df_hz['habitable_zone_status'] = 'Desconhecido' # Valor padrão para NaNs
        df_hz.loc[ (df_hz['semi_major_axis'] >= df_hz['inner_hz']) &
                   (df_hz['semi_major_axis'] <= df_hz['outer_hz']),
                   'habitable_zone_status'] = 'Na Zona Habitável'
        df_hz.loc[ (df_hz['semi_major_axis'] < df_hz['inner_hz']) |
                   (df_hz['semi_major_axis'] > df_hz['outer_hz']),
                   'habitable_zone_status'] = 'Fora da Zona Habitável'
        
        # Contar a frequência de cada status
        hz_counts = df_hz['habitable_zone_status'].value_counts().reset_index()
        hz_counts.columns = ['status', 'count']

        # Definir a ordem das categorias para o gráfico
        hz_order = ['Na Zona Habitável', 'Fora da Zona Habitável', 'Desconhecido']
        hz_counts['status'] = pd.Categorical(hz_counts['status'], categories=hz_order, ordered=True)
        hz_counts = hz_counts.sort_values('status')

        fig_hz = px.bar(hz_counts,
            x='count',
            y='status',
            title="Exoplanetas por Status da Zona Habitável",
            labels={'status': 'Status da Zona Habitável', 'count': 'Número de Exoplanetas'},
            orientation='h',
            color='count',
            color_continuous_scale=px.colors.sequential.Plotly3 # Um esquema de cores diferente
        )
        fig_hz.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': hz_order})
        st.plotly_chart(fig_hz, use_container_width=True)

        st.write(f"Status da zona habitável calculado para **{len(df_hz)}** de **{len(df)}** exoplanetas.")
        st.write("A zona habitável é a região ao redor de uma estrela onde a temperatura permite que a água líquida exista na superfície de um planeta. Para o calculo, precisamos da temperatura efetiva da estrela hospedeira e do semieixo maior (distância orbital) do planeta")
    else:
        st.warning("Não há dados suficientes (semi-major axis, star_teff, star_radius) para calcular e exibir o status da zona habitável.")
    
with col3: 
    st.header ("🪐 Distribuição de Massa")
    df_cleaned_mass = df.dropna(subset=['mass'])
    bins = [0, 0.1, 0.5, 1, 2, 5, 10, 15] 
    labels = ['< 0.1x Júpiter', '0.1x - 0.5x Júpiter', '0.5x - 1x Júpiter', 
              '1x - 2x Júpiter', '2x - 5x Júpiter', '5x - 10x Júpiter', '> 10x Júpiter']

    df_cleaned_mass['mass_range'] = pd.cut(df_cleaned_mass['mass'], bins=bins, labels=labels, right=True)    
    mass_range_counts = df_cleaned_mass['mass_range'].value_counts().reset_index()
    mass_range_counts = mass_range_counts.sort_values('mass_range')

    if not mass_range_counts.empty:
        fig_mass_range = px.bar(mass_range_counts,
            x='count',
            y='mass_range',
            title="Distribuição da Massa em Relação a Júpiter",
            labels={'mass_range': 'Faixa de Massa (x Júpiter)', 'count': 'Número de Exoplanetas'},
            orientation='h', # Gráfico horizontal
            color='count',
            color_continuous_scale=px.colors.sequential.Sunset # Outro esquema de cores
        )
        # Ajustar para exibir o rótulo completo da faixa de massa
        fig_mass_range.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': labels})

        st.plotly_chart(fig_mass_range, use_container_width=True)
        st.write(f"Total de {len(df_cleaned_mass)} exoplanetas com massa definida categorizados. A vasta maioria é cerca de até 0.10% do tamanho de Jupiter ")
    else:
        st.warning("Não há dados suficientes de massa para categorizar e gerar o gráfico de faixas.")

with col4:
    st.header("🌎 Tamanho do Exoplaneta (comparado com a Terra)")

    df_planet_radius = df.dropna(subset=['earth_radius']).copy()
    bins_planet_radius =[0,0.5,1,2,4,8,16,32,64, df_planet_radius['earth_radius'].max()+0.1]
    labels_planet_radius=['<0.5x Terra','0.5x-1x Terra','1x-2x Terra','2x-4x Terra','4x-8x Terra','8x-16x Terra','16x-32x Terra','32x-64x Terra','64x-78x Terra']

    df_planet_radius['planet_type_radius_category']= pd.cut(df_planet_radius['earth_radius'], bins=bins_planet_radius, labels=labels_planet_radius, right=True, include_lowest=True)
    planet_radius_counts = df_planet_radius['planet_type_radius_category'].value_counts().reset_index()
    planet_radius_counts.columns=['planet_type_radius_category', 'count']

    planet_radius_counts['planet_type_radius_category'] = pd.Categorical(
        planet_radius_counts['planet_type_radius_category'],
        categories=labels_planet_radius,
        ordered=True
    )

    planet_radius_counts=planet_radius_counts.sort_values('planet_type_radius_category')

    if not planet_radius_counts.empty:
        fig_planet_radius = px.bar(planet_radius_counts,
                                   x='count',
                                      y='planet_type_radius_category',
                                      title="Tamanho dos Exoplanetas",
                                      labels={'planet_type_radius_category':'Tamanho do Exoplaneta','count':'Número de planetas'},
                                      orientation='h',
                                      color='count', 
                                      color_continuous_scale=px.colors.sequential.Plotly3
        )
        fig_planet_radius.update_layout(yaxis={'categoryorder':'array', 'categoryarray':labels_planet_radius})

        st.plotly_chart(fig_planet_radius, use_container_width=True)
        st.write(f"Total de **{len(df_planet_radius)}** Exoplanetas classificados por seus tamanhos(em Relação a Terra)")
    else:
        st.warning("Não foi possível classificar e gerar gráfico por falta de dados")            

with col5:
    st.header("🗺️ Classificação dos planetas")

    df_planet_classification = df.dropna(subset=['mass']).copy()
    classification_bins = [0,0.01,0.05,0.1,13, df_planet_classification['mass'].max()+1]
    classification_labels = [
        'Sub-Terra/Terra (< 0.01 MJ)',
        'Super-Terra/Mini-Netuno (0.01-0.05 MJ)',
        'Netuno-like (0.05-0.1 MJ)',
        'Gigante Gasoso (0.1-13 MJ)',
        'Anã Marrom (> 13 MJ)'
    ]

    df_planet_classification['planet_type'] = pd.cut(df_planet_classification['mass'], bins=classification_bins, labels=classification_labels, right=True, include_lowest=True)
    planet_type_counts = df_planet_classification['planet_type'].value_counts().reset_index()
    planet_type_counts.columns = ['planet_type', 'count']


    planet_type_counts['planet_type'] = pd.Categorical(
        planet_type_counts['planet_type'],
        categories=classification_labels,
        ordered=True
    )
    planet_type_counts=planet_type_counts.sort_values('planet_type')

    if not planet_type_counts.empty:
        fig_planet_type= px.pie(planet_type_counts,
            values='count', 
            names='planet_type', 
            title="Tipos de Exoplanetas",
            hole=0.4 ,
            labels={'planet_type': 'Categoria do planeta', 'count':'quantidade'}
        )
        fig_planet_type.update_traces(textinfo='percent+label')
        fig_planet_type.update_layout(showlegend=True) 

        st.plotly_chart(fig_planet_type, use_container_width=True)
        st.write(f"Total de **{len(df_planet_classification)}** exoplanetas classificados por tipo de massa.")
    else:
        st.warning("Não há dados de massa suficientes para classificar e gerar o gráfico de tipos de planeta.")


with col6:
    st.header("⏳ Periodo orbital")
    df_cleaned_orbit = df.dropna(subset=['orbital_period'])
    bins_period=[0,1,10,100,1000,10000,100000,2000000]
    labels_period=['< 1 dia', '1 - 10 dias', '10 - 100 dias', 
                     '100 - 1000 dias', '1000 - 10000 dias', '10000 - 100000 dias', 
                     '> 100000 dias']
    df_cleaned_orbit ['period_range'] = pd.cut(df_cleaned_orbit['orbital_period'],
                                               bins=bins_period,labels=labels_period,right=True)
    period_range_counts = df_cleaned_orbit['period_range'].value_counts().reset_index()
    period_range_counts.columns = ['period_range','count']
    period_range_counts['period_range'] = pd.Categorical(period_range_counts['period_range'],
                                                         categories=labels_period,ordered=True)
    period_range_counts = period_range_counts.sort_values('period_range')

    if not period_range_counts.empty:
        fig_period_range = px.bar(period_range_counts,
                                  x='count',
                                  y='period_range',
                                  title="Distribuição do periodo orbital dos planetas",
                                  labels={'period_range' : 'Faixa do período orbital', 'count': 'Número de Exoplanetas'},
                                  orientation='h',
                                  color='count',
                                  color_continuous_scale=px.colors.sequential.Viridis                                   
                                  )
        fig_period_range.update_layout(yaxis={'categoryorder':'array', 'categoryarray':labels_period})

        st.plotly_chart(fig_period_range, use_container_width=True)
        st.write(f"total de Exoplanetas com período orbital calculado **{len(df_cleaned_orbit)}**. A maioria dos planetas detectados possui orbita inferior a 1 ano terrestre(365 dias)")
    else:
        st.write("Não há dados suficientes de orbita para categorizar")

with col7:
    st.header("☀️ Idade da Estrela hospedeira (1Gyr = 1bi anos)")

    df_age = df.dropna(subset=['star_age']).copy()
    bins_age=[0,0.1,1,10, df_age['star_age'].max()+1]
    labels_age=['Recém formada (< 0.1 Gyr)',
        'Estrelas jovens (0.1-1 Gyr)',
        'Estrelas de idade média (1-10 Gyr)',
        'Estrelas anciãs (>10 Gyr)']
    
    df_age['star_type_age_category'] = pd.cut(df_age['star_age'], bins=bins_age, labels=labels_age, right=True, include_lowest=True)
    age_type_counts = df_age['star_type_age_category'].value_counts().reset_index() 
    age_type_counts.columns = ['star_type_age_category','count'] 

    age_type_counts['star_type_age_category'] = pd.Categorical( 
        age_type_counts['star_type_age_category'],
        categories=labels_age,
        ordered=True
    )
    age_type_counts = age_type_counts.sort_values('star_type_age_category') 
    if not age_type_counts.empty:
        fig_star_type_age = px.pie(age_type_counts, 
                                  values='count',
                                  names='star_type_age_category',
                                  title='Idade das estrelas',
                                  hole=0.4,
                                  labels={
                                      'star_type_age_category': 'Categoria da idade: ', 'count':'Quantidade'
                                  }
                                  )
        fig_star_type_age.update_layout(yaxis={'categoryorder':'array', 'categoryarray':labels_age}) 

        st.plotly_chart(fig_star_type_age, use_container_width=True) 
        st.write(f"Total de **{len(df_age)}** Estrelas classificadas por suas idades.(Para efeitos de comparação, nosso Sol possui 4.57Gyr)")
    else:
        st.warning("Não há dados suficientes para classificar e gerar o gráfico de idades de estrelas.")

with col8:
    st.header("🌟 Massa da estrela(em massas solares)")

    df_solar_mass = df.dropna(subset=['star_mass']).copy()
    bins_star_mass = [0, 0.55, 1, 1.5, 2.5, 3.5, 6] 
    labels_star_mass = ['0.01x-0.55x', '0.55x-1.0x', '1.0x-1.5x', 
              '1.5x-2.5x', '2.5x-3.5x', '3.5x-6.0x']
    
    df_solar_mass['star_type_mass_category'] = pd.cut(df_solar_mass['star_mass'], bins=bins_star_mass, labels=labels_star_mass, right=True, include_lowest=True)
    mass_type_counts = df_solar_mass['star_type_mass_category'].value_counts().reset_index() 
    mass_type_counts.columns = ['star_type_mass_category','count'] 

    mass_type_counts['star_type_mass_category'] = pd.Categorical( 
        mass_type_counts['star_type_mass_category'],
        categories=labels_star_mass,
        ordered=True
    )
    mass_type_counts = mass_type_counts.sort_values('star_type_mass_category') 
    if not mass_type_counts.empty:
        fig_star_type_mass = px.bar(mass_type_counts, 
                                  x='count',
                                  y='star_type_mass_category',
                                  title="massa das estrelas hospedeiras",
                                  labels={'star_type_mass_category': 'Massa da estrela(Em massa solar)', 'count':'Número de Estrelas'}, 
                                  orientation='h',
                                  color='count', 
                                  color_continuous_scale=px.colors.sequential.Cividis 
                                  )
        fig_star_type_mass.update_layout(yaxis={'categoryorder':'array', 'categoryarray':labels_star_mass}) 

        st.plotly_chart(fig_star_type_mass, use_container_width=True) 
        st.write(f"Total de **{len(df_solar_mass)}** Estrelas classificadas por suas massas.(Em comparação a nosso sol)")
    else:
        st.warning("Não há dados suficientes para classificar e gerar o gráfico de massa de estrelas.")

with col9:
    st.header("☀️ Tamanho da estrela(relação ao Sol)")
    
    df_star_radius = df.dropna(subset=['star_radius']).copy()
    bins_star_radius=[0,1,5,10,20,40,df_star_radius['star_radius'].max()+0.1]
    labels_star_radius=['<=1.0','1.0x-5.0x','5.0x-10.0x','10.0x-20.0x','20.0x-40.0x','40.0x-60.0x']

    df_star_radius['star_type_radius_category']= pd.cut(df_star_radius['star_radius'],bins=bins_star_radius,labels=labels_star_radius,right=True, include_lowest=True)
    radius_type_counts=df_star_radius['star_type_radius_category'].value_counts().reset_index()
    radius_type_counts.columns=['star_type_radius_category', 'count']

    radius_type_counts['star_type_radius_category'] = pd.Categorical(
        radius_type_counts['star_type_radius_category'],
        categories=labels_star_radius,
        ordered=True
    )
    radius_type_counts = radius_type_counts.sort_values('star_type_radius_category')

    if not radius_type_counts.empty:
        fig_star_type_radius = px.bar(radius_type_counts,
                                      x='count',
                                      y='star_type_radius_category',
                                      title="Tamanho das estrelas hospedeiras",
                                      labels={'star_type_radius_category':'Tamanho da estrela','count':'Número de Estrelas'},
                                      orientation='h',
                                      color='count', 
                                      color_continuous_scale=px.colors.sequential.Plotly3)
        fig_star_type_radius.update_layout(yaxis={'categoryorder':'array', 'categoryarray':labels_star_radius})

        st.plotly_chart(fig_star_type_radius, use_container_width=True)
        st.write(f"Total de **{len(df_star_radius)}** Estrelas classificadas por seus tamanhos(em Relação a nosso sol)")
    else:
        st.warning("Não foi possível classificar e gerar gráfico por falta de dados")    

with col10:
    
    st.header("📏 Distância de nós")

    df_star_distance_plot = df.dropna(subset=['distance_ly']).copy()

    bins_distance = [0, 100, 500, 1000, 2000, 4000, 6520,15000,28000, df_star_distance_plot['distance_ly'].max() + 1]
    labels_distance = ['< 66 ly', '66 - 164 ly', '164 - 326 ly', '326 - 1630 ly', 
                       '1630 - 3260 ly', '3260 - 6520 ly', '6520-15000 ly','15000-28000','>28000']

    df_star_distance_plot['star_distance_category'] = pd.cut(df_star_distance_plot['distance_ly'], 
                                                            bins=bins_distance, 
                                                            labels=labels_distance, 
                                                            right=True, 
                                                            include_lowest=True)
    star_distance_counts = df_star_distance_plot['star_distance_category'].value_counts().reset_index()
    star_distance_counts.columns = ['star_distance_category', 'count']

    star_distance_counts['star_distance_category'] = pd.Categorical(
        star_distance_counts['star_distance_category'],
        categories=labels_distance,
        ordered=True
    )
    star_distance_counts = star_distance_counts.sort_values('star_distance_category')

    if not star_distance_counts.empty:
        fig_star_distance = px.bar(star_distance_counts, 
                                   x='count',
                                   y='star_distance_category',
                                   title="Distribuição da Distância das Estrelas Hospedeiras",
                                   labels={'star_distance_category': 'Distância (Anos-Luz)', 'count':'Número de Estrelas'}, 
                                   orientation='h',
                                   color='count', 
                                   color_continuous_scale=px.colors.sequential.Bluyl # Um esquema de cores
                                   )
        fig_star_distance.update_layout(yaxis={'categoryorder':'array', 'categoryarray':labels_distance}) 

        st.plotly_chart(fig_star_distance, use_container_width=True) 
        st.write(f"Total de **{len(df_star_distance_plot)}** Estrelas classificadas por sua distância.")
    else:
        st.warning("Não há dados de distância suficientes para classificar e gerar o gráfico.")





st.markdown("---") 
st.header("Visualização dos Dados")
st.dataframe(df2)        


