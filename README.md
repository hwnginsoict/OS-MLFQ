# OS-Project: Multilevel Feedback Queue Scheduling

This project implements a simulation of the **Multilevel Feedback Queue (MLFQ)** scheduling algorithm using Python and Streamlit. It provides an interactive interface for users to input processes and observe how MLFQ handles scheduling based on queue levels, time quanta, and dynamic priorities.

## Contributors

- **Phan Duc Hung** — 20214903  
- **Bui Doan Khang** — 20235950  
- **Ngo Duc Huy** — 20235946  

## Features

- Web-based UI for inputting process data  
- Simulation of MLFQ with customizable parameters  
- Real-time visualization of the scheduling sequence  
- Gantt chart output  
- Summary of process metrics (waiting time, turnaround time, etc.)

## How to Run

Follow these steps to set up and run the application:

### 1. Install Streamlit

If you're using Jupyter/Colab:

```bash
!pip install streamlit
```

Or from your terminal:

```bash
pip install streamlit
```

### 2. Navigate to the Project Directory

```bash
cd OS-MLFQ/code
```

### 3. Run the Streamlit App

```bash
streamlit run main.py
```

This will open the app in your default browser at `http://localhost:8501/`.

## Example Output

> *(You can include a screenshot of the Streamlit interface or Gantt chart here)*

## License

This project was developed for educational purposes as part of the *Parallel and Distributed Programming* course. You are welcome to reuse or adapt it with appropriate credit.
