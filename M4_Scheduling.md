# 📅 Scheduling Rules & Performance Visuals – Dry Run Demo

This document contains all finalized scheduling logic and performance metrics required for the dry run.

---

## 🔧 Scheduling Rules

### 1. Job Prioritization Rules

| Priority Level | Condition                                        | Example                         |
|----------------|--------------------------------------------------|---------------------------------|
| High           | Deadline < 24h OR client = “Premium”             | Urgent maintenance task         |
| Medium         | Deadline between 24h – 72h                       | Routine task                    |
| Low            | Deadline > 72h, non-blocking                     | Background data sync            |

> Execute high-priority jobs first. Use FIFO within the same level.

---

### 2. Time-Slot Based Scheduling

| Time Slot       | Rule                                               |
|------------------|----------------------------------------------------|
| 12am – 6am       | Run batch jobs and large data syncs (non-urgent)   |
| 6am – 10am       | Prioritize fast-response jobs (APIs)               |
| 10am – 6pm       | Client jobs, scheduled tasks                       |
| 6pm – 12am       | Deferred and monitoring-related jobs               |

---

### 3. Resource Utilization Thresholds

| Resource        | Threshold        | Action if Exceeded                      |
|----------------|------------------|-----------------------------------------|
| CPU Usage       | > 85%            | Pause low-priority jobs                 |
| Memory Usage    | > 80%            | Trigger garbage collection & alerts     |
| DB Connections  | > 90% of limit   | Queue incoming writes                   |

---

### 4. Retry and Fallback Logic

| Scenario                        | Retry Count | Delay (Backoff) | Fallback                  |
|--------------------------------|-------------|-----------------|---------------------------|
| Temporary DB failure           | 3           | 1s, 2s, 4s       | Retry later window        |
| API timeout                    | 2           | 2s, 5s           | Notify + log              |
| CPU > 90%                      | 0           | —               | Defer job                 |

---

### 5. Optimization Rules (AI/ML Assisted)

| Feature                  | Optimization Logic                                            |
|--------------------------|---------------------------------------------------------------|
| Predictive Scheduling    | Use historical data to pre-allocate time slots                |
| Load Balancing           | Distribute jobs based on predicted load                       |
| Job Batching             | Combine similar jobs to reduce overhead                       |

---

## 📊 Performance Visuals (Charts)

You can either generate these charts or just describe them here for now.

---

### 🔹 Efficiency vs Time


Hour 0 ➝ Efficiency: 60%
Hour 6 ➝ Efficiency: 75%
Hour 12 ➝ Efficiency: 90%
Hour 18 ➝ Efficiency: 82%


---

### 🔹 Resource Utilization

CPU: 45% ➝ 88% → Pause low-priority jobs
Memory: 40% ➝ 80% → Trigger GC
DB: 30% ➝ 91% → Queue Writes


---

### 🔹 Job Execution Time

| Job Type          | Avg Time (ms) |
|-------------------|---------------|
| High Priority API | 120           |
| Medium Task       | 450           |
| Batch Job         | 1500          |
| Background Sync   | 2100          |

---

## ✅ Summary

This file includes:

- All scheduling rules (priority, resource usage, retries)
- Performance indicators
- Charts in text format (or can be visualized later)




