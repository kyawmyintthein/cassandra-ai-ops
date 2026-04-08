# Cassandra AI Ops Solution Design v1.0.0

## 1. Purpose

This document defines version `1.0.0` of the MVP solution design for an AI-based investigation system focused on Cassandra and application environments.

The goal of this version is not to build a fully autonomous root cause analysis platform. The goal is to provide a transparent investigation assistant that:

- accepts an incident symptom from observability systems or users
- investigates application and Cassandra signals in a controlled sequence
- explains what it is doing at each step
- shows the current reasoning and next step
- produces evidence-backed causal hypotheses

This design intentionally favors transparency, repeatability, and operator trust over full autonomy.

## 2. Design Principles

- `Transparent by default`: the system must continuously explain the current step, reasoning, and next step
- `Evidence before conclusion`: hypotheses must be backed by collected observations
- `Human-in-the-loop`: operators should be able to follow and validate the investigation path
- `Deterministic workflow`: the orchestrator should follow a controlled sequence rather than unconstrained multi-agent behavior
- `Read-only MVP`: version `1.0.0` collects and analyzes data only; it does not execute remediation
- `Domain-aware analysis`: Cassandra investigation must consider topology, schema, and configuration context

## 3. Scope

### In Scope

- symptom-driven incident investigation
- application metric and log collection
- Cassandra metric, log, topology, schema, and configuration collection
- static service dependency graph
- ranked causal hypotheses
- live investigation progress updates

### Out of Scope

- automated remediation
- write operations against infrastructure or databases
- dynamic service graph discovery
- broad multi-cluster or multi-region orchestration
- long-term learning loops and automatic tuning

## 4. Problem Statement

When a symptom is detected, such as application latency increasing from `200ms` to `400ms`, operators need fast and trustworthy guidance on:

- what changed
- which components are likely involved
- whether Cassandra is a contributing factor
- what evidence supports the current theory
- what the next investigation step should be

Traditional dashboards provide signals but not investigation flow. This system fills that gap by guiding the user through an evidence-based causal investigation.

## 5. High-Level Architecture

The MVP consists of eight main components:

1. `Incident Intake`
2. `Context Builder`
3. `Orchestrator`
4. `Application Analyzer`
5. `Cassandra Analyzer`
6. `Hypothesis Engine`
7. `Explainer`
8. `Static Service Graph`

An optional supporting component is strongly recommended for implementation:

9. `Evidence Store`

For `v1.0.0`, a separate `Reporter` component is not required. Final reporting can be treated as one output mode of the `Explainer`, which keeps the MVP simpler while preserving clear operator communication.

## 6. Component Responsibilities

### 6.1 Incident Intake

The Incident Intake component receives the initial symptom from an observability platform, alerting system, or user input.

Example symptom:

> Application latency increased from `200ms` to `400ms` for service `checkout` in production.

Responsibilities:

- accept symptom input from external systems or users
- normalize the symptom into a standard incident format
- define the initial incident time window
- pass the normalized incident to the orchestrator

Example normalized incident fields:

- `incident_id`
- `service`
- `environment`
- `symptom_type`
- `metric_name`
- `baseline_value`
- `current_value`
- `start_time`
- `observation_window`
- `severity`
- `source`

### 6.2 Context Builder

The Context Builder enriches the incident before deeper investigation begins.

Responsibilities:

- map the incident to the affected service and environment
- identify dependent systems from the service graph
- determine whether Cassandra is in the likely investigation path
- define or refine the investigation time window
- attach useful environment and asset context to the incident
- optionally include recent change context if available

Typical context fields:

- `service`
- `environment`
- `dependencies`
- `cassandra_clusters`
- `time_window`
- `recent_deployments`
- `recent_config_changes`
- `topology_context_refs`

This component improves investigation quality by making sure analyzers and the orchestrator start with the right context rather than raw symptoms alone.

### 6.3 Orchestrator

The Orchestrator is the central workflow controller.

Unlike a traditional agent that silently reasons and only returns a final report, the Orchestrator in `v1.0.0` acts as a transparent investigation guide. It must continuously tell the user:

- the current step
- why the step matters
- what it found
- the current reasoning
- the next step
- why the next step is needed

Responsibilities:

- receive the normalized incident
- build and maintain investigation state
- decide which analyzer or tool to call next
- correlate evidence across application and Cassandra layers
- maintain and rank active hypotheses
- publish progress updates to the user throughout the investigation

The Orchestrator should behave like a controlled state machine with reasoning summaries, not as an unconstrained autonomous planner.

### 6.4 Application Analyzer

The Application Analyzer is responsible for collecting and interpreting application-side telemetry.

Responsibilities:

