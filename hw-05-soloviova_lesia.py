# -*- coding: utf-8 -*-
"""goit-numericalpy-hw-05-soloviova_lesia.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dwqFLaS6zOkuDfX3l0JUEW83Mobb1Y3j
"""

import numpy as np
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

print("Крок 1: Генерація даних")
# Встановлюємо фіксоване значення для генератора випадкових чисел для відтворюваності
np.random.seed(42)

# Генерація 100 випадкових значень для x1 та x2
x1 = np.random.rand(100)
x2 = np.random.rand(100)

# Функція для обчислення y за поліномом другого степеня
def polynomial(x1, x2):
    return 4 * x1**2 + 5 * x2**2 - 2 * x1 * x2 + 3 * x1 - 6 * x2

# Обчислюємо цільову змінну y за допомогою полінома
y = polynomial(x1, x2)

# Виведення перших 5 значень для перевірки
print("x1:", x1[:5])
print("x2:", x2[:5])
print("y:", y[:5])

print("Крок 2: Генерація додаткових ознак")
# Створення об'єкта PolynomialFeatures для другого степеня
poly = PolynomialFeatures(degree=2, include_bias=False)

# Створення матриці ознак
X = np.column_stack((x1, x2))
X_poly = poly.fit_transform(X)

# Виведення форми матриці ознак
print("Форма X_poly:", X_poly.shape)
print("Перші 5 рядків X_poly:\n", X_poly[:5])

print("Крок 3: Реалізація методів градієнтного спуску\n")
print("3.1. Стандартний градієнтний спуск")
def polynomial_regression_gradient_descent(X, y, learning_rate=0.01, iterations=1000):
    n_samples, n_features = X.shape
    theta = np.zeros(n_features)  # Початкові параметри
    losses = []  # Для збереження похибок
    for iteration in range(iterations):
        gradients = 2/n_samples * X.T.dot(X.dot(theta) - y)
        theta -= learning_rate * gradients
        # Обчислення похибки (MSE)
        y_pred = X.dot(theta)
        loss = mean_squared_error(y, y_pred)
        losses.append(loss)
    return theta, losses

# Виклик функції та виведення результатів
theta_gd = polynomial_regression_gradient_descent(X_poly, y)
print("Коефіцієнти (стандартний градієнтний спуск):", theta_gd)

print("\n3.2. SGD (Stochastic Gradient Descent)")
def polynomial_regression_SGD(X, y, learning_rate=0.01, iterations=1000):
    n_samples, n_features = X.shape
    theta = np.zeros(n_features)  # Початкові параметри
    losses = []  # Для збереження похибок
    for iteration in range(iterations):
        for i in range(n_samples):
            random_index = np.random.randint(n_samples)
            xi = X[random_index:random_index+1]
            yi = y[random_index:random_index+1]
            gradients = 2 * xi.T.dot(xi.dot(theta) - yi)
            theta -= learning_rate * gradients
        # Обчислення похибки (MSE)
        y_pred = X.dot(theta)
        loss = mean_squared_error(y, y_pred)
        losses.append(loss)
    return theta, losses

# Виклик функції та виведення результатів
theta_sgd = polynomial_regression_SGD(X_poly, y)
print("Коефіцієнти (SGD):", theta_sgd)

def polynomial_regression_rmsprop(X, y, learning_rate=0.01, iterations=1000, beta=0.9, epsilon=1e-8):
    n_samples, n_features = X.shape
    theta = np.zeros(n_features)  # Початкові параметри
    v_theta = np.zeros(n_features)  # Ініціалізація швидкості
    losses = []  # Для збереження похибок
    for iteration in range(iterations):
        gradients = 2/n_samples * X.T.dot(X.dot(theta) - y)
        v_theta = beta * v_theta + (1 - beta) * gradients**2
        theta -= learning_rate * gradients / (np.sqrt(v_theta) + epsilon)
        # Обчислення похибки (MSE)
        y_pred = X.dot(theta)
        loss = mean_squared_error(y, y_pred)
        losses.append(loss)
    return theta, losses

