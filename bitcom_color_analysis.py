from collections import Counter
import psycopg2
import random
import statistics
from config import settings 

data = {
    "MONDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "TUESDAY": "ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
    "WEDNESDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
    "THURSDAY": "BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "FRIDAY": "GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
}

# Flatten color data
all_colors = []
for colors in data.values():
    all_colors.extend(colors.replace(" ", "").split(","))

# Count color occurrences
color_counts = Counter(all_colors)

# 1. Mean color (most frequent)
mean_color = color_counts.most_common(1)[0][0]
print("Mean color:", mean_color)

# 2. Most worn color
most_worn_color = mean_color
print("Most worn color:", most_worn_color)

# 3. Median color
sorted_colors = sorted(color_counts.items(), key=lambda x: x[1])
median_color = sorted_colors[len(sorted_colors) // 2][0]
print("Median color:", median_color)

# 4. Variance of colors
color_frequencies = list(color_counts.values())
variance = statistics.variance(color_frequencies)
print("Variance of colors:", variance)

# 5. Probability of choosing red
prob_red = color_counts["RED"] / len(all_colors)
print("Probability of choosing red:", prob_red)

# 6. Save to PostgreSQL
def save_to_db():
    try:
        conn = psycopg2.connect(
            dbname=f"{settings.database_name}", user=f"{settings.database_username}", password=f"{settings.database_password}", host=f"{settings.database_hostname}", port=f"{settings.database_port}"
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS color_frequencies (
                color TEXT PRIMARY KEY,
                frequency INT
            )
        """)
        for color, freq in color_counts.items():
            cursor.execute("INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s) ON CONFLICT (color) DO UPDATE SET frequency = EXCLUDED.frequency", (color, freq))
        conn.commit()
        cursor.close()
        conn.close()
        print("Data saved to database successfully.")
    except Exception as e:
        print("Error:", e)

save_to_db()

# 7. Recursive search algorithm
def recursive_search(arr, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return recursive_search(arr, target, left, mid - 1)
    else:
        return recursive_search(arr, target, mid + 1, right)

numbers = sorted(random.sample(range(1, 100), 20))
target = int(input("Enter number to search: "))
result = recursive_search(numbers, target, 0, len(numbers) - 1)
print("Number found at index:", result if result != -1 else "Not found")

# 8. Convert random 4-digit binary to base 10
random_binary = "".join(random.choice("01") for _ in range(4))
base_10 = int(random_binary, 2)
print("Random binary:", random_binary, "Base 10:", base_10)

# 9. Sum first 50 Fibonacci numbers
def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

fib_sum = fibonacci_sum(50)
print("Sum of first 50 Fibonacci numbers:", fib_sum)
