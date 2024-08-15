import os
import pandas as pd
import matplotlib.pyplot as plt
import optuna
from fetch_btc_data import fetch_btc_data

def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=['Open Time', 'Close Time'])

def calculate_mav(df, windows=[10, 20, 30, 50, 80, 130, 210]):
    for window in windows:
        df[f'MAV_{window}'] = df['Close'].rolling(window=window).mean()
    df.dropna(inplace=True)
    return df

def calculate_investment_amounts(df, weights):
    investment_amounts = []
    for i in range(len(df)):
        if df['Open Time'].iloc[i].weekday() == 6:  # Check if it's Sunday
            mav_10 = (df['MAV_10'].iloc[i] - df['Close'].iloc[i])/ df['Close'].iloc[i]
            mav_20 = (df['MAV_20'].iloc[i] - df['Close'].iloc[i])/ df['Close'].iloc[i]
            mav_30 = (df['MAV_30'].iloc[i] - df['Close'].iloc[i])/ df['Close'].iloc[i]
            mav_50 = (df['MAV_50'].iloc[i] - df['Close'].iloc[i])/ df['Close'].iloc[i]
            mav_80 = (df['MAV_80'].iloc[i] - df['Close'].iloc[i])/ df['Close'].iloc[i]
            mav_130 = (df['MAV_130'].iloc[i] - df['Close'].iloc[i])/ df['Close'].iloc[i]
            mav_210 = (df['MAV_210'].iloc[i] - df['Close'].iloc[i])/ df['Close'].iloc[i]
            
            p10, p20, p30, p50, p80, p130, p210 = weights
            total_investment = (p10 * mav_10 + p20 * mav_20 + p30 * mav_30 +
                                p50 * mav_50 + p80 * mav_80 + p130 * mav_130 + p210 * mav_210)
            investment_amounts.append(total_investment)
    return investment_amounts

def normalize_investment_amounts(investment_amounts):
    min_investment = min(investment_amounts)
    max_investment = max(investment_amounts)
    normalized_investments = [
    (amount - min_investment) * (50 / (max_investment - min_investment))
    for amount in investment_amounts
    ]
    return normalized_investments

def simulate_investment(df, weights=(1, 1, 1, 1, 1, 1, 1)):
    investment_dates = []
    investment_amounts = []
    wallet_value = []
    total_invested = 0
    btc_wallet = 0

    unnormalized_investments = calculate_investment_amounts(df, weights)
    normalized_investments = normalize_investment_amounts(unnormalized_investments)

    investment_index = 0
    for i in range(len(df)):
        if df['Open Time'].iloc[i].weekday() == 6:  # Check if it's Sunday
            investment_amount = normalized_investments[investment_index]
            investment_index += 1
            total_invested += investment_amount
            btc_wallet += investment_amount / df['Close'].iloc[i]
            investment_dates.append(df['Open Time'].iloc[i])
            investment_amounts.append(total_invested)
            wallet_value.append(btc_wallet * df['Close'].iloc[i])

    return investment_dates, investment_amounts, wallet_value, normalized_investments

def plot_investment(investment_dates, investment_amounts, wallet_value, weights):
    plt.figure(figsize=(14, 7))
    plt.plot(investment_dates, investment_amounts, label='Total Invested ($)')
    plt.plot(investment_dates, wallet_value, label='Wallet Value ($)')
    plt.xlabel('Date')
    plt.ylabel('Value ($)')
    plt.title(f'Investment Simulation with Weights {weights}')
    plt.legend()
    plt.grid(True)
    
    # Create images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # Save the plot
    plt.savefig(f'images/investment_simulation_{investment_dates[-1].strftime('%Y-%m-%d')}.png')
    plt.close()

def print_final_simulation_results(investment_amounts, wallet_value):
    if investment_amounts and wallet_value:
        profit = wallet_value[-1] - investment_amounts[-1]
        print(f"Total Invested: ${investment_amounts[-1]:.2f}, Wallet Value: ${wallet_value[-1]:.2f}, Profit: ${profit:.2f}")

def save_investment_to_csv(investment_dates, normalized_investments):
    data = {
        'Date': investment_dates,
        'Investment ($)': normalized_investments
    }
    df = pd.DataFrame(data)
    df.to_csv(f'investment_simulation_weights_{investment_dates[-1].strftime('%Y-%m-%d')}.csv', index=False)
    print(f"Investment data saved to investment_simulation_weights_{investment_dates[-1].strftime('%Y-%m-%d')}.csv")

def objective(trial):
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

if __name__ == "__main__":
    fetch_btc_data()
    df = load_data('btc_data.csv')
    df = calculate_mav(df)
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100)
    
    print("Best trial:")
    trial = study.best_trial
    print(f"  Value: {trial.value}")
    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")
    
    # Plot the best investment simulation
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
    
    investment_dates, investment_amounts, wallet_value, normalized_investments = simulate_investment(df, weights=best_weights)
    plot_investment(investment_dates, investment_amounts, wallet_value, best_weights)
    save_investment_to_csv(investment_dates, normalized_investments)
    print("Results for Best Weights:")
    print_final_simulation_results(investment_amounts, wallet_value)
    print("\n" + "="*50 + "\n")