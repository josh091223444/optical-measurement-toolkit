from src.metrics import percentage_error


measured = 1.95
theoretical = 2.00

error = percentage_error(measured, theoretical)

print(f"Percentage error: {error:.2f}%")