- collect application metrics for the incident window
- collect relevant application logs
- identify latency, error, throughput, and saturation anomalies
- correlate symptoms with endpoint, service, or instance-level context
- return structured findings to the orchestrator

Typical data sources:

- request latency metrics
- error rates
- throughput metrics
- thread pool metrics
- connection pool metrics
- container or service logs
- deployment metadata if available

### 6.5 Cassandra Analyzer

The Cassandra Analyzer is responsible for collecting and interpreting Cassandra-specific telemetry and metadata.

Responsibilities:

- collect Cassandra metrics and logs for the incident window
- understand cluster topology and node relationships
- capture schema and key configuration context
- identify database-side anomalies that may explain the symptom
- return structured findings to the orchestrator

This component must be topology-aware. In Cassandra, the meaning of performance symptoms depends on:

- data center layout
- rack topology
- token ownership
- replication factor
- node membership and health
- schema design
- consistency behavior
- compaction and repair activity

Typical Cassandra signals for MVP:

- read latency
- write latency
- pending tasks
- dropped messages
- compaction activity
- GC pause behavior
- disk pressure indicators
- repair or streaming events
- node up/down state
- keyspace and table metadata
- selected Cassandra configuration values

### 6.6 Hypothesis Engine

The Hypothesis Engine manages candidate causes during the investigation.

Responsibilities:

- generate candidate hypotheses from collected evidence
- rank competing explanations
- track supporting and contradicting evidence
- update confidence as new observations arrive
- propose the next best validation step for each major hypothesis

This component should maintain a ranked list of candidate causes rather than forcing the orchestrator to jump to a single early conclusion.

### 6.7 Explainer

The Explainer converts internal investigation state into user-facing progress updates.

Responsibilities:

- describe the current step in clear language
- explain why the step matters
- summarize findings collected so far
- present the current reasoning in concise form
- describe the next step and why it is next
- produce the final investigation summary when the workflow completes

For `v1.0.0`, the final reporting function can be handled by this component instead of introducing a separate `Reporter`.

### 6.8 Static Service Graph

The Static Service Graph provides dependency context for the investigation.

For `v1.0.0`, this graph may be managed as static configuration.

Responsibilities:

- map application services to their dependencies
- identify which services depend on Cassandra
- provide upstream and downstream context to the orchestrator
- narrow the investigation path when a symptom occurs

The graph is not itself a reasoning engine. It is a dependency context provider.

### 6.9 Evidence Store

The Evidence Store is optional for a minimal prototype but recommended for practical implementation.

Responsibilities:

- store collected observations
- store investigation steps and tool outputs
- store active and rejected hypotheses
- preserve the evidence trail for later review

This component improves traceability, debugging, and trust.

## 7. Investigation Model

### 7.1 Core Idea

The system does not jump directly from symptom to root cause. It moves through a sequence of evidence-gathering and hypothesis-ranking steps.

The Orchestrator continuously updates the user with:

- what is happening now
- why it is happening
- what was learned
- what comes next

### 7.2 Investigation Stages

The default `v1.0.0` investigation flow is:

1. `Incident intake and normalization`
2. `Context enrichment`
3. `Application-side analysis`
4. `Cassandra-side analysis`
5. `Cross-layer correlation`
6. `Hypothesis generation and ranking`
7. `User-facing explanation and guidance`
8. `Recommendation and investigation summary`

The important change from a traditional final-report-only model is that user-facing updates occur during each stage, not only at the end.

## 8. Orchestrator State Model

The Orchestrator should maintain a structured internal state.

Recommended fields:

- `incident`
- `context`
- `current_step`
- `completed_steps`
- `observations`
- `active_hypotheses`
- `rejected_hypotheses`
- `reasoning_summary`
- `next_step`
- `next_step_rationale`
- `confidence`
- `requested_tools`
- `evidence_refs`

This state enables both workflow control and explainability.

## 9. User-Facing Progress Updates

### 9.1 Requirement

The Orchestrator must provide live investigation updates instead of waiting until the final step to explain the result.

Each update should answer:

- `What are we doing now?`
- `Why are we doing it?`
- `What have we found so far?`
- `What do we think right now?`
- `What will we do next?`
- `Why is that the next best step?`

### 9.2 Suggested Update Schema

