import matplotlib.pyplot as plt


def plot_retrieval_tradeoff(summary, save_path="results/tradeoff.png"):
    models = list(summary.keys())

    recall = [summary[m]["recall"] for m in models]
    latency = [summary[m]["latency"] for m in models]

    plt.figure()

    plt.scatter(latency, recall)

    for i, m in enumerate(models):
        plt.annotate(m, (latency[i], recall[i]))

    plt.xlabel("Latency (s)")
    plt.ylabel("Recall@5")
    plt.title("Retrieval Tradeoff: Recall vs Latency")

    plt.savefig(save_path)
    plt.close()


def plot_failure_distribution(df, save_path="results/failures.png"):
    dist = df["category"].value_counts()

    plt.figure()
    dist.plot(kind="bar")

    plt.title("Failure Distribution by Query Type")
    plt.ylabel("Count")

    plt.savefig(save_path)
    plt.close()