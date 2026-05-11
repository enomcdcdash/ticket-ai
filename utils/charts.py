import matplotlib.pyplot as plt

# =========================================
# CREATE BAR CHART
# =========================================
def create_bar_chart(data):

    fig, ax = plt.subplots()

    data.plot(
        kind="bar",
        ax=ax
    )

    plt.xticks(rotation=45)

    return fig