```json
{
  "current_step": "Analyze Cassandra health during the incident window",
  "why_this_step": "Application latency increased at the same time as database read latency, so we need to test whether Cassandra degradation is contributing to the symptom.",
  "findings": [
    "Application p95 latency rose from 200ms to 400ms",
    "Cassandra read latency increased on two nodes",
    "Application error rate remained stable"
  ],
  "current_reasoning": "The leading theory is that the latency spike is correlated with Cassandra node-level degradation rather than a broad application failure.",
  "next_step": "Inspect compaction, GC, and dropped messages on the affected Cassandra nodes.",
  "why_next": "These signals help distinguish between storage pressure, node instability, and workload-related issues.",
  "hypotheses": [
    {
      "name": "Node-level Cassandra degradation",
      "confidence": 0.68
    },
    {
      "name": "Hot partition or skewed workload",
      "confidence": 0.21
    },
    {
      "name": "Application regression",
      "confidence": 0.11
    }
  ]
}
```

### 9.3 Transparency Rule

The system should expose concise evidence-based rationale, not unrestricted hidden chain-of-thought. The explanation should be:

- concise
- actionable
- evidence-backed
- safe to show to operators

## 10. Hypothesis Model

The system should maintain a ranked list of candidate causes rather than a single early conclusion. In `v1.0.0`, this responsibility belongs to the `Hypothesis Engine`, while the `Orchestrator` uses those rankings to decide the next investigation step.

Each hypothesis should contain:

- `name`
- `description`
- `supporting_evidence`
- `contradicting_evidence`
- `confidence`
- `next_validation_step`

Example hypotheses:

- node-level Cassandra degradation
- compaction pressure
- hot partition
- application connection pool exhaustion
- recent deployment regression
- downstream dependency slowdown

## 11. Canonical Data Objects

To keep the MVP extensible, the system should define a small set of canonical objects.

Recommended objects:

- `Incident`
- `Observation`
- `Evidence`
- `Hypothesis`
- `InvestigationStep`
- `Asset`
- `TopologyContext`

These objects should be shared across all components so tools can evolve without changing the core orchestration model.

## 12. MVP Decision Logic

The Orchestrator should follow deterministic investigation rules where possible.

Example logic:

- if the symptom is application latency, first confirm whether the impact is isolated or correlated with Cassandra
- if Cassandra metrics correlate with the incident window, prioritize Cassandra analysis
- if only a subset of nodes show degradation, prioritize topology-aware node investigation
- if application errors increase without Cassandra correlation, prioritize application-side analysis
- if evidence is weak or contradictory, reduce confidence and request the next most valuable signal

This approach is better for `v1.0.0` than fully free-form agent debate.

## 13. Guardrails

The following guardrails should be built into version `1.0.0`:

- `Read-only access only`
- `Time-bounded investigations`
- `Fixed investigation window`
- `Evidence citation for each conclusion`
- `Confidence scoring for hypotheses`
- `Explicit unknown state when evidence is insufficient`
- `No automatic remediation`

These guardrails reduce risk and improve trust.

## 14. Supported MVP Use Cases

Version `1.0.0` should focus on a narrow set of investigation scenarios:

- application latency spike
- application error spike
- Cassandra read latency spike
- Cassandra write latency spike
- Cassandra node degradation

Recommended initial deployment boundary:

- one application domain
- one Cassandra cluster
- one production environment
- one static service graph definition

## 15. Example End-to-End Flow

1. Incident Intake receives:
   `checkout service p95 latency increased from 200ms to 400ms`
2. Orchestrator normalizes the incident and sets the investigation window
3. Static Service Graph shows that `checkout` depends on Cassandra
4. Application Analyzer checks latency, error rate, throughput, and logs
5. Orchestrator reports the current findings and explains why Cassandra analysis is next
6. Cassandra Analyzer checks topology, node health, read latency, compaction, and GC
7. Orchestrator correlates application and Cassandra evidence
8. Hypotheses are ranked and updated
9. Orchestrator presents the current likely cause, confidence, evidence, and next recommended action

## 16. Non-Functional Expectations

The system should aim for:

- clear and readable operator updates
- repeatable investigation paths
- auditable evidence trails
- low-risk read-only execution
- modular analyzers that can be extended later

## 17. Future Enhancements Beyond v1.0.0

The following can be added after the MVP:

- dynamic service graph discovery
- change event ingestion for deployments and schema changes
- stronger causal ranking models
- automated incident timeline generation
- multi-cluster and multi-region support
- remediation recommendation playbooks
- controlled remediation execution with approval

## 18. Summary

Version `1.0.0` defines a transparent AI-assisted investigation system for Cassandra and application environments.

The central design choice is that the Orchestrator does not operate as a hidden black box that only returns a final report. Working with the `Context Builder`, `Hypothesis Engine`, and `Explainer`, it continuously guides the user through the investigation by showing:

- the current step
- the reasoning behind it
- the findings so far
- the next step
- why that next step is valuable

This makes the system more trustworthy, easier to validate, and more practical for real incident investigation workflows.