# Виклик функції та виведення результатів
theta_rmsprop = polynomial_regression_rmsprop(X_poly, y)
print("Коефіцієнти (RMSProp):", theta_rmsprop)

print("\n3.4. Adam")
def polynomial_regression_adam(X, y, learning_rate=0.01, iterations=1000, beta1=0.9, beta2=0.999, epsilon=1e-8):
    n_samples, n_features = X.shape
    theta = np.zeros(n_features)  # Початкові параметри
    m_theta = np.zeros(n_features)  # Ініціалізація першого моменту
    v_theta = np.zeros(n_features)  # Ініціалізація другого моменту
    losses = []  # Для збереження похибок
    for iteration in range(iterations):
        gradients = 2/n_samples * X.T.dot(X.dot(theta) - y)
        m_theta = beta1 * m_theta + (1 - beta1) * gradients
        v_theta = beta2 * v_theta + (1 - beta2) * gradients**2
        m_theta_hat = m_theta / (1 - beta1**(iteration+1))
        v_theta_hat = v_theta / (1 - beta2**(iteration+1))
        theta -= learning_rate * m_theta_hat / (np.sqrt(v_theta_hat) + epsilon)
        # Обчислення похибки (MSE)
        y_pred = X.dot(theta)
        loss = mean_squared_error(y, y_pred)
        losses.append(loss)
    return theta, losses

# Виклик функції та виведення результатів
theta_adam = polynomial_regression_adam(X_poly, y)
print("Коефіцієнти (Adam):", theta_adam)

print("\n3.5. Nadam")
def polynomial_regression_nadam(X, y, learning_rate=0.01, iterations=1000, beta1=0.9, beta2=0.999, epsilon=1e-8):
    n_samples, n_features = X.shape
    theta = np.zeros(n_features)  # Початкові параметри
    m_theta = np.zeros(n_features)  # Ініціалізація першого моменту
    v_theta = np.zeros(n_features)  # Ініціалізація другого моменту
    losses = []  # Для збереження похибок
    for iteration in range(iterations):
        gradients = 2/n_samples * X.T.dot(X.dot(theta) - y)
        m_theta = beta1 * m_theta + (1 - beta1) * gradients
        v_theta = beta2 * v_theta + (1 - beta2) * gradients**2
        m_theta_hat = m_theta / (1 - beta1**(iteration+1))
        v_theta_hat = v_theta / (1 - beta2**(iteration+1))
        theta -= learning_rate * (beta1 * m_theta_hat + (1 - beta1) * gradients / (1 - beta1**(iteration+1))) / (np.sqrt(v_theta_hat) + epsilon)
        # Обчислення похибки (MSE)
        y_pred = X.dot(theta)
        loss = mean_squared_error(y, y_pred)
        losses.append(loss)
    return theta, losses

# Виклик функції та виведення результатів
theta_nadam = polynomial_regression_nadam(X_poly, y)
print("Коефіцієнти (Nadam):", theta_nadam)

# Commented out IPython magic to ensure Python compatibility.
print("\nКрок 4: Вимірювання часу роботи функцій\n")

# Тепер виміряємо час роботи кожної функції за допомогою %timeit

# Вимірювання часу для стандартного градієнтного спуску
print("Gradient Descent:")
# %timeit polynomial_regression_gradient_descent(X_poly, y)

# Вимірювання часу для SGD
print("\nSGD:")
# %timeit polynomial_regression_SGD(X_poly, y)

# Вимірювання часу для RMSProp
print("\nRMSProp:")
# %timeit polynomial_regression_rmsprop(X_poly, y)

# Вимірювання часу для Adam
print("\nAdam:")
# %timeit polynomial_regression_adam(X_poly, y)

