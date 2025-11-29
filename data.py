import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------
# CONFIGURAÇÃO DO STREAMLIT
# -----------------------
st.set_page_config(page_title="💻 Dashboard Interativo", layout="wide", page_icon="📊")
st.markdown(
    """
    <style>
    .main {background-color: #f5f5f5; padding: 2rem;}
    .stApp {color: #333333; font-family: 'Arial';}
    h1, h2, h3 {color: #1f2937;}
    .stButton>button {background-color:#1d4ed8; color:white; font-size:16px;}
    </style>
    """, unsafe_allow_html=True
)

st.title("📊 Dashboard Interativo de Excel/ Interactive Dashboard from Excel")
st.subheader("Transforme seus dados em gráficos em segundos!/ Transform your data into charts in seconds!")

# -----------------------
# UPLOAD DO ARQUIVO
# -----------------------
uploaded_file = st.file_uploader("📥 Escolha um arquivo Excel (.xls ou .xlsx)/ Choose an Excel file (.xls or .xlsx)", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Arquivo carregado com sucesso!/ File uploaded successfully!")
        st.dataframe(df)

        # -----------------------
        # SELEÇÃO DE COLUNAS
        # -----------------------
        st.sidebar.header("🔧 Opções de Análise/ Analysis Options")
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        all_cols = df.columns.tolist()

        # Seleção simples de colunas numéricas
        selected_cols = st.sidebar.multiselect("Escolha colunas para análise numérica. / Choose columns for numerical analysis.", numeric_cols)

        # -----------------------
        # ANÁLISE DE COLUNAS NUMÉRICAS
        # -----------------------
        if selected_cols:
            st.header("📈 Análise Individual de Colunas")
            for col in selected_cols:
                st.subheader(f"Coluna: {col} 🧮")
                st.write(f"**Total:** {df[col].sum()}")
                st.write(f"**Média/Average:** {df[col].mean():.2f}")
                st.write(f"**Mínimo/Minimun:** {df[col].min()}")
                st.write(f"**Máximo/Maximun:** {df[col].max()}")

                # Escolha do gráfico
                chart_type = st.selectbox(f"Escolha o gráfico para/ Choose the chart to {col}:", 
                                          ["Linha/Line", "Barras/Barrs", "Histograma/Histrogram", "Boxplot"], key=col)
                
                plt.figure(figsize=(8,4))
                if chart_type == "Linha/Line":
                    plt.plot(df[col], marker='o', color='#1d4ed8')
                    plt.ylabel(col)
                    plt.xlabel("Index")
                    plt.title(f"Gráfico de Linha/ Line Grafic - {col}")
                elif chart_type == "Barras/ Barrs":
                    plt.bar(df.index, df[col], color='#1d4ed8')
                    plt.ylabel(col)
                    plt.xlabel("Index")
                    plt.title(f"Gráfico de Barras/ Barrs Grafic - {col}")
                elif chart_type == "Histograma":
                    sns.histplot(df[col], kde=True, color='#1d4ed8')
                    plt.title(f"Histograma - {col}")
                elif chart_type == "Boxplot":
                    sns.boxplot(y=df[col], color='#1d4ed8')
                    plt.title(f"Boxplot - {col}")
                st.pyplot(plt)

        # -----------------------histogra
        # ANÁLISE CRUZADA
        # -----------------------
        st.header("🔄 Análise Cruzada/ Cross Analysis")
        st.write("Combine duas colunas para análise comparativa (ex: Idade x Gênero)./ Combine two columns for comparative analysis (e.g., Age x Gender).")

        col_x = st.selectbox("Selecione a coluna X/ Select column X", all_cols, key="cross_x")
        col_y = st.selectbox("Selecione a coluna Y/ Select column Y", all_cols, key="cross_y")
        
        if st.button("Gerar Gráfico Cruzado/Generate Cross Chart "):
            if col_x and col_y:
                plt.figure(figsize=(8,4))
                if pd.api.types.is_numeric_dtype(df[col_x]) and pd.api.types.is_numeric_dtype(df[col_y]):
                    sns.scatterplot(x=df[col_x], y=df[col_y], color="#1d4ed8", s=80)
                    plt.title(f"Scatter Plot: {col_x} x {col_y}")
                else:
                    cross_tab = pd.crosstab(df[col_x], df[col_y])
                    cross_tab.plot(kind='bar', stacked=True, figsize=(8,4), colormap='tab20')
                    plt.title(f"Gráfico de Barras Empilhadas/Stacked Bar Chart: {col_x} x {col_y}")
                    plt.ylabel(col_y)
                    plt.xlabel(col_x)
                st.pyplot(plt)

        # -----------------------
        # EXPORTAÇÃO
        # -----------------------
        st.sidebar.header("💾 Exportar Dados/ Export Data")
        export_format = st.sidebar.selectbox("Formato de exportação/ Export format", ["CSV", "Excel"])
        export_file_name = st.sidebar.text_input("Nome do arquivo/ Name of the file", "resultado/ result")

        if st.sidebar.button("Exportar/Export"):
            if export_format == "CSV":
                df.to_csv(f"{export_file_name}.csv", index=False)
                st.success(f"Arquivo/File {export_file_name}.csv exportado/exported!")
            else:
                df.to_excel(f"{export_file_name}.xlsx", index=False)
                st.success(f"Arquivo/ File {export_file_name}.xlsx exportado/exported!")

    except Exception as e:
        st.error(f"❌ Erro ao ler o arquivo/ Error reading file: {e}")
