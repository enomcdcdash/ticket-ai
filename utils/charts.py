import matplotlib.pyplot as plt


# =========================================
# REGIONAL BAR CHART
# =========================================
def create_bar_chart(data, title="Chart"):

    fig, ax = plt.subplots(figsize=(10, 5))

    data.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(title)

    plt.xticks(rotation=45)

    return fig