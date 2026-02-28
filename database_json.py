import json
import os
from datetime import datetime

class JSONDatabase:
    def __init__(self, filename='markers.json'):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(current_dir, filename)
        print(f"📁 Файл данных: {self.filename}")
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_empty_structure()
        return self.get_empty_structure()
    
    def get_empty_structure(self):
        return {
            'users': {},
            'districts': {
                'Адмиралтейский район': {'name': 'Адмиралтейский район', 'markers_count': 0},
                'Василеостровский район': {'name': 'Василеостровский район', 'markers_count': 0},
                'Выборгский район': {'name': 'Выборгский район', 'markers_count': 0},
                'Калининский район': {'name': 'Калининский район', 'markers_count': 0},
                'Кировский район': {'name': 'Кировский район', 'markers_count': 0},
                'Колпинский район': {'name': 'Колпинский район', 'markers_count': 0},
                'Красногвардейский район': {'name': 'Красногвардейский район', 'markers_count': 0},
                'Красносельский район': {'name': 'Красносельский район', 'markers_count': 0},
                'Кронштадтский район': {'name': 'Кронштадтский район', 'markers_count': 0},
                'Курортный район': {'name': 'Курортный район', 'markers_count': 0},
                'Московский район': {'name': 'Московский район', 'markers_count': 0},
                'Невский район': {'name': 'Невский район', 'markers_count': 0},
                'Петроградский район': {'name': 'Петроградский район', 'markers_count': 0},
                'Петродворцовый район': {'name': 'Петродворцовый район', 'markers_count': 0},
                'Приморский район': {'name': 'Приморский район', 'markers_count': 0},
                'Пушкинский район': {'name': 'Пушкинский район', 'markers_count': 0},
                'Фрунзенский район': {'name': 'Фрунзенский район', 'markers_count': 0},
                'Центральный район': {'name': 'Центральный район', 'markers_count': 0}
            },
            'markers': [],
            'marker_counter': 0
        }
    
    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_or_create_user(self, telegram_id, username, first_name, last_name):
        user_id = str(telegram_id)
        if user_id not in self.data['users']:
            self.data['users'][user_id] = {
                'telegram_id': telegram_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'registered_at': datetime.now().isoformat(),
                'rating': 0,
                'markers_count': 0
            }
            self.save_data()
            print(f"👤 Новый пользователь: {username or first_name}")
        
        return {'id': user_id, **self.data['users'][user_id]}
    
    def add_marker(self, user_id, district_name, category, lat, lng):
        self.data['marker_counter'] += 1
        marker_id = self.data['marker_counter']
        
        marker = {
            'id': marker_id,
            'user_id': user_id,
            'district_name': district_name,
            'category': category,
            'lat': lat,
            'lng': lng,
            'created_at': datetime.now().isoformat(),
            'status': 'pending',
            'confirmed_count': 0,
            'rejected_count': 0
        }
        
        self.data['markers'].append(marker)
        
        if district_name in self.data['districts']:
            self.data['districts'][district_name]['markers_count'] += 1
        
        self.save_data()
        print(f"📍 Добавлена метка #{marker_id}")
        return marker