import os
import pandas as pd
import optuna
from fetch_btc_data import fetch_btc_data
from investment_simulation import load_data, calculate_mav, simulate_investment, normalize_investment_amounts, calculate_investment_amounts

def objective(trial, df):
    weights = [
        trial.suggest_float('p10', 0, 1),
        trial.suggest_float('p20', 0, 1),
        trial.suggest_float('p30', 0, 1),
        trial.suggest_float('p50', 0, 1),
        trial.suggest_float('p80', 0, 1),
        trial.suggest_float('p130', 0, 1),
        trial.suggest_float('p210', 0, 1)
    ]
    
    # Normalize weights to sum to 1
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]
    
    investment_dates, investment_amounts, wallet_value, _ = simulate_investment(df, weights=weights)
    profit = wallet_value[-1] - investment_amounts[-1]
    return profit

def run_simulation():
    # Fetch the latest BTC data
    fetch_btc_data()
    df = load_data('btc_data.csv')
    df = calculate_mav(df)
    
    # Optimize weights using Optuna
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, df), n_trials=100)
    
    print("Best trial:")
    trial = study.best_trial
    print(f"  Value: {trial.value}")
    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")
    
    # Get the best weights
    best_weights = [
        trial.params['p10'],
        trial.params['p20'],
        trial.params['p30'],
        trial.params['p50'],
        trial.params['p80'],
        trial.params['p130'],
        trial.params['p210']
    ]
    total_weight = sum(best_weights)
    best_weights = [w / total_weight for w in best_weights]
    
    # Calculate the investment amounts
    unnormalized_investments = calculate_investment_amounts(df, best_weights)
    normalized_investments = normalize_investment_amounts(unnormalized_investments)
    
    # Calculate the investment amount for the current Sunday
    if df['Open Time'].iloc[-1].weekday() == 6:
        last_investment_amount = normalized_investments[-1]
        last_btc_price = df['Close'].iloc[-1]
        btc_to_buy = last_investment_amount / last_btc_price
        print(f"Investment amount for {df['Open Time'].iloc[-1]}: ${last_investment_amount:.2f}")
        print(f"BTC to buy: {btc_to_buy:.6f} BTC")

if __name__ == "__main__":
    run_simulation()