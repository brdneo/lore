#!/usr/bin/env python3
"""
Agent Name Generator - Lore N.A.
================================

Unique and personalized name generation system for neural agents.
Creates complete identities based on:
- Agent personality
- Genetic DNA
- Simulated cultural origin
- Unique characteristics

Author: Lore N.A. Genesis Team
Date: 2024
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
    """Complete identity of an agent"""
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
    """Name generator for neural agents"""

    def __init__(self):
        # Names by personality category and origin
        self.name_database = {
            # Names for leaders and visionaries
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

            # Names for artists and creatives
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

            # Names for analysts and strategists
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

            # Names for adventurers and speculators
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

            # Names for social and community-oriented
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

            # Names for loyal followers
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

        # Simulated cultural origins
        self.cultural_origins = {
            'Neo-Tokyo': 'A futuristic digital metropolis',
            'Cyber-London': 'Center of technological innovation',
            'Digital-São Paulo': 'Hub of Latin creativity',
            'Virtual-Stockholm': 'Birthplace of digital sustainability',
            'Meta-Singapore': 'Gateway to neural commerce',
            'Quantum-Sydney': 'Frontier of digital exploration',
            'Neural-Berlin': 'Capital of generative art',
            'Pixel-Mumbai': 'Heart of digital diversity',
            'Code-Toronto': 'AI research center',
            'Data-Dubai': 'Oasis of virtual luxury'
        }

        # Titles based on personality
        self.personality_titles = {
            'Brave Speculator': ['The Fearless', 'The Visionary', 'The Pioneer', 'The Adventurer'],
            'Bargain Hunter': ['The Astute', 'The Smart', 'The Negotiator', 'The Strategist'],
            'Innovative Artist': ['The Creative', 'The Inspiring', 'The Visionary', 'The Inventor'],
            'Community Leader': ['The Mentor', 'The Guide', 'The Leader', 'The Inspiration'],
            'Loyal Follower': ['The Faithful', 'The Devoted', 'The Reliable', 'The Loyal'],
            'Methodical Analyst': ['The Wise', 'The Analyst', 'The Strategist', 'The Researcher'],
            'Social Adventurer': ['The Connected', 'The Sociable', 'The Communicator', 'The Influencer']
        }

        # Name meanings
        self.name_meanings = {
            # Leader name meanings
            'Alexander': 'Defender of humanity',
            'Victoria': 'Victory and conquest',
            'Marcus': 'Warrior protector',
            'Diana': 'Divine huntress',
            'Adrian': 'One who comes from the sea',
            'Sophia': 'Pure wisdom',

            # Creative name meanings
            'Zara': 'Blooming flower',
            'Phoenix': 'Rebirth through fire',
            'Luna': 'Light of the moon',
            'River': 'Constant flow of life',
            'Sage': 'Ancestral wisdom',
            'Iris': 'Messenger of the gods',

            # Generic meanings
            'default': 'Bearer of infinite potential'
        }

    def generate_identity(self, agent_id: str, personality: str, dna_genes: Dict) -> AgentIdentity:
        """Generate complete identity for an agent"""

        # Determine name category based on personality
        name_category = self._determine_name_category(personality)

        # Generate names
        first_name, last_name = self._generate_names(name_category, agent_id)
        full_name = f"{first_name} {last_name}"

        # Generate nickname based on personality
        nickname = self._generate_nickname(first_name, personality, dna_genes)

        # Determine title
        title = self._determine_title(personality)

        # Determine origin
        origin = self._determine_origin(dna_genes)

        # Find name meaning
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
        """Determine name category based on personality"""
        personality_mapping = {
            'Brave Speculator': 'adventurer_names',
            'Bargain Hunter': 'analytical_names',
            'Innovative Artist': 'creative_names',
            'Community Leader': 'leader_names',
            'Loyal Follower': 'loyal_names',
            'Methodical Analyst': 'analytical_names',
            'Social Adventurer': 'social_names'
        }

        return personality_mapping.get(personality, 'social_names')

    def _generate_names(self, category: str, agent_id: str) -> Tuple[str, str]:
        """Generate first and last name deterministically"""

        # Use agent_id as seed to ensure consistency
        seed = int(hashlib.md5(agent_id.encode()).hexdigest()[:8], 16)
        random.seed(seed)

        name_pool = self.name_database.get(category, self.name_database['social_names'])

        first_name = random.choice(name_pool['first'])
        last_name = random.choice(name_pool['last'])

        # Reset seed
        random.seed()

        return first_name, last_name

    def _generate_nickname(self, first_name: str, personality: str, dna_genes: Dict) -> str:
        """Generate nickname based on name and characteristics"""

        # Probability of having nickname based on personality
        nickname_probability = {
            'Brave Speculator': 0.8,
            'Bargain Hunter': 0.6,
            'Innovative Artist': 0.9,
            'Community Leader': 0.7,
            'Loyal Follower': 0.3,
            'Methodical Analyst': 0.4,
            'Social Adventurer': 0.8
        }

        if random.random() > nickname_probability.get(personality, 0.5):
            return first_name  # No nickname

        # Nickname strategies
        strategies = []

        # Based on first name
        if len(first_name) > 4:
            strategies.append(first_name[:3])  # First 3 letters
            strategies.append(first_name[-3:])  # Last 3 letters

        # Based on personality
        personality_nicks = {
            'Brave Speculator': ['Ace', 'Blaze', 'Storm', 'Hawk'],
            'Bargain Hunter': ['Sharp', 'Quick', 'Smart', 'Keen'],
            'Innovative Artist': ['Neo', 'Vibe', 'Flow', 'Spark'],
            'Community Leader': ['Chie', 'Guide', 'Sage', 'Mentor'],
            'Loyal Follower': ['True', 'Faith', 'Hope', 'Joy'],
            'Methodical Analyst': ['Logic', 'Data', 'Mind', 'Calc'],
            'Social Adventurer': ['Social', 'Connect', 'Link', 'Hub']
        }

        if personality in personality_nicks:
            strategies.extend(personality_nicks[personality])

        # Based on dominant genes
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
        """Determine title based on personality"""
        titles = self.personality_titles.get(personality, ['The Unique'])
        return random.choice(titles)

    def _determine_origin(self, dna_genes: Dict) -> str:
        """Determine origin based on genes"""

        # Gene analysis to determine most likely origin
        origin_scores = {}

        for origin in self.cultural_origins.keys():
            origin_scores[origin] = 0

        # Logic based on genes
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

        # Select origin with highest score (with some randomness)
        best_origins = [origin for origin, score in origin_scores.items()
                        if score == max(origin_scores.values())]

        if not best_origins:
            best_origins = list(self.cultural_origins.keys())

        return random.choice(best_origins)

    def get_display_name(self, identity: AgentIdentity, format_type: str = 'full') -> str:
        """Return formatted name for display"""

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
        """Generate personal introduction for the agent"""

        templates = [
            f"Hello! I am {identity.full_name}, but you can call me {identity.nickname}. "
            f"I come from {identity.origin} and am known as {identity.title}. "
            f"My name means '{identity.name_meaning}' and I represent the {identity.personality_archetype} archetype.",

            f"Greetings! {identity.title} {identity.first_name} {identity.last_name} at your service. "
            f"Originally from {identity.origin}, I carry with me the essence of {identity.name_meaning}. "
            f"As a {identity.personality_archetype}, my mission is unique in this digital universe.",

            f"Pleasure to meet you! I'm {identity.nickname}, more formally {identity.full_name}. "
            f"From the digital lands of {identity.origin}, I bring with me the spirit of {identity.name_meaning}. "
            f"My {identity.personality_archetype} personality guides me on this neural journey."
        ]

        return random.choice(templates)

    def save_identities_database(self, identities: Dict[str, AgentIdentity], filepath: str):
        """Save identities database"""

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

        # Calculate statistics
        for identity in identities.values():
            personality = identity.personality_archetype
            origin = identity.origin

            data['generation_stats']['personality_breakdown'][personality] = \
                data['generation_stats']['personality_breakdown'].get(personality, 0) + 1

            data['generation_stats']['origin_breakdown'][origin] = \
                data['generation_stats']['origin_breakdown'].get(origin, 0) + 1

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"💾 Identity database saved: {filepath}")

    def load_identities_database(self, filepath: str) -> Dict[str, AgentIdentity]:
        """Load identities database"""

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

            print(f"📚 Identity database loaded: {len(identities)} identities")
            return identities

        except Exception as e:
            print(f"❌ Error loading identity database: {e}")
            return {}

    def generate_simple_identity(self, agent_id: str = None) -> AgentIdentity:
        """Generate simple identity for testing"""
        if agent_id is None:
            agent_id = f"test_agent_{int(time.time() * 1000)}"

        # Use simple default values
        personality = "balanced"
        dna_genes = {"curiosity": 0.5, "creativity": 0.5, "logic": 0.5}

        return self.generate_identity(agent_id, personality, dna_genes)


def main():
    """Main function for testing the name generator"""
    print("🎭 Agent Name Generator - Lore N.A.")
    print("===================================")

    # Create generator
    name_generator = AgentNameGenerator()

    # Generate test identities
    test_personalities = [
        'Brave Speculator',
        'Bargain Hunter',
        'Innovative Artist',
        'Community Leader',
        'Loyal Follower',
        'Methodical Analyst',
        'Social Adventurer'
    ]

    print("\n🧬 Generating test identities...")

    identities = {}

    for i, personality in enumerate(test_personalities):
        agent_id = f"test_agent_{i+1:03d}"

        # Simulated DNA
        test_dna = {
            'limbo': {'risk_tolerance': random.uniform(0, 1), 'quality_preference': random.uniform(0, 1)},
            'odyssey': {'creativity_drive': random.uniform(0, 1), 'experimentation': random.uniform(0, 1)},
            'ritual': {'leadership_tendency': random.uniform(0, 1), 'community_bonding': random.uniform(0, 1)},
            'engine': {'analytical_thinking': random.uniform(0, 1), 'decision_confidence': random.uniform(0, 1)},
            'logs': {'operational_efficiency': random.uniform(0, 1), 'quality_focus': random.uniform(0, 1)}
        }

        # Generate identity
        identity = name_generator.generate_identity(agent_id, personality, test_dna)
        identities[agent_id] = identity

        print(f"\n👤 {identity.agent_id}:")
        print(f"   Name: {identity.full_name}")
        print(f"   Nickname: {identity.nickname}")
        print(f"   Title: {identity.title}")
        print(f"   Origin: {identity.origin}")
        print(f"   Personality: {identity.personality_archetype}")
        print(f"   Meaning: {identity.name_meaning}")

        # Show different display formats
        print(f"   Full format: {name_generator.get_display_name(identity, 'full')}")
        print(f"   Casual format: {name_generator.get_display_name(identity, 'casual')}")

    print("\n🎤 Introduction examples:")
    for i, identity in enumerate(list(identities.values())[:3]):
        print(f"\n{i+1}. {name_generator.generate_introduction(identity)}")

    # Save test database
    test_db_path = "/tmp/agent_identities_test.json"
    name_generator.save_identities_database(identities, test_db_path)

    # Test loading
    print("\n📚 Testing database loading...")
    loaded_identities = name_generator.load_identities_database(test_db_path)

    print(f"✅ {len(loaded_identities)} identities loaded successfully!")

    # Statistics
    print("\n📊 Statistics of generated identities:")

    personality_count = {}
    origin_count = {}

    for identity in identities.values():
        personality = identity.personality_archetype
        origin = identity.origin

        personality_count[personality] = personality_count.get(personality, 0) + 1
        origin_count[origin] = origin_count.get(origin, 0) + 1

    print("\n🎭 By personality:")
    for personality, count in personality_count.items():
        print(f"   {personality}: {count}")

    print("\n🌍 By origin:")
    for origin, count in origin_count.items():
        print(f"   {origin}: {count}")

    print("\n✅ Name generator test completed!")


if __name__ == "__main__":
    main()
