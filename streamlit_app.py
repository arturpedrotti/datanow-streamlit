import streamlit as st

# Set up page
st.set_page_config(page_title="DataNow", page_icon="📊")

# Navigation Bar
st.title("DataNow")
st.markdown("**Visualização e Análise de Dados Simplificadas**")

# Add buttons for navigation
if st.button("Data Insights"):
    st.markdown("[Click here for Data Insights](http://127.0.0.1:8050)")
if st.button("Graph Builder"):
    st.markdown("[Click here for Graph Builder](http://127.0.0.1:8060)")

# About Section
st.header("Sobre o Projeto")
st.write("""
DataNow é uma aplicação web inovadora que une visualizações de dados interativas e insights profundos
para explorar métricas relacionadas ao combate à pobreza.
""")

st.subheader("✨ Funcionalidades Principais")
st.write("""
- 📊 **Gerador de gráficos interativos:** Criação de gráficos customizados em tempo real, com base em métricas selecionadas.
- 📈 **Dashboards dinâmicos:** Exploração de dados sobre pobreza, desigualdade e outras métricas socioeconômicas.
- 🌟 **Interface otimizada e moderna:** Com base no design minimalista, mas totalmente customizado para este projeto.
- 🔄 **Navegação intuitiva:** Conexões entre telas e visualizações para facilitar o uso e aprendizado.
- 🚀 **Em constante evolução:** Novas funcionalidades e melhorias sendo adicionadas regularmente.
""")

# Footer
st.markdown("---")
st.markdown("**Desenvolvido por Artur Pedrotti**")
st.markdown("[GitHub Repo](https://github.com/arturpedrotti/datanow) | [Contato](mailto:arturpedrotti@datanow.info)")
