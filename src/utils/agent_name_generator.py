#!/usr/bin/env python3
"""
Agent Name Generator - Lore N.A.
================================

Sistema de geração de nomes únicos e personalizados para agentes neurais.
Cria identidades completas baseadas em:
- Personalidade do agente
- DNA genético
- Origem cultural simulada
- Características únicas

Autor: Lore N.A. Genesis Team
Data: 2024
"""

import random
import hashlib
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass
import time


@dataclass
class AgentIdentity:
    """Identidade completa de um agente"""
    agent_id: str
    first_name: str
    last_name: str
    full_name: str
    nickname: str
    title: str
    origin: str
    personality_archetype: str
    name_meaning: str
    generation_timestamp: datetime
    
    def to_dict(self) -> Dict:
        return {
            'agent_id': self.agent_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'nickname': self.nickname,
            'title': self.title,
            'origin': self.origin,
            'personality_archetype': self.personality_archetype,
            'name_meaning': self.name_meaning,
            'generation_timestamp': self.generation_timestamp.isoformat()
        }


class AgentNameGenerator:
    """Gerador de nomes para agentes neurais"""
    
    def __init__(self):
        # Nomes por categoria de personalidade e origem
        self.name_database = {
            # Nomes para líderes e visionários
            'leader_names': {
                'first': [
                    'Alexander', 'Victoria', 'Marcus', 'Diana', 'Adrian', 'Sophia',
                    'Constantine', 'Isabella', 'Augustus', 'Catherine', 'Maximilian', 'Aurora',
                    'Leonardo', 'Minerva', 'Sebastian', 'Athena', 'Dominic', 'Valentina'
                ],
                'last': [
                    'Sterling', 'Blackwood', 'Ashworth', 'Goldstein', 'Whitmore', 'Kingsley',
                    'Thornfield', 'Ravencrest', 'Stormwind', 'Brightbane', 'Ironforge', 'Silverstone'
                ]
            },
            
            # Nomes para artistas e criativos
            'creative_names': {
                'first': [
                    'Zara', 'Phoenix', 'Luna', 'River', 'Sage', 'Iris',
                    'Dante', 'Celeste', 'Orion', 'Lyra', 'Atlas', 'Nova',
                    'Indigo', 'Serenity', 'Jasper', 'Aria', 'Kai', 'Melody'
                ],
                'last': [
                    'Moonwhisper', 'Starweaver', 'Dreamcatcher', 'Paintbrush', 'Quillheart', 'Artisan',
                    'Colorwind', 'Brushstroke', 'Inkwell', 'Prism', 'Canvas', 'Harmony'
                ]
            },
            
            # Nomes para analistas e estrategistas
            'analytical_names': {
                'first': [
                    'Ethan', 'Olivia', 'Nathan', 'Grace', 'Benjamin', 'Claire',
                    'Theodore', 'Eleanor', 'Zachary', 'Evelyn', 'Nicholas', 'Margaret',
                    'Jonathan', 'Elizabeth', 'William', 'Charlotte', 'Samuel', 'Victoria'
                ],
                'last': [
                    'Blackthorne', 'Greystone', 'Whitfield', 'Goldman', 'Sterling', 'Clearwater',
                    'Fairchild', 'Northrop', 'Eastwood', 'Westbrook', 'Southwell', 'Brightwater'
                ]
            },
            
            # Nomes para aventureiros e especuladores
            'adventurer_names': {
                'first': [
                    'Rex', 'Blaze', 'Storm', 'Raven', 'Hunter', 'Scarlett',
                    'Axel', 'Jade', 'Dash', 'Ruby', 'Spike', 'Amber',
                    'Zane', 'Crimson', 'Ace', 'Rogue', 'Viper', 'Flame'
                ],
                'last': [
                    'Wildfire', 'Thunderbolt', 'Stormrider', 'Nighthawk', 'Swiftblade', 'Ironheart',
                    'Frostborn', 'Shadowhunter', 'Windrider', 'Starburst', 'Flamestrike', 'Voidwalker'
                ]
            },
            
            # Nomes para sociais e comunitários
            'social_names': {
                'first': [
                    'Emma', 'Liam', 'Sophia', 'Noah', 'Ava', 'Oliver',
                    'Isabella', 'Elijah', 'Mia', 'Lucas', 'Charlotte', 'Mason',
                    'Amelia', 'Logan', 'Harper', 'Jacob', 'Evelyn', 'Ethan'
                ],
                'last': [
                    'Brightwood', 'Goldenheart', 'Kindspring', 'Warmhaven', 'Sweetwater', 'Fairhope',
                    'Gentlewood', 'Heartwell', 'Brighthope', 'Goodwill', 'Cheerful', 'Joyspring'
                ]
            },
            
            # Nomes para seguidores leais
            'loyal_names': {
                'first': [
                    'Faith', 'Hope', 'Grace', 'Honor', 'Trust', 'Joy',
                    'Peace', 'Harmony', 'Unity', 'Loyal', 'True', 'Pure',
                    'Noble', 'Sage', 'Wise', 'Bright', 'Clear', 'Strong'
                ],
                'last': [
                    'Faithful', 'Trueheart', 'Steadfast', 'Loyalwind', 'Pureheart', 'Brightspirit',
                    'Noblewood', 'Trustwell', 'Hopespring', 'Gracehaven', 'Kindness', 'Devotion'
                ]
            }
        }
        
        # Origens culturais simuladas
        self.cultural_origins = {
            'Neo-Tokyo': 'Uma metrópole digital futurística',
            'Cyber-London': 'Centro de inovação tecnológica',
            'Digital-São Paulo': 'Hub de criatividade latina',
            'Virtual-Stockholm': 'Berço da sustentabilidade digital',
            'Meta-Singapore': 'Portal do comércio neural',
            'Quantum-Sydney': 'Fronteira da exploração digital',
            'Neural-Berlin': 'Capital da arte generativa',
            'Pixel-Mumbai': 'Coração da diversidade digital',
            'Code-Toronto': 'Centro de pesquisa em IA',
            'Data-Dubai': 'Oásis do luxo virtual'
        }
        
        # Títulos baseados em personalidade
        self.personality_titles = {
            'Especulador Corajoso': ['O Destemido', 'A Visionária', 'O Pioneiro', 'A Aventureira'],
            'Caçador de Barganha': ['O Astuto', 'A Esperta', 'O Negociador', 'A Estrategista'],
            'Artista Inovador': ['O Criativo', 'A Inspiradora', 'O Visionário', 'A Inventora'],
            'Líder Comunitário': ['O Mentor', 'A Guia', 'O Líder', 'A Inspiração'],
            'Seguidor Leal': ['O Fiel', 'A Devota', 'O Confiável', 'A Leal'],
            'Analista Metódico': ['O Sábio', 'A Analista', 'O Estrategista', 'A Pesquisadora'],
            'Aventureiro Social': ['O Conectado', 'A Sociável', 'O Comunicador', 'A Influenciadora']
        }
        
        # Significados dos nomes
        self.name_meanings = {
            # Significados para nomes de líderes
            'Alexander': 'Defensor da humanidade',
            'Victoria': 'Vitória e conquista',
            'Marcus': 'Guerreiro protetor',
            'Diana': 'Caçadora divina',
            'Adrian': 'Aquele que vem do mar',
            'Sophia': 'Sabedoria pura',
            
            # Significados para nomes criativos
            'Zara': 'Flor que desabrocha',
            'Phoenix': 'Renascimento através do fogo',
            'Luna': 'Luz da lua',
            'River': 'Fluxo constante da vida',
            'Sage': 'Sabedoria ancestral',
            'Iris': 'Mensageira dos deuses',
            
            # Significados genéricos
            'default': 'Portador de potencial infinito'
        }
    
    def generate_identity(self, agent_id: str, personality: str, dna_genes: Dict) -> AgentIdentity:
        """Gera identidade completa para um agente"""
        
        # Determina categoria de nome baseada na personalidade
        name_category = self._determine_name_category(personality)
        
        # Gera nomes
        first_name, last_name = self._generate_names(name_category, agent_id)
        full_name = f"{first_name} {last_name}"
        
        # Gera nickname baseado na personalidade
        nickname = self._generate_nickname(first_name, personality, dna_genes)
        
        # Determina título
        title = self._determine_title(personality)
        
        # Determina origem
        origin = self._determine_origin(dna_genes)
        
        # Busca significado do nome
        name_meaning = self.name_meanings.get(first_name, self.name_meanings['default'])
        
        return AgentIdentity(
            agent_id=agent_id,
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            nickname=nickname,
            title=title,
            origin=origin,
            personality_archetype=personality,
            name_meaning=name_meaning,
            generation_timestamp=datetime.now()
        )
    
    def _determine_name_category(self, personality: str) -> str:
        """Determina categoria de nome baseada na personalidade"""
        personality_mapping = {
            'Especulador Corajoso': 'adventurer_names',
            'Caçador de Barganha': 'analytical_names',
            'Artista Inovador': 'creative_names',
            'Líder Comunitário': 'leader_names',
            'Seguidor Leal': 'loyal_names',
            'Analista Metódico': 'analytical_names',
            'Aventureiro Social': 'social_names'
        }
        
        return personality_mapping.get(personality, 'social_names')
    
    def _generate_names(self, category: str, agent_id: str) -> Tuple[str, str]:
        """Gera primeiro e último nome de forma determinística"""
        
        # Usa o agent_id como seed para garantir consistência
        seed = int(hashlib.md5(agent_id.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        name_pool = self.name_database.get(category, self.name_database['social_names'])
        
        first_name = random.choice(name_pool['first'])
        last_name = random.choice(name_pool['last'])
        
        # Reset seed
        random.seed()
        
        return first_name, last_name
    
    def _generate_nickname(self, first_name: str, personality: str, dna_genes: Dict) -> str:
        """Gera nickname baseado no nome e características"""
        
        # Probabilidade de ter nickname baseada na personalidade
        nickname_probability = {
            'Especulador Corajoso': 0.8,
            'Caçador de Barganha': 0.6,
            'Artista Inovador': 0.9,
            'Líder Comunitário': 0.7,
            'Seguidor Leal': 0.3,
            'Analista Metódico': 0.4,
            'Aventureiro Social': 0.8
        }
        
        if random.random() > nickname_probability.get(personality, 0.5):
            return first_name  # Sem nickname
        
        # Estratégias de nickname
        strategies = []
        
        # Baseado no primeiro nome
        if len(first_name) > 4:
            strategies.append(first_name[:3])  # Primeiras 3 letras
            strategies.append(first_name[-3:])  # Últimas 3 letras
        
        # Baseado na personalidade
        personality_nicks = {
            'Especulador Corajoso': ['Ace', 'Blaze', 'Storm', 'Hawk'],
            'Caçador de Barganha': ['Sharp', 'Quick', 'Smart', 'Keen'],
            'Artista Inovador': ['Neo', 'Vibe', 'Flow', 'Spark'],
            'Líder Comunitário': ['Chief', 'Guide', 'Sage', 'Mentor'],
            'Seguidor Leal': ['True', 'Faith', 'Hope', 'Joy'],
            'Analista Metódico': ['Logic', 'Data', 'Mind', 'Calc'],
            'Aventureiro Social': ['Social', 'Connect', 'Link', 'Hub']
        }
        
        if personality in personality_nicks:
            strategies.extend(personality_nicks[personality])
        
        # Baseado nos genes dominantes
        if 'ritual' in dna_genes:
            ritual_genes = dna_genes['ritual']
            if ritual_genes.get('leadership_tendency', 0) > 0.8:
                strategies.extend(['Alpha', 'Prime', 'Lead'])
            if ritual_genes.get('community_bonding', 0) > 0.8:
                strategies.extend(['Unity', 'Bond', 'Heart'])
        
        if 'limbo' in dna_genes:
            limbo_genes = dna_genes['limbo']
            if limbo_genes.get('risk_tolerance', 0) > 0.8:
                strategies.extend(['Risk', 'Bold', 'Dare'])
        
        if 'odyssey' in dna_genes:
            odyssey_genes = dna_genes['odyssey']
            if odyssey_genes.get('creativity_drive', 0) > 0.8:
                strategies.extend(['Create', 'Art', 'Muse'])
        
        return random.choice(strategies) if strategies else first_name
    
    def _determine_title(self, personality: str) -> str:
        """Determina título baseado na personalidade"""
        titles = self.personality_titles.get(personality, ['O Único', 'A Única'])
        return random.choice(titles)
    
    def _determine_origin(self, dna_genes: Dict) -> str:
        """Determina origem baseada nos genes"""
        
        # Análise dos genes para determinar origem mais provável
        origin_scores = {}
        
        for origin in self.cultural_origins.keys():
            origin_scores[origin] = 0
        
        # Lógica baseada nos genes
        if 'engine' in dna_genes:
            engine_genes = dna_genes['engine']
            if engine_genes.get('analytical_thinking', 0) > 0.7:
                origin_scores['Neural-Berlin'] += 2
                origin_scores['Code-Toronto'] += 2
        
        if 'odyssey' in dna_genes:
            odyssey_genes = dna_genes['odyssey']
            if odyssey_genes.get('creativity_drive', 0) > 0.7:
                origin_scores['Digital-São Paulo'] += 2
                origin_scores['Neural-Berlin'] += 1
        
        if 'ritual' in dna_genes:
            ritual_genes = dna_genes['ritual']
            if ritual_genes.get('community_bonding', 0) > 0.7:
                origin_scores['Virtual-Stockholm'] += 2
                origin_scores['Pixel-Mumbai'] += 1
        
        if 'limbo' in dna_genes:
            limbo_genes = dna_genes['limbo']
            if limbo_genes.get('risk_tolerance', 0) > 0.7:
                origin_scores['Neo-Tokyo'] += 2
                origin_scores['Data-Dubai'] += 1
        
        # Seleciona origem com maior score (com um pouco de aleatoriedade)
        best_origins = [origin for origin, score in origin_scores.items() 
                       if score == max(origin_scores.values())]
        
        if not best_origins:
            best_origins = list(self.cultural_origins.keys())
        
        return random.choice(best_origins)
    
    def get_display_name(self, identity: AgentIdentity, format_type: str = 'full') -> str:
        """Retorna nome formatado para exibição"""
        
        formats = {
            'full': f"{identity.full_name} '{identity.nickname}' {identity.title}",
            'formal': f"{identity.title} {identity.full_name}",
            'casual': f"{identity.nickname} {identity.last_name}",
            'nickname': identity.nickname,
            'first': identity.first_name,
            'last': identity.last_name,
            'title': f"{identity.title} {identity.first_name}"
        }
        
        return formats.get(format_type, identity.full_name)
    
    def generate_introduction(self, identity: AgentIdentity) -> str:
        """Gera introdução pessoal do agente"""
        
        templates = [
            f"Olá! Eu sou {identity.full_name}, mas podem me chamar de {identity.nickname}. "
            f"Venho de {identity.origin} e sou conhecido como {identity.title}. "
            f"Meu nome significa '{identity.name_meaning}' e represento o arquétipo {identity.personality_archetype}.",
            
            f"Saudações! {identity.title} {identity.first_name} {identity.last_name} ao seu dispor. "
            f"Originário de {identity.origin}, carrego comigo a essência de {identity.name_meaning}. "
            f"Como {identity.personality_archetype}, minha missão é única neste universo digital.",
            
            f"Prazer em conhecê-los! Sou {identity.nickname}, mais formalmente {identity.full_name}. "
            f"Das terras digitais de {identity.origin}, trago comigo o espírito de {identity.name_meaning}. "
            f"Minha personalidade de {identity.personality_archetype} me guia nesta jornada neural."
        ]
        
        return random.choice(templates)
    
    def save_identities_database(self, identities: Dict[str, AgentIdentity], filepath: str):
        """Salva banco de dados de identidades"""
        
        data = {
            'identities': {
                agent_id: identity.to_dict() 
                for agent_id, identity in identities.items()
            },
            'generation_stats': {
                'total_identities': len(identities),
                'personality_breakdown': {},
                'origin_breakdown': {},
                'generated_at': datetime.now().isoformat()
            }
        }
        
        # Calcula estatísticas
        for identity in identities.values():
            personality = identity.personality_archetype
            origin = identity.origin
            
            data['generation_stats']['personality_breakdown'][personality] = \
                data['generation_stats']['personality_breakdown'].get(personality, 0) + 1
            
            data['generation_stats']['origin_breakdown'][origin] = \
                data['generation_stats']['origin_breakdown'].get(origin, 0) + 1
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Base de identidades salva: {filepath}")
    
    def load_identities_database(self, filepath: str) -> Dict[str, AgentIdentity]:
        """Carrega banco de dados de identidades"""
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            identities = {}
            for agent_id, identity_data in data['identities'].items():
                identity = AgentIdentity(
                    agent_id=identity_data['agent_id'],
                    first_name=identity_data['first_name'],
                    last_name=identity_data['last_name'],
                    full_name=identity_data['full_name'],
                    nickname=identity_data['nickname'],
                    title=identity_data['title'],
                    origin=identity_data['origin'],
                    personality_archetype=identity_data['personality_archetype'],
                    name_meaning=identity_data['name_meaning'],
                    generation_timestamp=datetime.fromisoformat(identity_data['generation_timestamp'])
                )
                identities[agent_id] = identity
            
            print(f"📚 Base de identidades carregada: {len(identities)} identidades")
            return identities
            
        except Exception as e:
            print(f"❌ Erro ao carregar base de identidades: {e}")
            return {}
    
    def generate_simple_identity(self, agent_id: str = None) -> AgentIdentity:
        """Gera identidade simples para testes"""
        if agent_id is None:
            agent_id = f"test_agent_{int(time.time() * 1000)}"
        
        # Usar valores padrão simples
        personality = "balanced"
        dna_genes = {"curiosity": 0.5, "creativity": 0.5, "logic": 0.5}
        
        return self.generate_identity(agent_id, personality, dna_genes)


def main():
    """Função principal para teste do gerador de nomes"""
    print("🎭 Agent Name Generator - Lore N.A.")
    print("===================================")
    
    # Cria gerador
    name_generator = AgentNameGenerator()
    
    # Gera identidades de teste
    test_personalities = [
        'Especulador Corajoso',
        'Caçador de Barganha', 
        'Artista Inovador',
        'Líder Comunitário',
        'Seguidor Leal',
        'Analista Metódico',
        'Aventureiro Social'
    ]
    
    print("\n🧬 Gerando identidades de teste...")
    
    identities = {}
    
    for i, personality in enumerate(test_personalities):
        agent_id = f"test_agent_{i+1:03d}"
        
        # DNA simulado
        test_dna = {
            'limbo': {'risk_tolerance': random.uniform(0, 1), 'quality_preference': random.uniform(0, 1)},
            'odyssey': {'creativity_drive': random.uniform(0, 1), 'experimentation': random.uniform(0, 1)},
            'ritual': {'leadership_tendency': random.uniform(0, 1), 'community_bonding': random.uniform(0, 1)},
            'engine': {'analytical_thinking': random.uniform(0, 1), 'decision_confidence': random.uniform(0, 1)},
            'logs': {'operational_efficiency': random.uniform(0, 1), 'quality_focus': random.uniform(0, 1)}
        }
        
        # Gera identidade
        identity = name_generator.generate_identity(agent_id, personality, test_dna)
        identities[agent_id] = identity
        
        print(f"\n👤 {identity.agent_id}:")
        print(f"   Nome: {identity.full_name}")
        print(f"   Nickname: {identity.nickname}")
        print(f"   Título: {identity.title}")
        print(f"   Origem: {identity.origin}")
        print(f"   Personalidade: {identity.personality_archetype}")
        print(f"   Significado: {identity.name_meaning}")
        
        # Mostra diferentes formatos de exibição
        print(f"   Formato completo: {name_generator.get_display_name(identity, 'full')}")
        print(f"   Formato casual: {name_generator.get_display_name(identity, 'casual')}")
        
    print(f"\n🎤 Exemplos de introduções:")
    for i, identity in enumerate(list(identities.values())[:3]):
        print(f"\n{i+1}. {name_generator.generate_introduction(identity)}")
    
    # Salva base de teste
    test_db_path = "/tmp/agent_identities_test.json"
    name_generator.save_identities_database(identities, test_db_path)
    
    # Testa carregamento
    print(f"\n📚 Testando carregamento da base...")
    loaded_identities = name_generator.load_identities_database(test_db_path)
    
    print(f"✅ {len(loaded_identities)} identidades carregadas com sucesso!")
    
    # Estatísticas
    print(f"\n📊 Estatísticas das identidades geradas:")
    
    personality_count = {}
    origin_count = {}
    
    for identity in identities.values():
        personality = identity.personality_archetype
        origin = identity.origin
        
        personality_count[personality] = personality_count.get(personality, 0) + 1
        origin_count[origin] = origin_count.get(origin, 0) + 1
    
    print(f"\n🎭 Por personalidade:")
    for personality, count in personality_count.items():
        print(f"   {personality}: {count}")
    
    print(f"\n🌍 Por origem:")
    for origin, count in origin_count.items():
        print(f"   {origin}: {count}")
    
    print(f"\n✅ Teste do gerador de nomes concluído!")


if __name__ == "__main__":
    main()