# Вимірювання часу для Nadam
print("\nNadam:")
# %timeit polynomial_regression_nadam(X_poly, y)

print("\nКрок 5.1: Обчислення середньоквадратичної похибки (MSE)\n")
def mean_squared_error(y_true, y_pred):
    # Функція обчислює середньоквадратичну похибку між справжніми та передбаченими значеннями
    return np.mean((y_true - y_pred)**2)

# Передбачення значень для кожного методу
y_pred_gd = X_poly.dot(theta_gd)
y_pred_sgd = X_poly.dot(theta_sgd)
y_pred_rmsprop = X_poly.dot(theta_rmsprop)
y_pred_adam = X_poly.dot(theta_adam)
y_pred_nadam = X_poly.dot(theta_nadam)

# Обчислення MSE для кожного методу
mse_gd = mean_squared_error(y, y_pred_gd)
mse_sgd = mean_squared_error(y, y_pred_sgd)
mse_rmsprop = mean_squared_error(y, y_pred_rmsprop)
mse_adam = mean_squared_error(y, y_pred_adam)
mse_nadam = mean_squared_error(y, y_pred_nadam)

# Виведення результатів
print("MSE (Gradient Descent):", mse_gd)
print("MSE (SGD):", mse_sgd)
print("MSE (RMSProp):", mse_rmsprop)
print("MSE (Adam):", mse_adam)
print("MSE (Nadam):", mse_nadam)

def plot_losses(losses, label):
    # Функція для візуалізації зміни похибки протягом ітерацій
    plt.plot(losses, label=label)

# Кількість ітерацій для порівняння методів
iterations = 1000

# Виконання кожного з методів і збереження їхніх похибок
theta_gd, gd_losses = polynomial_regression_gradient_descent(X_poly, y, iterations=iterations)
theta_sgd, sgd_losses = polynomial_regression_SGD(X_poly, y, iterations=iterations)
theta_rmsprop, rmsprop_losses = polynomial_regression_rmsprop(X_poly, y, iterations=iterations)
theta_adam, adam_losses = polynomial_regression_adam(X_poly, y, iterations=iterations)
theta_nadam, nadam_losses = polynomial_regression_nadam(X_poly, y, iterations=iterations)

# Побудова графіків для всіх методів
plot_losses(gd_losses, label="Gradient Descent")
plot_losses(sgd_losses, label="SGD")
plot_losses(rmsprop_losses, label="RMSProp")
plot_losses(adam_losses, label="Adam")
plot_losses(nadam_losses, label="Nadam")

# Налаштування графіку
plt.xlabel("Ітерації")
plt.ylabel("MSE")
plt.title("Порівняння методів оптимізації")
plt.legend()
plt.show()

print("""
Висновки:

1.Швидкість збіжності:
- Gradient Descent (GD): Повільний, але стабільний. Потребує багато ітерацій для досягнення мінімуму.
- SGD: Швидший за GD, але може бути нестабільним через випадковість у виборі даних.
- RMSProp: Швидше за GD, стабільніший за SGD. Використовує адаптивний learning rate.
- Adam: Найшвидший і найстабільніший. Добре підходить для більшості задач.
- Nadam: Покращена версія Adam, ще швидше збігається.

2.Точність (MSE):
- Усі методи досягають схожої точності, але Adam і Nadam роблять це значно швидше.
- SGD може мати вищу MSE через нестабільність.

3.Обчислювальна ефективність:
- GD: Вимагає багато ітерацій, але обчислювально простий.
- SGD: Швидший, але може потребувати більше ітерацій для стабілізації.
- RMSProp, Adam, Nadam: Найефективніші. Вимагають менше ітерацій для досягнення мінімуму.

4.Рекомендації:
- Для великих наборів даних краще використовувати Adam або Nadam через їхню швидкість і стабільність.
- Якщо обчислювальні ресурси обмежені, можна спробувати RMSProp.
- SGD підходить для задач, де важлива швидкість, але не критична точність.
""")