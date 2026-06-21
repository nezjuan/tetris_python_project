class Score:
    LINE_SCORES = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def __init__(self):
        self._score = 0
        self._lines = 0

    @property
    def score(self):
        return self._score
    
    @property
    def lines(self):
        return self._lines
    
    def add_lines(self, count):
        self._lines += count
        self._score += self.LINE_SCORES.get(count, 0)

    def reset(self):
        self._score = 0
        self._lines = 0

    def __int__(self):
        return self.score
    
class Record: 
    def __init__(self, path="Records"):
        self._path = path

    def get(self):
        try:
            with open(self._path) as record_file:
                content = record_file.readline().strip()
                return int(content) if content else 0
        except FileNotFoundError:
            with open(self.path, 'w') as record_file:
                record_file.write('0')
            return 0
        
    def update(self, score):
        new_record = max(self. get(), int(score))
        with open(self._path, 'w') as record_file:
            record_file.write(str(new_record))
            return new_record