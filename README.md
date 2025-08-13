# 🪐 Análise e Dashboard Interativo de Exoplanetas catalogados

## 🚀 Visão Geral do Projeto

Este projeto é um dashboard interativo construído com **Streamlit** para explorar e visualizar dados de exoplanetas. Utilizando bibliotecas de análise de dados como Pandas e Plotly, este aplicativo oferece alguns insights sobre:

- Os métodos de descoberta mais comuns.
- A distribuição de massa e raio dos planetas.
- O potencial de habitabilidade dos exoplanetas.
- As características das estrelas hospedeiras, como tipo evolutivo e idade.

O objetivo é transformar um conjunto de dados brutos em uma narrativa visual e interativa.

## ✨ Destaques e Funcionalidades

- **Dashboard Interativo:** Navegue e explore os dados de exoplanetas através de uma interface web intuitiva.
- **Limpeza e Engenharia de Features:** Dados brutos foram processados para criar novas categorias e métricas relevantes (ex: "Tipo de Planeta", "Status da Zona Habitável").
- **Visualizações Dinâmicas:** Gráficos interativos criados com Plotly que permitem filtrar, dar zoom e explorar os dados com detalhes.
- **Análise por Categorias:** Classificação de planetas por massa e de estrelas por idade e tipo evolutivo.

## 🔗 Demonstração 

Você pode acessar a versão hospedada do dashboard aqui:
https://exoplanetas-nasa-dashboard.streamlit.app/ 

## 🛠️ Tecnologias e Bibliotecas

O projeto foi desenvolvido em Python e utiliza as seguintes bibliotecas:

- `streamlit`: Para criar o dashboard interativo.
- `pandas`: Para a manipulação e análise dos dados.
- `plotly.express`: Para a criação de gráficos interativos e asthetic.
- `numpy`: Para cálculos numéricos.
- `re`: Para expressões regulares (usado pra classificação de estrelas).

## 📊 Fonte de Dados

O dataset utilizado neste projeto é o **"Exoplanets - We are Not Alone!"**, disponível no Kaggle. Ele é uma compilação de dados sobre exoplanetas confirmados, incluindo informações sobre os planetas e suas estrelas hospedeiras.

- **Link do Dataset:** https://www.kaggle.com/datasets/akashbommidi/exoplanets-dataset

## 📈 Metodologia e Análise

1.  **Limpeza de Dados:** Remoção de colunas com alta porcentagem de valores ausentes e tratamento de `NaNs` para garantir a integridade dos dados para cada visualização.
2.  **Engenharia de Features:** Criação de novas colunas-chave:
    - **`planet_type`:** Classifiquei planetas em categorias como "Sub-Terra", "Gigante Gasoso" e "Anã Marrom", baseada na massa.
    - **`habitable_zone_status`:** Determinação se o planeta está dentro da zona habitável de sua estrela, usando a temperatura estelar e a distância orbital.
    - **`star_evolutionary_type`:** Classificação da estrela hospedeira em tipos como "Anã" ou "Gigante Vermelha" com base em seu tipo espectral.
    - **`distance_ly` e `distance_parsec`:** Conversão de distâncias estelares de parsecs para ano-luz.
3.  **Visualização e Insights:** Desenvolvimento de gráficos de barras, histogramas e gráficos de pizza para explorar a distribuição de cada nova categoria criada, revelando padrões e tendências.

## 💡 Insights Chave

- **Métodos de Descoberta:** O gráfico de métodos de descoberta mostra que o método de **Velocidade Radial** foi historicamente dominante, mas o de **Trânsito** o superou em número de descobertas.
- **Tipos de Planetas:** A maioria dos planetas classificados são **gigantes gasosos**, seguidos por **super-terras/mini-netunos**.
- **Zona Habitável:** Uma pequena, mas significativa, quantidade de planetas está dentro da zona habitável de suas estrelas, levantando questões sobre seu potencial de abrigar vida.
- **Idade das Estrelas:** A maioria das estrelas hospedeiras são de **idade média**, com idades entre 1 e 10 bilhões de anos, similar ao nosso Sol.

## 🔧 Como Executar Localmente

Se vc quiser rodar este projeto em sua própria máquina, siga esses passos:
1.  Clone este repositório:
    ```bash
    git clone [https://github.com/Belisarius-42/ExoPlanetas---NASA.git](https://github.com/Belisarius-42/ExoPlanetas---NASA.git)
    cd ExoPlanetas---NASA
    ```
2.  Instale as bibliotecas necessárias.Recomendável usar um ambiente virtual (venv):
    ```bash
    pip install -r requirements.txt
    ```
3.  Execute o aplicativo Streamlit:
    ```bash
    streamlit run app.py
    ```

Saudações
-Bruno Henrique
    

O aplicativo será aberto automaticamente no seu navegador.

---
