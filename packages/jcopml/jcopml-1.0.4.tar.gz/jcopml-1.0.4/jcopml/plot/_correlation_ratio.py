import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_correlation_ratio(df, target_col, numvar, report=False):
    """
    Correlation Ratio heatmap
    https://en.wikipedia.org/wiki/Correlation_ratio
    """
    df_corr = df.copy()

    group_count = df_corr.groupby(target_col).count()[numvar]
    group_mean = df_corr.groupby(target_col).mean()[numvar]

    total_mean = (group_mean * group_count).sum()
    total_mean = total_mean.divide((group_count).sum())

    std_cat = (group_count * (group_mean - total_mean) ** 2).sum()
    std_num = ((df_corr[numvar] - total_mean) ** 2).sum()
    eta = std_cat / (std_num + 1e-8)

    sns.heatmap(pd.DataFrame(eta, columns=[target_col]), cmap="bwr", vmin=-1, vmax=1, square=True, annot=True,
                fmt=".1f", cbar=False, linewidths=1, linecolor='k')
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.title(f"Correlation Ratio", fontsize=14)

    if report:
        return eta

