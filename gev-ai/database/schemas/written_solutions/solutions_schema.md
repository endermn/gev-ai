# Project Database Schema

This document outlines the database schema for the project, illustrating the relationship between `issues` and `solutions`.

## Entity-Relationship Diagram

The following diagram shows the structure of the tables and the relationship between them. An `issue` can have multiple `solutions`.

```mermaid
erDiagram
    issues {
        int id PK "increment"
        text issue_title "not null"
        text issue_description
        text tags
        timestamp created_at
    }

    solutions {
        int id PK "increment"
        int issue_id FK "not null"
        text solution_description "not null"
        timestamp created_at
    }

    issues ||--o{ solutions : "has"
```
