from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Counter
import time
import random
import schedule

# Create Prometheus metrics
registry = CollectorRegistry()

# Gauge for account balance with 'account_id' label
balance = Gauge('bank_account_balance', 'Current account balance', ['account_id'], registry=registry)

# Counter for successful auto-debit transactions
successful_debits = Counter('bank_auto_debit_successful', 'Successful auto-debit transactions', registry=registry)

# Counter for failed auto-debit transactions
failed_debits = Counter('bank_auto_debit_failed', 'Failed auto-debit transactions', registry=registry)


def simulate_auto_debit(account_id, amount):
  # Simulate auto-debit action
  # In a real system, you would interact with the bank's API or database to perform the debit.

  # Simulate success or failure randomly
  success = random.choice([True, False])

  if success:
    # Update balance with 'account_id' label
    balance.labels(account_id=account_id).set(amount)
    successful_debits.inc()
    print(f"Auto-debit for account {account_id} successful. New balance: ${amount:.2f}")
  else:
    failed_debits.inc()
    print(f"Auto-debit for account {account_id} failed. Balance remains unchanged.")


def push_metrics_to_prometheus(pushgateway_url):
  # Push metrics to Prometheus Pushgateway
  try:
    push_to_gateway(pushgateway_url, job='bank_auto_debit', registry=registry)
    print(f"Metrics pushed to Prometheus Pushgateway: {pushgateway_url}")
  except Exception as e:
    print(f"Failed to push metrics: {e}")


def process():
  account_ids = [111, 122, 123, 124, 314, 987, 261, 120, 872, 542, 342, 614]

  for acc in account_ids:
    # Simulate auto-debit for account 123 with $100
    simulate_auto_debit(account_id=acc, amount=random.randint(100, 100000))

    # Push metrics to Prometheus Pushgateway (provide your Pushgateway URL)
    push_metrics_to_prometheus('http://prometheus-pushgateway:9091')

if __name__ == "__main__":
  schedule.every(1).minutes.do(process)

  while True:
    schedule.run_pending()
    time.sleep(1)
