technologies = {
    'percent': {
        'infantry': {
            'soft_attack': [
                +0.05 * 3,  # 改良步兵装备
            ],
            'hard_attack': [
                +0.25 * 2,  # 步兵反坦克武器
            ],
            'ap_attack': [
                +1 * 2,  # 步兵反坦克武器
            ],
            'defense': [
                +0.05 * 4,  # 支援武器
            ],
            'breakthrough': [
                +0.05 * 4,  # 支援武器
            ],
        },
        'marine': {
            'soft_attack': [
                +0.05 * 3,  # 改良步兵装备
                +0.05,  # 海军陆战队
                +0.05,  # 特种部队
            ],
            'hard_attack': [
                +0.25 * 2,  # 步兵反坦克武器
            ],
            'ap_attack': [
                +1 * 2,  # 步兵反坦克武器
            ],
            'defense': [
                +0.03 * 4,  # 支援武器
                +0.05,  # 特种部队
            ],
            'breakthrough': [
                +0.03 * 4,  # 支援武器
            ],
        },
        'mountaineers': {
            'soft_attack': [
                +0.05 * 3,  # 改良步兵装备
                +0.05,  # 山地步兵
                +0.05,  # 特种部队
            ],
            'hard_attack': [
                +0.25 * 2,  # 步兵反坦克武器
            ],
            'ap_attack': [
                +1 * 2,  # 步兵反坦克武器
            ],
            'defense': [
                +0.03 * 4,  # 支援武器
                +0.05,  # 特种部队
            ],
            'breakthrough': [
                +0.03 * 4,  # 支援武器
            ],
        },
        'paratrooper': {
            'soft_attack': [
                +0.05 * 3,  # 改良步兵装备
                +0.05,  # 伞兵
                +0.05,  # 特种部队
            ],
            'hard_attack': [
                +0.25 * 2,  # 步兵反坦克武器
            ],
            'ap_attack': [
                +1 * 2,  # 步兵反坦克武器
            ],
            'defense': [
                +0.03 * 4,  # 支援武器
                +0.05,  # 特种部队
            ],
            'breakthrough': [
                +0.03 * 4,  # 支援武器
            ],
        },
        'motorized': {
            'soft_attack': [
                +0.05 * 2,  # 改良步兵装备
                +0.1,  # 改良步兵装备
            ],
            'hard_attack': [
                +0.25 * 2,  # 步兵反坦克武器
            ],
            'ap_attack': [
                +1 * 2,  # 步兵反坦克武器
            ],
            'armor_value': [
                +1  # 机械化装备
            ],
            'defense': [
                +0.05 * 4,  # 支援武器
            ],
            'breakthrough': [
                +0.05 * 4,  # 支援武器
            ],
        },
        'mechanized': {
            'soft_attack': [
                +0.05 * 2,  # 改良步兵装备
                +0.1,  # 改良步兵装备
                +0.15  # 机械化装备
            ],
            'hard_attack': [
                +0.25 * 2,  # 步兵反坦克武器
                +0.15  # 机械化装备
            ],
            'ap_attack': [
                +1 * 2,  # 步兵反坦克武器
            ],
            'defense': [
                +0.05 * 4,  # 支援武器
            ],
            'breakthrough': [
                +0.05 * 4,  # 支援武器
            ],
        },
        'cavalry': {
            'soft_attack': [
                +0.05 * 2,  # 改良步兵装备
                +0.1,  # 改良步兵装备
            ],
            'hard_attack': [
                +0.25 * 2,  # 步兵反坦克武器
            ],
            'ap_attack': [
                +1 * 2,  # 步兵反坦克武器
            ],
            'defense': [
                +0.05 * 2,  # 支援武器
            ],
            'breakthrough': [
                +0.05 * 2,  # 支援武器
            ],
        },
        'artillery_brigade': {
            'soft_attack': [
                +0.1 * 4,  # 改良火炮
            ],
        },
        'anti_air_brigade': {
            'air_attack': [
                +0.1 * 3,  # 改良防空炮
            ],
        },
        'anti_tank_brigade': {
            'hard_attack': [
                +0.1 * 3,  # 改良反坦克炮
            ],
            'ap_attack': [
                +0.2,  # 改良反坦克炮
                +0.1 * 2,  # 改良反坦克炮
            ],
        },
        'rocket_artillery_brigade': {
            'soft_attack': [
                +0.15 * 2,  # 火箭炮升级
            ],
        },
        'motorized_rocket_brigade': {
            'soft_attack': [
                +0.15 * 2,  # 火箭炮升级
                +0.3  # 火箭炮升级
            ],
        },
        'artillery': {
            'soft_attack': [
                +0.1 * 4,  # 改良火炮
            ],
        },
        'anti_air': {
            'air_attack': [
                +0.1 * 3,  # 改良防空炮
            ],
        },
        'anti_tank': {
            'hard_attack': [
                +0.1 * 3,  # 改良反坦克炮
            ],
            'ap_attack': [
                +0.2,  # 改良反坦克炮
                +0.1 * 2,  # 改良反坦克炮
            ]
        },
        'rocket_artillery': {
            'soft_attack': [
                +0.15 * 2,  # 火箭炮升级
            ],
        },
    },

    'base': {
        'marine': {
            'max_organisation': [
                5 * 2,  # 海军陆战队
                5 * 2,  # 特种部队
            ],
        },
        'mountaineers': {
            'max_organisation': [
                5 * 2,  # 山地步兵
                5 * 2,  # 特种部队
            ],
        },
        'paratrooper': {
            'max_organisation': [
                5 * 2,  # 伞兵
                5 * 2,  # 特种部队
            ],
        },
    },
}

