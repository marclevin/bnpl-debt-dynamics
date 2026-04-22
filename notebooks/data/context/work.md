# ABM Design: Modelling BNPL Impact on South African Consumer Credit Market

## Story

We are modelling consumer behaviour in the South African consumer credit market, with a focus on the impact of Buy Now Pay Later (BNPL) platforms. The goal is to understand how BNPL affects consumer debt saturation and the potential for systemic default. We will create an Agent-Based Model (ABM) using Python's Mesa framework, defining three key agents: Consumers, Traditional Banks, and BNPL Platforms. Each agent will have specific attributes and behaviors that reflect real-world dynamics in the South African credit market.

## World

The simulation will exist in a simplified representation of the South African consumer credit market. The world will consist of a population of consumer agents, a set of traditional bank agents, and a set of BNPL platform agents. The interactions between these agents will be governed by rules that reflect real-world financial behaviors and regulatory environments.

We want our simulation to broadly use the concept of the balance sheet as the core engine and structure. We must be able to track the flow of money and debt across the system, and how it accumulates or dissipates over time. The "world" will be a dynamic environment where agents interact based on their financial states and the rules governing their behavior.

Our first step is to define the consumer, bank and world such that we could perform a retrospective analysis with our model to prove that it is aligned and calibrated.

Each agent will have a balance sheet.

### Consumer Agent

- Balance Sheet: Assets (Income, Savings) and Liabilities (Traditional Debt, BNPL Obligations)
- Receives income, pays expenses, and manages debt. Can fall into financial distress if liabilities exceed a certain threshold relative to income (e.g., DSTI > 50%).
- Can access unsecured, secured credit from banks, and BNPL credit from platforms. The consumer's ability to access credit will depend on their financial state and the rules of the respective agents.

### Traditional Bank Agent

- Balance Sheet: Assets (Loans Issued) and Liabilities (Deposits, Capital)
- Provides unsecured, and secured credit products, but operates under strict regulatory oversight (NCA). Cannot see BNPL obligations.

### BNPL Platform Agent

- Balance Sheet: Assets (Receivables from Consumers) and Liabilities (Capital, Operational Costs)

### World Engine

- The world will track the overall credit market, including total outstanding debt, default rates, and the growth of BNPL usage. It will also simulate economic shocks that can affect consumer income and spending behavior.

### Core Papers

We need at least three core papers to anchor our model design and calibration:

- ABM
- BNPL
- Behavioural Economics
