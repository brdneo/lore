#!/usr/bin/env python3
"""
Dashboard Web - Lore N.A.
=========================

Interface web para visualização de agentes neurais e evolução.

Autor: Lore N.A. Genesis Team
Data: 27 de Junho de 2025
"""

import logging
import traceback
from typing import Optional, Any

# Configuração de logging robusto
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import networkx as nx
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(__file__))

from agent_dna import AgentDNA
from neural_web import NeuralWeb
from agent_name_generator import AgentNameGenerator
from population_manager import PopulationManager

st.set_page_config(
    page_title="Lore N.A. Dashboard",
    page_icon="🧬",
    layout="wide"
)

def generate_sample_population(size=20):
    """Gera população de exemplo para demonstração"""
    agents = []
    name_gen = AgentNameGenerator()
    
    for i in range(size):
        dna = AgentDNA.generate_random(f"demo_agent_{i:03d}")
        identity = name_gen.generate_identity(f"demo_agent_{i:03d}", "Demo Agent", dna.genes)
        
        agent_data = {
            'id': dna.agent_id,
            'name': identity.full_name,
            'nickname': identity.nickname,
            'personality': identity.personality_archetype,
            'origin': identity.origin,
            'generation': dna.generation,
            'fitness_overall': dna.fitness_scores['overall'],
            'fitness_limbo': dna.fitness_scores['limbo'],
            'fitness_odyssey': dna.fitness_scores['odyssey'],
            'fitness_ritual': dna.fitness_scores['ritual'],
            'fitness_engine': dna.fitness_scores['engine'],
            'fitness_logs': dna.fitness_scores['logs'],
            'created_at': datetime.now() - timedelta(days=np.random.randint(0, 30))
        }
        agents.append(agent_data)
    
    return pd.DataFrame(agents)

def plot_population_distribution(df):
    """Gráfico de distribuição da população"""
    fig = px.histogram(
        df, 
        x='fitness_overall', 
        nbins=20,
        title="Distribuição de Fitness da População",
        labels={'fitness_overall': 'Fitness Overall', 'count': 'Número de Agentes'}
    )
    fig.update_layout(showlegend=False)
    return fig

def plot_universe_radar(df):
    """Radar chart dos 5 universos"""
    avg_scores = {
        'Limbo': df['fitness_limbo'].mean(),
        'Odyssey': df['fitness_odyssey'].mean(),
        'Ritual': df['fitness_ritual'].mean(),
        'Engine': df['fitness_engine'].mean(),
        'Logs': df['fitness_logs'].mean()
    }
    
    categories = list(avg_scores.keys())
    values = list(avg_scores.values())
    
    # Fecha o radar
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Fitness Médio por Universo'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Performance Média nos 5 Universos"
    )
    
    return fig

