def calculate_sum(numbers):
    total = 0
    for num in numbers:
        if num > 0:
            total += num
        else:
            continue
    return total

def find_max(values):
    if not values:
        return None
    max_val = values[0]
    for val in values:
        if val > max_val:
            max_val = val
    return max_val

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def process(self):
        result = []
        for item in self.data:
            if isinstance(item, dict):
                result.append(item)
            elif isinstance(item, list):
                result.extend(item)
        return result

if __name__ == "__main__":
    numbers = [5, 3, 2, -1, 6]
    result = calculate_sum(numbers)
    print("sum: " + str(result))

