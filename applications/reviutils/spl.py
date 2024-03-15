import re

class NoiseLevel:
    def __init__(self, area):
        self.area = area
        self.day_level = NoiseLevel.get_level(area, is_day=True)
        self.night_level = NoiseLevel.get_level(area, is_day=False)
       
    @staticmethod
    def get_level(area, is_day):
        ''' 环境噪声限值 '''
        area = str(area)
        if '4a' in area and not is_day:
            return 55
        base_night = 40
        match = re.search(r'\d', area)

        assert match is not None, '请检查功能区是否正确'
        digit = match.group()
        digit = int(digit)
        assert digit in range(5), '请检查功能区是否正确'
        level = base_night + digit * 5
        if is_day:
            level += 10
        return level