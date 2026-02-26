Collective Intelligence Simulator
Modeling Human–AI Collaboration in Decision Systems
________________________________________
Overview
This project simulates how human decision-makers interact with AI systems in uncertain environments.
It studies a key question:
Does collaboration between humans and AI improve collective intelligence?
Using a multi-agent simulation, this project models:
•	Human decision biases
•	AI rational optimization
•	Dynamic trust adaptation
•	Social influence mechanisms
•	Emergent performance outcomes
________________________________________
Key Features
•	Multiple human personalities (Safe, Balanced, Risky)
•	AI agent with adjustable error rate
•	Dynamic trust evolution based on AI performance
•	Statistical comparison of:
o	Humans only
o	AI only
o	Humans + AI collaboration
•	Visualization:
o	Performance bar charts
o	Trust evolution over time
•	Automatic CSV export of simulation data
________________________________________
Core Concept
The system models a repeated decision game:
Option	Probability	Reward
A	70%	10
B	30%	50
•	Humans choose based on risk tolerance.
•	AI chooses based on expected value.
•	Humans may revise decisions after observing AI.
•	Trust increases or decreases depending on AI success.
This allows analysis of emergent collective intelligence dynamics.
________________________________________
Project Structure
collective-intelligence-simulator/
│
├── simulator.py
├── simulation_results.csv
├── requirements.txt
└── README.md
________________________________________
Installation
Clone the repository:
git clone https://github.com/jyotydivya844/Collective-Intelligence.git
cd collective-intelligence-simulator
Install dependencies:
pip install -r requirements.txt
________________________________________
Run the Simulation
python simulator.py
The program will:
•	Run 1000 simulation rounds
•	Print performance comparison
•	Display visualization graphs
•	Generate simulation_results.csv
________________________________________
Example Output
===== PERFORMANCE COMPARISON =====
Scenario             Avg Reward
-----------------------------------
Humans Only          7.32
AI Only              14.87
Humans + AI          10.41
Visual outputs include:
•	Collective Intelligence Comparison Bar Chart
•	Trust Evolution Over Time
## Visualization

### Performance Comparison
![Performance](images/performance.png)

### Trust Evolution
![Trust](images/trust.png)
________________________________________
Experimental Insights
This simulation enables experimentation with:
•	AI reliability (error rate adjustment)
•	Human diversity (risk tolerance variation)
•	Trust dynamics
•	Influence strength effects
•	Human-to-AI ratio scaling
It demonstrates how adaptive trust mechanisms impact collective decision performance.
________________________________________
Skills Demonstrated
•	Python programming
•	Multi-agent system design
•	Simulation modeling
•	Behavioral modeling
•	Statistical analysis
•	Data visualization (Matplotlib)
•	Synthetic dataset generation
•	Research-oriented experimentation
________________________________________
Future Improvements
•	Reinforcement Learning–based adaptive AI
•	Network-based influence graphs
•	Real human interaction interface (web application)
•	More complex decision environments
•	Performance benchmarking across agent ratios
________________________________________
Research Motivation
As AI systems increasingly collaborate with humans in domains such as:
•	Finance
•	Healthcare
•	Autonomous systems
•	Decision support systems
Understanding when AI enhances or harms collective intelligence becomes critical.
This project explores that question through controlled simulation experiments.
________________________________________
Author
Divya Jyoty

