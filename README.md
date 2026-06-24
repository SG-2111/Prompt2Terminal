<div align="center">

# ⚡ Prompt2Terminal

### Agentic AI-Powered Terminal Auto Pilot

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-FF6B35?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

> **Transform natural language objectives into safe, structured, and fully auditable terminal workflows — powered by multi-agent AI.**

[Overview](#-overview) · [Architecture](#-system-architecture) · [Agents](#-agent-design) · [Features](#-key-features) · [Installation](#-installation) · [Usage](#-usage) · [Safety](#-safety--security) · [Roadmap](#-future-enhancements)

---

</div>

## 📋 Abstract

**Prompt2Terminal** is an Agentic AI system that bridges the cognitive gap between high-level developer intent and low-level terminal command execution. By accepting natural language objectives as input, the system autonomously constructs structured command-line workflows, applies multi-layer safety validation, executes or simulates the resulting operations, and synthesises detailed execution reports.

Built on a pipeline of specialised AI agents — **Planner**, **Safety**, and **Report** — orchestrated by a LangGraph-managed state machine and powered by Google Gemini, Prompt2Terminal eliminates the friction of manual CLI interaction while ensuring every automated operation is explainable, auditable, and reproducible.

---

## 🔍 Problem Statement

Modern software development demands engineers navigate an ever-expanding surface area of terminal operations. Each domain requires precise command syntax, contextual awareness, and an understanding of potential side effects — cognitive burdens that compound across a development session.

| Challenge | Impact |
|-----------|--------|
| 🧠 **Cognitive Load** | Developers must recall precise syntax across dozens of tools, flags, and configurations |
| ❌ **Manual Error Propagation** | Typos, incorrect flags, and misordered sequences introduce hard-to-diagnose defects |
| 🔍 **Lack of Explainability** | Shell scripts execute without human-readable rationale, making audit and maintenance difficult |
| ⚠️ **Unsafe Automation** | Ad-hoc scripts may include destructive operations without prior safety review |
| ⏳ **Productivity Bottlenecks** | Repetitive boilerplate operations consume disproportionate developer time |

---

## 💡 Overview

Prompt2Terminal addresses these challenges through three foundational principles:

**1. Natural Language Interface** — Users express intent in plain English. The Planner Agent decomposes the objective into atomic, sequentially ordered command-line steps, eliminating the need for command-syntax recall.

**2. Agent-Based Safety Enforcement** — Every generated workflow passes through a dedicated Safety Agent before execution. Dangerous operations are detected and blocked with plain-language explanations and suggested safe alternatives.

**3. Auditable Execution and Reporting** — The Execution Layer logs all operations with timestamps and exit states. The Report Agent synthesises these logs into structured, human-readable reports with recommendations and anomaly flags.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER / CLI LAYER                         │
│          Natural Language Objective Input Interface             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LANGGRAPH ORCHESTRATOR                        │
│          Stateful Multi-Agent Workflow State Machine            │
└──────┬──────────────┬──────────────────┬────────────────────────┘
       │              │                  │
       ▼              ▼                  ▼
┌────────────┐  ┌──────────────┐  ┌──────────────────┐
│  PLANNER   │  │    SAFETY    │  │   REPORT AGENT   │
│   AGENT    │─▶│    AGENT     │  │                  │
│            │  │              │  │  Execution Logs  │
│ JSON Plan  │  │ APPROVED /   │  │  → Human Report  │
│ Generation │  │ BLOCKED      │  └──────────────────┘
└────────────┘  └──────┬───────┘
                        │  APPROVED
                        ▼
               ┌─────────────────┐
               │ EXECUTION LAYER │
               │                 │
               │  Live / Dry-Run │
               │  Subprocess Mgr │
               └─────────────────┘
```

### Pipeline Flow

```
User Prompt → Planner Agent → ExecutionPlan (JSON)
           → Safety Agent  → SafetyReport (APPROVED | BLOCKED)
           → Execution     → ExecutionLog (commands + outputs)
           → Report Agent  → FinalReport (human-readable)
```

---

## 🤖 Agent Design

### 🗺️ Planner Agent

Converts natural language objectives into structured, machine-executable workflows.

- Invokes Google Gemini with a structured prompt template
- Decomposes high-level goals into atomic, sequentially ordered steps
- Each step includes: command string, human-readable rationale, expected output, and dependency relationships
- Returns a fully validated **`ExecutionPlan`** Pydantic object

```json
{
  "goal": "Set up Python virtual environment",
  "steps": [
    {
      "id": 1,
      "command": "python -m venv env",
      "rationale": "Create isolated Python virtual environment",
      "expected_output": "env/ directory created",
      "depends_on": []
    },
    {
      "id": 2,
      "command": "pip install -r requirements.txt",
      "rationale": "Install project dependencies",
      "expected_output": "Packages installed successfully",
      "depends_on": [1]
    }
  ]
}
```

---

### 🛡️ Safety Agent

Evaluates every workflow before execution using multi-layer risk assessment.

- **Pattern Matching** — Blocklist of destructive command patterns (`rm -rf /`, `chmod 777 /`, `dd if=/dev/zero`, etc.)
- **LLM-Assisted Analysis** — Contextual risk inference for novel or obfuscated operations
- **Privilege Escalation Detection** — Flags `sudo`/root-level operations for explicit user confirmation
- Returns a **`SafetyReport`** with APPROVED / BLOCKED status and plain-language explanations

```
✅ APPROVED  — Workflow is safe to execute
❌ BLOCKED   — Dangerous operation detected: [explanation + safe alternative]
```

---

### ⚙️ LangGraph Orchestrator

Manages the entire multi-agent workflow as a typed state graph.

- Nodes correspond to agent invocations and the Execution Layer
- Conditional edges route based on agent outputs (e.g., APPROVED → Execute, BLOCKED → Halt)
- Maintains a shared **workflow context object** enriched at every stage
- Ensures deterministic, inspectable, and modifiable control flow

---

### 🚀 Execution Layer

Secure subprocess environment for live and simulated execution.

| Mode | Description |
|------|-------------|
| **Live Mode** | Commands dispatched to managed subprocess with timeout, output capture, and exit-code monitoring |
| **Simulation Mode** | Synthetic execution traces produced without modifying the host system — safe dry-run validation |

All operations logged to a structured **`ExecutionLog`**: command text, timestamps, stdout/stderr, exit codes, elapsed durations.

---

### 📊 Report Agent

Synthesises execution telemetry into actionable human-readable documentation.

- Consumes `ExecutionLog` and invokes Gemini for narrative synthesis
- Identifies anomalies, performance concerns, and highlights successful outcomes
- Provides forward-looking recommendations
- Outputs formatted for both terminal display and file export

---

## 🛠️ Technology Stack

| Technology | Role |
|-----------|------|
| **Python 3.10+** | Core language; agent orchestration, CLI interface, business logic |
| **Google Gemini API** | LLM backbone for NL understanding, planning, and report generation |
| **LangGraph** | Stateful multi-agent workflow orchestration via directed acyclic graph |
| **Pydantic** | Data validation and schema enforcement for all agent I/O |
| **Python Dotenv** | Secure environment variable management for API keys and config |
| **Git & GitHub** | Version control and repository analysis features |
| **CLI Interface** | Primary user interaction layer for prompt input and feedback display |

---

## ✨ Key Features

- 🗣️ **Natural Language to CLI Workflow Conversion** — Plain-English objectives → precise, ordered command sequences
- 🤖 **Agent-Based Decision Making** — Specialised agents handle planning, safety, execution, and reporting independently
- 📋 **Structured Workflow Planning** — JSON execution plans that are both machine-readable and human-inspectable
- 🛡️ **Multi-Layer Safety Validation** — Pattern-based and LLM-assisted checks prevent destructive command execution
- 💬 **Explainable AI Decisions** — Every planning and safety decision includes a plain-language rationale
- 📡 **Execution Monitoring** — Real-time tracking with stdout/stderr capture and timeout enforcement
- 📝 **Automated Reporting** — Post-execution reports with insights, anomaly flags, and recommendations
- 🔍 **GitHub Repository Analysis** — Context-aware planning adapted to a target repository's structure and toolchain
- ⚡ **Developer Productivity Enhancement** — Eliminates repetitive command construction and manual error correction

---

## 🔒 Safety & Security

Safety is a first-class concern in Prompt2Terminal's design.

### Blocklist Pattern Matching
A curated blocklist of dangerous command patterns is applied to every `ExecutionStep` before LLM analysis. Matches result in immediate `BLOCKED` status — no LLM invocation, minimal latency.

```
Blocked patterns include (not limited to):
  rm -rf /          → Recursive force-deletion of root
  chmod 777 /       → Universal permission assignment
  dd if=/dev/zero   → Device overwrite
  curl | bash       → Unverified remote code execution
```

### LLM-Assisted Contextual Risk Analysis
Commands passing the blocklist are submitted to Gemini for holistic risk assessment — catching semantically dangerous operations that may not match explicit patterns.

### Simulation Mode
All workflows can be executed in simulation mode, producing synthetic execution traces without touching the host system. Ideal for production-adjacent environments.

### Principle of Least Privilege
The Execution Layer operates without elevated privileges by default. Any `sudo` or root-level command triggers an explicit confirmation prompt and is flagged in the safety report.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/prompt2terminal.git
cd prompt2terminal

# Create and activate a virtual environment
python -m venv env
source env/bin/activate        # macOS / Linux
env\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

---

## 🚀 Usage

### Basic Usage

```bash
# Run with a natural language objective
python main.py "Set up a Python virtual environment and install dependencies"

# Dry-run / simulation mode
python main.py --simulate "Deploy the application to staging"

# Analyse a GitHub repository and generate a setup workflow
python main.py --repo https://github.com/user/repo "Set up local development environment"
```

### CLI Options

```
usage: main.py [-h] [--simulate] [--repo REPO] [--output OUTPUT] objective

positional arguments:
  objective          Natural language description of the goal to automate

optional arguments:
  -h, --help         Show this help message and exit
  --simulate         Run in simulation mode (no system changes)
  --repo REPO        GitHub repository URL for context-aware planning
  --output OUTPUT    Export execution report to file (default: terminal)
```

---

## 📋 Sample Workflow Execution

**Objective:** `"Set up a Python virtual environment and install dependencies from requirements.txt"`

| Step | Agent / Component | Action / Output |
|------|-------------------|-----------------|
| 1 | **User / CLI** | Submits natural language objective |
| 2 | **Planner Agent** | Decomposes goal → creates venv, activates, installs deps; generates JSON `ExecutionPlan` |
| 3 | **Safety Agent** | Validates each command — no destructive flags detected → `APPROVED` |
| 4 | **LangGraph Orchestrator** | Routes approved plan to Execution Layer; manages state transitions |
| 5 | **Execution Layer** | Runs: `python -m venv env` → `source env/bin/activate` → `pip install -r requirements.txt`; logs output |
| 6 | **Report Agent** | Generates success report with dependency stats, version warnings, and recommendations |

**Sample Report Output:**

```
╔══════════════════════════════════════════════════╗
║         PROMPT2TERMINAL EXECUTION REPORT         ║
╠══════════════════════════════════════════════════╣
║  Goal      : Set up Python virtual environment   ║
║  Status    : ✅ SUCCESS                          ║
║  Steps     : 3/3 completed                       ║
║  Duration  : 14.3s                               ║
╠══════════════════════════════════════════════════╣
║  RECOMMENDATIONS                                 ║
║  → Commit resolved requirements to version ctrl  ║
║  → Pin dependency versions for reproducibility   ║
╚══════════════════════════════════════════════════╝
```

---

## 🗂️ Project Structure

```
prompt2terminal/
├── agents/
│   ├── planner.py          # Planner Agent — workflow generation
│   ├── safety.py           # Safety Agent — risk assessment
│   └── report.py           # Report Agent — execution reporting
├── orchestrator/
│   └── graph.py            # LangGraph state graph definition
├── execution/
│   └── runner.py           # Subprocess management (live + simulate)
├── models/
│   └── schemas.py          # Pydantic data models
├── cli/
│   └── interface.py        # CLI entry-point and argument parsing
├── .env.example            # Environment variable template
├── requirements.txt
└── main.py                 # Application entry-point
```

---

## 🎯 Objectives

- ✅ Automate repetitive CLI operations through natural language intent
- ✅ Reduce manual command execution and associated human error
- ✅ Improve developer productivity by eliminating boilerplate interactions
- ✅ Provide safe and explainable AI-driven automation
- ✅ Generate comprehensive execution logs and human-readable reports

---

## 🔭 Future Enhancements

- 🐳 **Multi-Environment Support** — Docker, Podman, AWS CLI, gcloud, Azure CLI integration with environment-aware safety policies
- 💬 **Interactive Refinement Loop** — Conversational interface for iterative workflow refinement before execution
- 🧠 **Memory & Context Persistence** — Long-term agent memory for personalised, project-aware workflows
- 🔌 **IDE Plugin Integration** — VS Code and JetBrains extensions surfacing capabilities within the development environment
- 👥 **Team Collaboration Features** — Shared workflow libraries and team-level safety policy configuration
- 🎯 **Fine-Tuned Domain Models** — Task-specific LLM fine-tuning on verified terminal workflow datasets

---

## 🤝 Contributing

Contributions are welcome! Please open an issue to discuss your proposed change before submitting a pull request.

```bash
# Fork the repository, then:
git checkout -b feature/your-feature-name
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
# Open a Pull Request
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using Python · Google Gemini · LangGraph · Pydantic**

*Prompt2Terminal — Because your terminal should understand you.*

</div>
