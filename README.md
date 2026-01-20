# ai-career-agent

Config-driven AI agents for career automation (job search, learning, scheduling).

---

## Purpose

This project demonstrates a config-driven, extensible AI agent used to automate
local cybersecurity job discovery.

It is designed to showcase:
- clean agent architecture
- configuration-based behavior (no hardcoding)
- safe iteration before real integrations
- DevOps-friendly workflows (versioning, reproducibility, testing)

This repository is intentionally built as a portfolio project following
industry best practices.

---

## Features

- Config-driven job search agent
- Pluggable job sources via registry pattern
- CLI overrides for config and sources
- Distance-based filtering (radius in miles)
- Keyword and title relevance filtering
- Deduplication by job URL
- Deterministic JSON output for downstream agents
- Mock source for safe development and testing

---

## Architecture

```text
ai-career-agent/
├── agents/          # Agent entrypoints and orchestration
├── sources/         # Job sources (mock, indeed, monster, ziprecruiter)
├── models/          # Shared data models (Job)
├── config/          # YAML configuration
├── data/            # Generated outputs (ignored by git)
└── tests/           # Test scaffolding

## Why this project

This project is part of a larger effort to build autonomous agents that
work continuously in the background to support career development,
learning prioritization, and scheduling.

It reflects a DevOps-first, agent-oriented way of working.

## Run

### Install dependencies
python -m pip install -r requirements.txt

Run with default configuration:
python -m agents.local_job_agent --config config/config.yaml

Run with single surce (CLI override):
python -m agents.local_job_agent --sources mock

Output:
data/jobs.json
