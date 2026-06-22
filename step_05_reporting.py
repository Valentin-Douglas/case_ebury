from matplotlib import pyplot as plt
import seaborn as sns
import os

def generate_reporting(transactions_per_partner, min_exchange_rate, max_exchange_rate, trades_per_day, foreign_gross_amount_per_currency, avg_capping_rate_per_currency):
    # Create reports directory if it doesn't exist
    if not os.path.exists('./msc/reports'):
        os.makedirs('./msc/reports')
    
    sns.set(style="whitegrid")

    # COLOR PALETTE
    # Define a color palette for the plots
    currencies = sorted(foreign_gross_amount_per_currency.index.tolist())
    currency_colors = dict(zip(currencies, sns.color_palette("husl", len(currencies))))
    
    partners = sorted(transactions_per_partner.index.tolist())
    partner_colors = dict(zip(partners, sns.color_palette("Set2", len(partners))))

    dates = sorted(trades_per_day.index.tolist())
    date_colors = dict(zip(dates, sns.color_palette("YlGnBu", len(dates))))

    # 1. Count the number of transactions from each partner.
    plt.figure(figsize=(10, 6))
    ax1 = sns.barplot(
        x=transactions_per_partner.index, 
        y=transactions_per_partner.values, 
        hue=transactions_per_partner.index,
        palette=partner_colors,
        legend=False
    )
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%d', padding=3)
    plt.title('Number of Transactions per Partner')
    plt.xlabel('Partner Name')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./msc/reports/transactions_per_partner.png')
    plt.close()

    # 2. Calculate the minimum and the maximum exchangeRate.
    plt.figure(figsize=(10, 6))
    metrics = ['Minimum', 'Maximum']
    values = [min_exchange_rate, max_exchange_rate]
    ax2 = sns.barplot(
        x=metrics, 
        y=values, 
        hue=metrics, 
        palette={'Minimum': '#d62728', 'Maximum': '#2ca02c'}, 
        legend=False
    )
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%.8f', padding=3)
    plt.title('Minimum and Maximum Exchange Rate')
    plt.xlabel('Metrics')
    plt.ylabel('Exchange Rate')
    plt.tight_layout()
    plt.savefig('./msc/reports/min_max_exchange_rate.png')
    plt.close()

    # 3. Determine the number of trades per day.
    plt.figure(figsize=(10, 6))
    ax3 = sns.barplot(
        x=trades_per_day.index, 
        y=trades_per_day.values, 
        hue=trades_per_day.index, 
        palette=date_colors, 
        legend=False
    )
    for container in ax3.containers:
        ax3.bar_label(container, fmt='%d', padding=3)
    plt.title('Number of Trades per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Trades')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./msc/reports/trades_per_day.png')
    plt.close()


    # 4. Determine the foreignGrossAmount per currency
    plt.figure(figsize=(10, 6))
    ax4 = sns.barplot(
        x=foreign_gross_amount_per_currency.index, 
        y=foreign_gross_amount_per_currency.values, 
        hue=foreign_gross_amount_per_currency.index, 
        palette=currency_colors, 
        legend=False
    )
    for container in ax4.containers:
        ax4.bar_label(container, fmt='%.2f', padding=3)
    plt.title('Foreign Gross Amount per Currency')
    plt.xlabel('Currency Code')
    plt.ylabel('Foreign Gross Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./msc/reports/foreign_gross_amount_per_currency.png')
    plt.close()

    # 5. Determine the average cappingRate per currency
    plt.figure(figsize=(10, 6))
    ax5 = sns.barplot(
        x=avg_capping_rate_per_currency.index, 
        y=avg_capping_rate_per_currency.values, 
        hue=avg_capping_rate_per_currency.index, 
        palette=currency_colors, 
        legend=False
    )
    for container in ax5.containers:
        ax5.bar_label(container, fmt='%.8f', padding=3)
    plt.title('Average Capping Rate per Currency')
    plt.xlabel('Currency Code')
    plt.ylabel('Average Capping Rate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./msc/reports/avg_capping_rate_per_currency.png')
    plt.close()

    return None