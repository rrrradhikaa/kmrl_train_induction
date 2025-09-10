import pandas as pd
from utils import categorize_priority, categorize_time_slot, simulate_resources, apply_retry_logic

def load_jobs(file_path='data/job_data.csv'):
    return pd.read_csv(file_path)

def apply_scheduling(df):
    df['priority'] = df.apply(lambda x: categorize_priority(x['deadline_hours'], x['client']), axis=1)
    df['time_slot'] = df['scheduled_time'].apply(categorize_time_slot)

    # Sort by priority & FIFO
    df['priority_rank'] = df['priority'].map({'High': 1, 'Medium': 2, 'Low': 3})
    df.sort_values(by=['priority_rank', 'scheduled_time'], inplace=True)

    return df.reset_index(drop=True)

def execute_jobs(df):
    logs = []
    for _, row in df.iterrows():
        resource_status = simulate_resources()
        if resource_status['CPU'] > 85 and row['priority'] != 'High':
            logs.append((row['job_id'], 'Paused due to CPU > 85%'))
            continue
        if resource_status['Memory'] > 80:
            logs.append((row['job_id'], 'Triggered GC - Memory > 80%'))
        if resource_status['DB'] > 90:
            logs.append((row['job_id'], 'Queued due to DB > 90%'))

        retry_result = apply_retry_logic(row['job_type'], resource_status)
        logs.append((row['job_id'], retry_result))

    return logs

if __name__ == "__main__":
    df = load_jobs()
    scheduled_df = apply_scheduling(df)
    print("\n🔄 Scheduled Jobs:")
    print(scheduled_df[['job_id', 'priority', 'time_slot']])

    print("\n⚙️ Execution Log:")
    execution_log = execute_jobs(scheduled_df)
    for log in execution_log:
        print(f"{log[0]} ➝ {log[1]}")

    scheduled_df.to_csv("data/scheduled_jobs_output.csv", index=False)
