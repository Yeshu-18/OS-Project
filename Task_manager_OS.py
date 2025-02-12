import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots

class Process:
    def __init__(self, pid, burst_time):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.turnaround_time = 0

class TaskSchedulerApp:
    def __init__(self, master):
        self.master = master
        master.title("Task Scheduler")
        self.tasks = []
        self.fig_combined = None  # Store combined figure as a class attribute

        self.create_widgets()

    def create_widgets(self):
        self.entry_pid = tk.Entry(self.master, width=10)
        self.entry_burst_time = tk.Entry(self.master, width=10)
        self.entry_quantum = tk.Entry(self.master, width=10)

        self.btn_add_task = tk.Button(self.master, text="Add Task", command=self.add_task, bg="green", fg="white")
        self.btn_run_scheduler = tk.Button(self.master, text="Run Scheduler", command=self.run_scheduler, bg="blue", fg="white")

        self.text_output = scrolledtext.ScrolledText(self.master, width=40, height=10)

        self.entry_pid.grid(row=0, column=0)
        self.entry_burst_time.grid(row=0, column=1)
        self.entry_quantum.grid(row=0, column=2)
        self.btn_add_task.grid(row=1, column=0, columnspan=3)
        self.btn_run_scheduler.grid(row=2, column=0, columnspan=3)
        self.text_output.grid(row=3, column=0, columnspan=3, rowspan=2)

        self.tree = ttk.Treeview(self.master, columns=('PID', 'Burst Time', 'Turnaround Time'))
        self.tree.grid(row=3, column=3, columnspan=2, rowspan=2)
        self.tree.heading('#0', text='Task ID')
        self.tree.heading('PID', text='PID')
        self.tree.heading('Burst Time', text='Burst Time')
        self.tree.heading('Turnaround Time', text='Turnaround Time')

    def add_task(self):
        pid = int(self.entry_pid.get())
        burst_time = int(self.entry_burst_time.get())
        task = Process(pid, burst_time)
        self.tasks.append(task)

    def run_scheduler(self):
        quantum = int(self.entry_quantum.get())
        self.text_output.delete(1.0, tk.END)  # Clear previous output

        completed_tasks = 0
        current_time = 0

        while completed_tasks < len(self.tasks):
            for task in self.tasks:
                if task.remaining_time > 0:
                    execution_time = min(task.remaining_time, quantum)
                    task.remaining_time -= execution_time
                    current_time += execution_time

                    if task.remaining_time <= 0:
                        completed_tasks += 1
                        task.turnaround_time = current_time

                        self.tree.insert('', 'end', text=f'Task {task.pid}', values=(task.pid, task.burst_time, task.turnaround_time))

                        output = f"Task {task.pid} has completed. Turnaround Time: {task.turnaround_time}\n"
                        self.text_output.insert(tk.END, output)

        self.display_task_charts()

    def display_task_charts(self):
        burst_times = [task.burst_time for task in self.tasks]
        turnaround_times = [task.turnaround_time for task in self.tasks]

        fig_combined = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                                     subplot_titles=('Burst Time Comparison', 'Turnaround Time Comparison'))

        fig_combined.add_trace(go.Pie(labels=[f'Task {task.pid}' for task in self.tasks], values=burst_times, name='Burst Time'),
                               1, 1)
        fig_combined.add_trace(go.Pie(labels=[f'Task {task.pid}' for task in self.tasks], values=turnaround_times, name='Turnaround Time'),
                               1, 2)

        fig_combined.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig_combined.update_layout(title_text='Task Metrics Comparison')

        self.fig_combined = fig_combined

        # Save the plot to an HTML file and open it in a browser
        pyo.plot(fig_combined, filename='combined_task_metrics.html', auto_open=True)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskSchedulerApp(root)
    root.mainloop()
