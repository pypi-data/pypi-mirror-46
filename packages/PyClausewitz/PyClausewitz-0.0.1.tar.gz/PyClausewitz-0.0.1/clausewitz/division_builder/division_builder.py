from collections import Counter

from clausewitz.utils import get_item_dict, round_sum, round_min, round_max, round_util


class LandDivisionBuilder:
    def __init__(self, root_path: str):
        units_file_list = [
            'anti_tank.txt', 'anti_tank_brigade.txt', 'anti-air.txt', 'anti-air_brigade.txt', 'artillery.txt',
            'artillery_brigade.txt', 'cavalry.txt', 'engineer.txt', 'field_hospital.txt', 'heavy_armor.txt',
            'infantry.txt', 'light_armor.txt', 'logistics.txt', 'maintenance.txt', 'medium_armor.txt',
            'military_police.txt',
            'modern_armor.txt', 'recon.txt', 'signal.txt', 'sp_anti-air_brigade.txt', 'sp_artillery_brigade.txt',
            'super_heavy_armor.txt', 'tank_destroyer_brigade.txt'
        ]
        self.units_dict = get_item_dict(root_path + "common/units/", units_file_list)
        equipment_file_list = [
            'anti_air.txt', 'anti_tank.txt', 'artillery.txt', 'guided_missiles.txt', 'infantry.txt', 'mechanized.txt',
            'motorized.txt', 'support.txt', 'tank_heavy.txt', 'tank_light.txt', 'tank_medium.txt', 'tank_modern.txt',
            'tank_super_heavy.txt'
        ]
        equipment_dict = get_item_dict(root_path + "common/units/equipment/", equipment_file_list)
        self.equipment_stats_dict = {}  # type: dict

        equipment_stat_list = [
            'maximum_speed', 'reliability', 'defense', 'breakthrough', 'hardness', 'armor_value', 'soft_attack',
            'hard_attack', 'ap_attack', 'air_attack', 'priority', 'visual_level'
        ]

        for equipment in equipment_dict:
            if equipment[-1:].isdigit():
                _dict = equipment_dict[equipment[:-2]].copy()
                _dict.update(equipment_dict[equipment])
                for item in set(_dict.keys()) - set(equipment_stat_list):
                    _dict.pop(item)
                self.equipment_stats_dict[equipment] = _dict

    def calculate_stats(self, division_template_dict: dict) -> dict:
        equipment_stats_dict = self.equipment_stats_dict.copy()
        stat_dicts = {}  # type: dict
        battalion_types = ['regiments', 'supports']
        stats_list = [
            'maximum_speed', 'max_strength', 'max_organisation', 'default_morale', 'suppression', 'weight',
            'supply_consumption', 'soft_attack', 'hard_attack', 'air_attack', 'defense', 'breakthrough',
            'armor_value', 'ap_attack', 'combat_width', 'manpower', 'training_time', 'need', 'reliability_factor',
            'equipment_capture_factor', 'casualty_trickleback', 'experience_loss_factor', 'entrenchment', 'recon',
            'hardness', 'priority', 'sprite'
        ]
        equipment_stats_list = [
            'maximum_speed', 'max_strength', 'max_organisation', 'default_morale', 'suppression', 'weight',
            'supply_consumption', 'soft_attack', 'hard_attack', 'air_attack', 'defense', 'breakthrough',
            'armor_value', 'ap_attack', 'combat_width', 'manpower', 'training_time', 'need', 'reliability_factor',
            'equipment_capture_factor', 'casualty_trickleback', 'experience_loss_factor', 'entrenchment', 'recon',
            'hardness'
        ]
        unit_stat_percent_list = ['soft_attack', 'hard_attack', 'breakthrough', 'defense', 'ap_attack', 'air_attack']
        for battalion_type in battalion_types:
            for battalion in set(division_template_dict[battalion_type]):
                stat_dict = {
                    'base': {},
                    'percent': {},
                }  # type: dict
                for stat in self.units_dict[battalion]:
                    if stat in unit_stat_percent_list:
                        stat_dict['percent'][stat] = self.units_dict[battalion][stat]
                    else:
                        stat_dict['base'][stat] = self.units_dict[battalion][stat]
                    stat_dict[stat] = self.units_dict[battalion][stat]
                for equipment_name in division_template_dict['equipments'][battalion]:
                    for stat in set(equipment_stats_dict[equipment_name]) & set(equipment_stats_list):
                        if stat not in stat_dict['base']:
                            stat_dict['base'][stat] = 0
                        stat_dict['base'][stat] = stat_dict['base'][stat] + equipment_stats_dict[equipment_name][stat]
                stat_dicts[battalion] = stat_dict

                if battalion in division_template_dict['technologies']['percent']:
                    for stat in division_template_dict['technologies']['percent'][battalion]:
                        if stat not in stat_dicts[battalion]['percent']:
                            stat_dicts[battalion]['percent'][stat] = 0
                        stat_dicts[battalion]['percent'][stat] = stat_dicts[battalion]['percent'][stat] \
                                                                 + sum(
                            division_template_dict['technologies']['percent'][battalion][stat])
                if battalion in division_template_dict['technologies']['base']:
                    for stat in division_template_dict['technologies']['base'][battalion]:
                        if stat not in stat_dicts[battalion]['fixed']:
                            stat_dicts[battalion]['base'][stat] = 0
                        stat_dicts[battalion]['base'][stat] = stat_dicts[battalion]['base'][stat] + \
                                                              sum(division_template_dict['technologies']['base'][
                                                                      battalion][
                                                              stat])
                for stat in stat_dicts[battalion]['base']:
                    stat_dicts[battalion][stat] = stat_dicts[battalion]['base'][stat]
                    if stat in stat_dicts[battalion]['percent']:
                        stat_dicts[battalion][stat] = stat_dicts[battalion][stat] * \
                                                      (1 + stat_dicts[battalion]['percent'][stat])


        stats_dict = {k: [] for k in stats_list}  # type: dict
        for battalion_type in battalion_types:
            for battalion in division_template_dict[battalion_type]:
                for stat in set(stat_dicts[battalion]) & set(stats_list):
                    stats_dict[stat].append(stat_dicts[battalion][stat])

        _need = Counter({})  # type: Counter
        for item in stats_dict['need']:
            _need = _need + Counter(item)

        _priority = {}
        for i in range(len(stats_dict['sprite'])):
            if stats_dict['sprite'][i] not in _priority:
                _priority[stats_dict['sprite'][i]] = 0
            _priority[stats_dict['sprite'][i]] = _priority[stats_dict['sprite'][i]] + stats_dict['priority'][i]

        result = {
            'Name': division_template_dict['name'],
            'Division Names Group': division_template_dict['division_names_group'],
            'Max Speed': round_min(stats_dict['maximum_speed']),
            'HP': round_sum(stats_dict['max_strength']),
            'Organisation': round_util(sum(stats_dict['max_organisation']) / len(stats_dict['max_organisation'])),
            'Recovery Rate': round_util(sum(stats_dict['default_morale']) / len(stats_dict['default_morale'])),
            'Reconnaissance': round_sum(stats_dict['recon']),
            'Suppression': round_sum(stats_dict['suppression']),
            'Weight': round_sum(stats_dict['weight']),
            'Supply use': round_sum(stats_dict['supply_consumption']),
            'Reliability': round_sum(stats_dict['reliability_factor']),
            'Trickleback': round_sum(stats_dict['casualty_trickleback']),
            'Exp. Loss': round_sum(stats_dict['experience_loss_factor']),

            'Soft attack': round_sum(stats_dict['soft_attack']),
            'Hard attack': round_sum(stats_dict['hard_attack']),
            'Air attack': round_sum(stats_dict['air_attack']),
            'Defense': round_sum(stats_dict['defense']),
            'Breakthrough': round_sum(stats_dict['breakthrough']),
            'Armor': round_util(max(stats_dict['armor_value']) * 0.3 + sum(stats_dict['armor_value']) / len(
                stats_dict['armor_value']) * 0.7),
            'Piercing': round_util(max(stats_dict['ap_attack']) * 0.4 + sum(stats_dict['ap_attack']) / len(
                stats_dict['ap_attack']) * 0.6),
            'Entrenchment': round_sum(stats_dict['entrenchment']),
            'Eq. Capture Ratio': round_sum(stats_dict['equipment_capture_factor']),
            'Combat Width': round_sum(stats_dict['combat_width']),
            'Manpower': round_sum(stats_dict['manpower']),
            'Training Time': round_max(stats_dict['training_time']),
            'Hardness': round_util(sum(stats_dict['hardness']) / len(
                stats_dict['hardness'])),
            'Need': dict(_need),
            'Priority': dict(_priority),
            'Template': {
                'regiments': division_template_dict['regiments'],
                'supports': division_template_dict['supports'],
            }

        }
        return result
