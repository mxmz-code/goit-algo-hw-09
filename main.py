import time
import os
from datetime import datetime
from colorama import Fore, Style, init

# Ініціалізація colorama
init(autoreset=True)

# Визначення валют і їх номіналів
currencies = {
    "GOIT": [50, 25, 10, 5, 2, 1],
    "USD": [100, 50, 20, 10, 5, 1],
    "EUR": [100, 50, 20, 10, 5, 2, 1],
    "GBP": [100, 50, 20, 10, 5, 2]
}

# Валюта за замовчуванням
default_currency = "GOIT"

# Функція для очищення екрану
def clear_screen():
    if os.name == 'nt':  # Якщо Windows
        os.system('cls')
    else:  # Якщо Unix/Linux/Mac
        os.system('clear')

# Функція для логування результатів
def log_results(amount, currency, greedy_result, dp_result, greedy_time, dp_time):
    current_time = datetime.now().strftime("%H:%M:%S")  # Поточний час у форматі "HH:MM:SS"
    log_data = f"{current_time} - {currency} - Сума: {amount} - Жадібний алгоритм: {greedy_result}, Час: {greedy_time:.9f} сек - Динамічне програмування: {dp_result}, Час: {dp_time:.9f} сек\n"
    with open("log.txt", "a") as log_file:
        log_file.write(log_data)

# Функція жадібного алгоритму
def find_coins_greedy(amount, coins):
    result = {}
    for coin in coins:
        if amount >= coin:
            count = amount // coin
            result[coin] = count
            amount -= count * coin
    return result

# Функція динамічного програмування
def find_min_coins(amount, coins):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    coin_used = [0] * (amount + 1)
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                coin_used[i] = coin
    
    result = {}
    while amount > 0:
        coin = coin_used[amount]
        result[coin] = result.get(coin, 0) + 1
        amount -= coin

    return result

# Оцінка часу виконання
def measure_time(amount, coins, currency):
    start_time = time.perf_counter()
    greedy_result = find_coins_greedy(amount, coins)
    greedy_time = time.perf_counter() - start_time
    
    start_time = time.perf_counter()
    dp_result = find_min_coins(amount, coins)
    dp_time = time.perf_counter() - start_time

    # Порівняння часів
    if dp_time != 0:
        time_diff = dp_time - greedy_time
        time_percent = (time_diff / greedy_time) * 100
        print(Fore.CYAN + f"\nЧасове порівняння:\nЖадібний алгоритм: {greedy_time:.9f} сек\nДинамічне програмування: {dp_time:.9f} сек\nРізниця в часі: {time_diff:.9f} сек\nПроцентна різниця: {time_percent:.2f}%")
    else:
        print(Fore.RED + "Динамічне програмування не виконано або не потребує часу.")
    
    # Логування результатів у файл
    log_results(amount, currency, greedy_result, dp_result, greedy_time, dp_time)

    return greedy_time, dp_time

# Діалог з користувачем
def user_dialog():
    clear_screen()
    print(Fore.BLUE + Style.BRIGHT + "Ласкаво просимо до касового апарату!")
    print(Fore.CYAN + "Цей інструмент допоможе вам визначити оптимальний спосіб видачі решти за допомогою різних алгоритмів.")
    print(Fore.CYAN + "У вас є можливість вибрати одну з доступних валют та обчислити кількість монет для будь-якої суми.")
    print(Fore.CYAN + "Ви можете ввести як одну суму, так і кілька сум через пробіл або кому.")

    while True:
        # Вибір валюти за допомогою цифр
        print("\nДоступні валюти та їх номінали монет:")
        print("1. GOIT: [50, 25, 10, 5, 2, 1]")
        print("2. USD: [100, 50, 20, 10, 5, 1]")
        print("3. EUR: [100, 50, 20, 10, 5, 2, 1]")
        print("4. GBP: [100, 50, 20, 10, 5, 2]")

        currency_choice = input(Fore.MAGENTA + "\nВиберіть валюту (1-4, за замовчуванням 1): ").strip()

        if currency_choice == "" or currency_choice == "1":
            currency_choice = "GOIT"
        elif currency_choice == "2":
            currency_choice = "USD"
        elif currency_choice == "3":
            currency_choice = "EUR"
        elif currency_choice == "4":
            currency_choice = "GBP"
        else:
            print(Fore.RED + "Невірний вибір. За замовчуванням вибрана валюта GOIT.")
            currency_choice = "GOIT"
        
        coins = currencies[currency_choice]

        # Інтерактивна підказка
        print(Fore.CYAN + f"Ви обрали валюту {currency_choice}. Номінали монет: {coins}.")
        print(Fore.CYAN + "Тепер введіть суму або суми для обчислення кількості монет.")

        # Введення кількох сум
        sums_input = input(Fore.MAGENTA + "\nВведіть суми через пробіл або кому (наприклад: 1234 5678 9123): ").strip()
        sums = [int(x) for x in sums_input.replace(",", " ").split() if x.isdigit()]

        if not sums:
            print(Fore.RED + "Будь ласка, введіть хоча б одну суму.")
            continue

        # Обробка кожної суми
        for amount in sums:
            print(Fore.CYAN + f"\nОбчислення для суми {amount} ({currency_choice}):")
            greedy_result = find_coins_greedy(amount, coins)
            dp_result = find_min_coins(amount, coins)
            
            print(Fore.GREEN + f"Рішення жадібним алгоритмом: {greedy_result}")
            print(Fore.YELLOW + f"Рішення динамічним програмуванням: {dp_result}")
            
            # Оцінка часу виконання
            measure_time(amount, coins, currency_choice)
        
        # Запит на продовження або завершення
        while True:
            action = input(Fore.CYAN + "Введіть 'y' для продовження або 'n' для завершення: ").lower()
            if action == 'n':
                print(Fore.GREEN + "До побачення!")
                return
            elif action == 'y':
                break
            else:
                print(Fore.RED + "Невірний ввід. Будь ласка, введіть 'y' або 'n'.")

if __name__ == "__main__":
    user_dialog()
