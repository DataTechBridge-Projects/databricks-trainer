# BI Tools

A reference library for Solution Architects working on **BI reporting migration and modernization engagements**. Each tool page is designed to help you quickly understand the components, artifact lifecycle, and delivery model of a BI platform — so you can assess scope, map concepts, and guide customers toward a modern analytics stack on Databricks.

---

## Why This Exists

Enterprise BI migrations are deceptively complex. Customers have years of report logic, embedded security, and delivery automation built into tools like SSRS, Cognos, or Business Objects — and they need help understanding what they have, how it actually works under the hood, and what maps cleanly to a modern platform.

This section helps SAs answer:

- What are the core components and artifacts in this BI tool?
- How does data flow from source to consumer — what is server-side vs. client-side?
- What is the artifact lifecycle: what gets built, deployed, compiled, cached, and rendered?
- How do I inventory and scope the estate for migration?
- How do concepts in this tool map to Databricks SQL, Lakeview, or a connected BI layer?

---

## Available Tools

| Tool | Description |
|------|-------------|
| [SSRS](ssrs.md) | Microsoft SQL Server Reporting Services — components, artifact lifecycle, RDL/RDS/RSD formats, RLS patterns, and Databricks migration mapping |
| [IBM Cognos](cognos.md) | IBM Cognos Analytics — component architecture, Framework Manager semantic layer, burst delivery, OLAP/TM1 mapping, and Databricks migration assessment |

---

> More tools will be added over time. Each follows the same structure: ecosystem overview → component architecture → artifact lifecycle → migration assessment → Databricks mapping.
