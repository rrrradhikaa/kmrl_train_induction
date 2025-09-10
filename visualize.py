import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_efficiency_over_time():
    hours = [0, 6, 12, 18]
    efficiency = [60, 75, 90, 82]
    plt.plot(hours, efficiency, marker='o')
    plt.title("Efficiency vs Time")
    plt.xlabel("Hour of Day")
    plt.ylabel("Efficiency (%)")
    plt.grid(True)
    plt.savefig("data/efficiency_vs_time.png")
    plt.show()

def plot_resource_utilization():
    resources = ['CPU', 'Memory', 'DB']
    utilization = [88, 80, 91]

    colors = ['red' if val > 85 else 'green' for val in utilization]
    plt.bar(resources, utilization, color=colors)
    plt.title("Resource Utilization")
    plt.ylabel("Usage (%)")
    plt.axhline(y=85, color='gray', linestyle='--', label='CPU Threshold')
    plt.axhline(y=80, color='blue', linestyle='--', label='Memory Threshold')
    plt.axhline(y=90, color='orange', linestyle='--', label='DB Threshold')
    plt.legend()
    plt.savefig("data/resource_utilization.png")
    plt.show()

def plot_job_execution_times():
    job_types = ['High Priority API', 'Medium Task', 'Batch Job', 'Background Sync']
    times = [120, 450, 1500, 2100]

    sns.barplot(x=job_types, y=times)
    plt.ylabel("Avg Execution Time (ms)")
    plt.xticks(rotation=30)
    plt.title("Job Execution Time by Type")
    plt.tight_layout()
    plt.savefig("data/job_execution_time.png")
    plt.show()

if __name__ == "__main__":
    plot_efficiency_over_time()
    plot_resource_utilization()
    plot_job_execution_times()