equipments = {
    'infantry': ['infantry_equipment_3'],
    'bicycle_battalion': ['infantry_equipment_3'],
    'marine': ['infantry_equipment_3'],
    'mountaineers': ['infantry_equipment_3'],
    'paratrooper': ['infantry_equipment_3'],
    'motorized': ['infantry_equipment_3', 'motorized_equipment_1'],
    'mechanized': ['infantry_equipment_3', 'mechanized_equipment_3'],
    'cavalry': ['infantry_equipment_3'],
    'artillery_brigade': ['artillery_equipment_3'],
    'anti_air_brigade': ['anti_air_equipment_3'],
    'anti_tank_brigade': ['anti_tank_equipment_3'],
    'rocket_artillery_brigade': ['rocket_artillery_equipment_2'],
    'motorized_rocket_brigade': ['motorized_rocket_equipment_1'],
    'artillery': ['artillery_equipment_3'],
    'anti_air': ['anti_air_equipment_3'],
    'anti_tank': ['anti_tank_equipment_3'],
    'rocket_artillery': ['rocket_artillery_equipment_2'],
    'engineer': ['infantry_equipment_3', 'support_equipment_1'],
    'recon': ['infantry_equipment_3'],

    'light_armor': ['light_tank_equipment_3'],
    'medium_armor': ['medium_tank_equipment_3'],
    'heavy_armor': ['heavy_tank_equipment_3'],
    'super_heavy_armor': ['super_heavy_tank_equipment_1'],
    'modern_armor': ['modern_tank_equipment_1'],

    'light_tank_destroyer_brigade': ['light_tank_destroyer_equipment_3'],
    'medium_tank_destroyer_brigade': ['medium_tank_destroyer_equipment_3'],
    'heavy_tank_destroyer_brigade': ['heavy_tank_destroyer_equipment_3'],
    'super_heavy_tank_destroyer_brigade': ['super_heavy_tank_destroyer_equipment_1'],
    'modern_tank_destroyer_brigade': ['modern_tank_destroyer_equipment_1'],

    'light_sp_artillery_brigade': ['light_tank_artillery_equipment_3'],
    'medium_sp_artillery_brigade': ['medium_tank_artillery_equipment_3'],
    'heavy_sp_artillery_brigade': ['heavy_tank_artillery_equipment_3'],
    'super_heavy_sp_artillery_brigade': ['super_heavy_tank_artillery_equipment_1'],
    'modern_sp_artillery_brigade': ['modern_tank_destroyer_equipment_1'],

    'light_sp_anti_air_brigade': ['light_tank_aa_equipment_3'],
    'medium_sp_anti_air_brigade': ['medium_tank_aa_equipment_3'],
    'heavy_sp_anti_air_brigade': ['heavy_tank_aa_equipment_3'],
    'super_sp_anti_air_brigade': ['super_heavy_tank_aa_equipment_1'],
    'modern_sp_anti_air_brigade': ['modern_tank_destroyer_equipment_1'],

}