def plot_neural_network(df):
    """Simula e visualiza rede neural"""
    # Cria grafo de exemplo baseado em compatibilidade simulada
    G = nx.Graph()
    
    # Adiciona nós
    for _, agent in df.iterrows():
        G.add_node(agent['id'], 
                   name=agent['nickname'],
                   fitness=agent['fitness_overall'])
    
    # Adiciona conexões baseadas em proximidade de fitness
    agents_list = df.to_dict('records')
    for i, agent1 in enumerate(agents_list):
        for agent2 in agents_list[i+1:i+6]:  # Conecta com próximos 5
            fitness_diff = abs(agent1['fitness_overall'] - agent2['fitness_overall'])
            if fitness_diff < 0.3:  # Threshold de compatibilidade
                G.add_edge(agent1['id'], agent2['id'], weight=1-fitness_diff)
    
    # Layout do grafo
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Prepara dados para plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        agent_data = df[df['id'] == node].iloc[0]
        node_text.append(f"{agent_data['nickname']}<br>Fitness: {agent_data['fitness_overall']:.2f}")
        node_color.append(agent_data['fitness_overall'])
    
    # Cria o plot
    fig = go.Figure()
    
    # Adiciona edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines',
        name='Conexões'
    ))
    
    # Adiciona nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            color=node_color,
            size=10,
            colorbar=dict(
                thickness=15,
                len=0.5,
                x=1.02,
                title="Fitness"
            ),
            line=dict(width=2)
        ),
        name='Agentes'
    ))
    
    fig.update_layout(
        title='Rede Social Neural',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        annotations=[ dict(
            text="Conexões baseadas em compatibilidade genética",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002,
            xanchor='left', yanchor='bottom',
            font=dict(color='gray', size=12)
        )],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig

def main():
    """Interface principal do dashboard"""
    
    st.title("🧬 Lore N.A. - Dashboard de Vida Artificial")
    st.markdown("*Sistema de agentes neurais com evolução darwiniana*")
    
    # Sidebar com controles
    st.sidebar.header("⚙️ Controles")
    
    # Gera ou carrega dados
    if st.sidebar.button("🔄 Gerar Nova População"):
        st.session_state.clear()
    
    population_size = st.sidebar.slider("Tamanho da População", 10, 50, 20)
    
    # Gera dados se não existir
    if 'population_df' not in st.session_state:
        with st.spinner("Gerando população de agentes..."):
            st.session_state.population_df = generate_sample_population(population_size)
    
    df = st.session_state.population_df
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Agentes", len(df))
    
    with col2:
        avg_fitness = df['fitness_overall'].mean()
        st.metric("Fitness Médio", f"{avg_fitness:.3f}")
    
    with col3:
        best_agent = df.loc[df['fitness_overall'].idxmax()]
        st.metric("Melhor Agente", str(best_agent['nickname']))  # type: ignore
    
    with col4:
        personalities = df['personality'].nunique()
        st.metric("Personalidades", personalities)
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs(["👥 População", "🌐 Rede Neural", "📊 Análises", "🧬 Agentes"])
    
    with tab1:
        st.header("Distribuição da População")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = plot_population_distribution(df)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = plot_universe_radar(df)
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.header("Rede Social Neural")
        fig3 = plot_neural_network(df)
        st.plotly_chart(fig3, use_container_width=True)
        
        st.info("💡 Os agentes se conectam baseado em compatibilidade genética. Nodes maiores = maior fitness.")
    
    with tab3:
        st.header("Análises Detalhadas")
        
        # Correlação entre universos
        corr_matrix = df[['fitness_limbo', 'fitness_odyssey', 'fitness_ritual', 'fitness_engine', 'fitness_logs']].corr()
        fig4 = px.imshow(corr_matrix, 
                        title="Correlação entre Universos",
                        color_continuous_scale='RdBu_r')
        st.plotly_chart(fig4, use_container_width=True)
        
        # Timeline de criação
        fig5 = px.scatter(df, x='created_at', y='fitness_overall', 
                         color='personality',
                         title="Evolução Temporal do Fitness",
                         hover_data=['name'])
        st.plotly_chart(fig5, use_container_width=True)
    
    with tab4:
        st.header("Lista de Agentes")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            personality_filter = st.selectbox(
                "Filtrar por Personalidade:",
                ["Todos"] + sorted(df['personality'].unique().tolist())
            )
        
        with col2:
            min_fitness = st.slider("Fitness Mínimo:", 0.0, 1.0, 0.0)
        
        # Aplica filtros
        filtered_df = df.copy()
        if personality_filter != "Todos":
            filtered_df = filtered_df[filtered_df['personality'] == personality_filter]
        filtered_df = filtered_df[filtered_df['fitness_overall'] >= min_fitness]
        
        # Tabela de agentes
        st.dataframe(
            filtered_df[['name', 'nickname', 'personality', 'origin', 'fitness_overall']].sort_values('fitness_overall', ascending=False),
            use_container_width=True
        )
        
        # Detalhes do agente selecionado
        if not filtered_df.empty:
            selected_agent = st.selectbox(
                "Ver detalhes do agente:",
                filtered_df['name'].tolist()
            )
            
            agent_details = filtered_df[filtered_df['name'] == selected_agent].iloc[0]
            
            st.subheader(f"🎭 {agent_details['name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Nickname:** {agent_details['nickname']}")
                st.write(f"**Personalidade:** {agent_details['personality']}")
                st.write(f"**Origem:** {agent_details['origin']}")
                st.write(f"**Geração:** {agent_details['generation']}")
            
            with col2:
                st.write("**Fitness por Universo:**")
                for universe in ['limbo', 'odyssey', 'ritual', 'engine', 'logs']:
                    score = agent_details[f'fitness_{universe}']
                    st.progress(score, text=f"{universe.title()}: {score:.3f}")

if __name__ == "__main__":
    main()
