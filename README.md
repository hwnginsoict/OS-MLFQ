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
- Summary of average waiting time.

## How to Run

Follow these steps to set up and run the application:

### 1. Install Streamlit

Open your terminal:

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
