## Data Migration and Cloud Adoption Strategies

### Section at a Glance
**What you'll learn:**
- Evaluating and selecting Cloud Adoption Framework (CAF) migration strategies (Rehost, Replatform, Refactor).
- Architecting offline vs. online data migration patterns for varying dataset scales.
- Selecting the appropriate Azure migration tools (Azure Data Box, DMS, ADF, AzCopy) based on bandwidth and downtime constraints.
- Designing secure, scalable pipelines for large-scale data movement.
- Assessing the business impact and cost-benefit analysis of different migration approaches.

**Key terms:** `Replatforming` · `Online Migration` · `Offline Migration` · `Azure Data Box` · `Azure Database Migration Service (DMS)` · `Data Gravity`

**TL; $DR:** Successful migration is not just about moving bits; it is about choosing a strategy (Rehost, Replatform, or Refactor) that balances business downtime requirements against the complexity of modernizing your data architecture.

---

### Overview
For many enterprises, the "Cloud Migration" project is the most significant technical and cultural undertaking they will face. From a business perspective, the driver is rarely just "using new tech"; it is about reducing technical debt, eliminating capital expenditure (CapEx) for on-premises hardware, and gaining the ability to iterate on data products at a speed impossible in a legacy environment.

The core problem a Data Engineer solves during migration is "Data Gravity." As datasets grow into the petabyte scale, they become difficult to move due to bandwidth constraints and the sheer time required for transfer. A poorly planned migration results in "extended downtime," where business-critical reporting and analytics are unavailable, leading to lost revenue and eroded trust in the IT organization.

In the context of the DP-203 exam and your professional practice, this section bridges the gap between *storing* data and *moving* it. You cannot build a modern Lakehouse in Azure if you cannot reliably ingest the historical context residing in legacy SQL Servers or Hadoop clusters. We will focus on the decision-making framework used to choose between moving "as-is" versus "re-architecting" for the cloud.

---

### Core Concepts

#### 1. The Migration Strategies (The "R" Framework)
When moving workloads, you must choose a path based on your budget, time, and desired end-state.
* **Rehost (Lift & Shift):** Moving VMs or databases to Azure (e.g., SQL Server on Azure VM) with minimal changes. 
    > ⚠️ **Warning:** While Rehosting is the fastest way to exit a data center, it often carries your legacy technical debt and inefficient licensing costs into the cloud.
* **Replatform (Lift and Reshape):** Making minor optimizations to take advantage of cloud benefits without changing the core architecture (e.g., moving SQL Server to Azure SQL Managed Instance).
* **Refactor (Re-architect):** Completely redesigning the data architecture to be cloud-native (e.g., moving from a monolithic SQL Server to an Azure Synapse/Databricks Lakehouse). 
    📌 **Must Know:** This is the most expensive and time-consuming strategy, but it offers the highest long-term ROI through scalability and reduced management overhead.

#### 2. Online vs. Offline Migration
The choice between these two is governed by your **Network Bandwidth** and **Allowed Downtime**.
* **Online Migration:** Data is transferred over the network (e.g., via VPN or ExpressRoute) while the source database remains operational. This requires careful synchronization to capture changes that occur during the migration.

* **Offline Migration:** Physical hardware is shipped to an Azure datacenter. This is used when the dataset is so large that the "transfer time" over the internet would take weeks or months.
    > 💡 **Tip:** Use Online migration for databases where a "cutover window" of a few minutes is acceptable; use Offline migration for massive historical archives where the "initial seed" is the primary challenge.

#### 3. Migration Tooling Landscape
* **Azure Data Box:** A physical device sent to you to load data locally.
* **Azure Database Migration Service (DMS):** A fully managed service designed to enable seamless migrations from various database engines to Azure.
* **Azure Data Factory (ADF):** The "orchestrator." It is used for both the initial bulk move and the subsequent incremental updates.
* **AzCopy:** A command-line utility for high-performance copying of blobs.

---

### Architecture / How It Works

The following diagram illustrates a hybrid migration pattern involving an initial "Bulk" offline load followed by an "Incremental" online synchronization.

```mermaid
graph LR
    subgraph "On-Premises Data Center"
        A[(Legacy SQL Server<br/>100 TB)] --> B[Data Box Service]
        A --> C[Change Data Capture / Log Tailing]
    end

    sub\.subgraph "Transit"
        B -->|Physical Shipping| D[Azure Data Box]
        C -->|ExpressRoute/VPN| E[Azure Data Factory]
    end

    subgraph "Azure Cloud"
        D --> F[(Azure Data Lake Storage Gen2)]
        E --> F
        F --> G[(Azure SQL Managed Instance)]
    end
```

1. **Legacy SQL Server:** The source system containing the authoritative historical data.
2. **Data Box Service:** Handles the "Heavy Lifting" of the 100TB baseline to avoid saturating the corporate network.
3. **Azure Data Box:** The physical appliance that receives the data and is shipped to Microsoft.
4. **Change Data Capture (CDC):** A process that tracks all transactions occurring on-prem *after* the Data Box was packed.
5. **Azure Data Factory:** The engine that pulls those small, incremental changes over the network to keep the cloud target in sync with the source.
6. **Azure SQL Managed Instance:** The final, modernized destination for the data.

---

/### Comparison: When to Use What

| Strategy | Best For | Trade-offs | Approx. Cost Signal |
| :--- | :--- | :--- | :--- |
| **Rehost** | Rapid data center exit; urgent deadlines. | Low agility; retains legacy cost/complexity. | Low (Initial) / High (Long-term) |
| **Replatform** | Reducing management burden without code changes. | Requires some schema/connection string updates. | Moderate |
| **Refactor** | Maximum scalability; modernizing analytics. | High engineering effort; high risk of complexity. | High (Initial) / Low (Long-term) |
| **Retain** | Legacy systems that cannot be moved due to latency. | Stagnant technology; "Data Silo" risk. | Moderate (Maintenance) |

**How to choose:** Start with your **Downtime Tolerance**. If you cannot afford more than 1 hour of downtime, you must choose a Replatform/Refactor strategy using DMS/ADF for continuous sync.

---

### Cost Cheat Sheet

| Scenario | Recommended Option | Key Cost Driver | Watch Out For |
| :--- | :--- | :--- | :--- |
| **Multi-PB Migration** | Azure Data Box | Shipping & Hardware rental | Data egress/ingress complexity |
| **Small DB (< 500GB)** | AzCopy / ADF | Network Bandwidth/Egress | Not optimizing for compression |
| **Continuous Sync** | Azure DMS | Compute Instance uptime | Over-provisioning the DMS instance |
| **Global Data Move** | Azure Data Factory | Integration Runtime (IR) usage | Running IR in a high-cost region |

> 💰 **Cost Note:** The single biggest "hidden" cost in migration is **Data Egress**. While Azure Ingress (moving data *into* Azure) is free, moving data *out* of a cloud provider or between regions during a complex migration can result in massive, unexpected telecommunications charges.

---

### Service & Tool Integrations

1. **The "Seed & Sync" Pattern:**
    1. Use **Azure Data Box** to move the "Base" dataset (the bulk of the TBs).
    2. Use **Azure Data Factory** to monitor the source for changes.
    3. Use **Azure SQL Managed Instance** to receive the final incremental updates.
2. **The Modernization Pipeline:**
    1. Extract from **On-Prem SQL** using **Self-Hosted Integration Runtime**.
    2. Transform via **Azure Databricks**.
    3. Sink into **Azure Data Lake Storage (ADLS) Gen2**.

---

### Security Considerations

Data migration involves moving your most sensitive assets across boundaries. Security must be baked into the pipeline, not bolted on.

| Control | Default State | How to Enable / Strengthen |
| :--- | :--- | :--- |
| **Encryption in Transit** | Enabled (TLS) | Ensure all ADF pipelines use HTTPS/TLS 1.2+. |
| **Encryption at Rest** | Enabled (SSE) | Use Customer-Managed Keys (CMK) for higher compliance. |
| **Network Isolation** | Public Access | Use **Azure Private Link** to ensure data never hits the public internet. |
| **Identity Management** | Local Credentials | Use **Managed Identities** for ADF to access Storage/SQL. |

---

### Performance & Cost

**The Throughput Bottleneck:**
In migrations, the bottleneck is rarely the Azure destination; it is almost always the **Source Read Capacity** or the **Network Pipe**. 

**Example Scenario:**
You need to migrate 50TB of data. 
* **Option A (Internet/VPN):** 100 Mbps connection. Theoretical transfer time: ~46 days (assuming 100% utilization, which never happens).
* **Option B (Azure Data Box):** 4-7 days (including shipping and local loading).

**Tuning Guidance:**
* **Compression:** Always compress data before transmission (using `AzCopy` or `ADF`).
* **Parallelism:** In ADF, increase the `degree of copy parallelism` to saturate the available bandwidth.
* **Partitioning:** For large SQL tables, use "Physical Partitions" or "Dynamic Range" partitioning in your copy activity to read multiple chunks of the table simultaneously.

---

### Hands-On: Key Operations

**Step 1: Using AzCopy to move a folder to Blob Storage**
This command initiates a high-speed transfer of a local directory to an Azure container.
```bash
azcopy copy "/mnt/data/historical_logs" "https://mystorageaccount.blob.core.windows.net/migration_container?<SAS_TOKEN>" --recursive
```
> 💡 **Tip:** Always use a SAS token with a short expiration for migrations to minimize the security risk if the command logs are intercepted.

**Step 2: Creating a Self-Hosted Integration Runtime (SHIR) via Azure CLI**
This allows Azure Data Factory to "reach into" your on-premises network to pull data.
```azurecli
az datafactory runtime create \
    --resource-group MyMigrationRG \
    --factory-name MyDataFactory \
    --name MyOnPremRuntime \
    --type SelfHosted
```

---

### Customer Conversation Angles

**Q: "We have 200TB of data. Can we just use our existing VPN to move it all over the weekend?"**
**A:** "With a standard VPN, that would likely take several weeks of continuous transfer. I recommend an Azure Data Box for the initial bulk move to avoid saturating your business-critical network, followed by an online sync for the final delta."

**Q: "Will our applications experience downtime during the migration?"**
**A:** "That depends on the strategy. If we choose a Replatforming strategy using Azure DMS, we can keep your source database online and only perform a brief 'cutover' once the cloud target is synchronized."

**Q: "Is it cheaper to move everything 'as-is' (Rehost) or rewrite it for the cloud (Refactor)?"**
**A:** "Rehosting is cheaper and faster in the short term, but it doesn't reduce your long-term operational costs. Refactoring requires a higher upfront investment but significantly lowers your long-term management and scaling costs."

**Q: "How do we ensure our data isn't intercepted while moving over the internet?"**
**A:** "We implement end-to-end encryption using TLS for data in transit and use Azure Private Link to ensure the data travels through a private tunnel, completely bypassing the public internet."

** Answering the 'Hidden Cost' question:**
**Q: "What is the biggest risk to our migration budget?"**
**A:** "Unplanned data egress fees and the 'hidden' labor cost of fixing broken application code if we choose a Replatforming or Refactoring strategy."

---

### Common FAQs and Misconceptions

**Q: Does Azure Data Box encrypt the data on the device?**
**A:** Yes, the data is encrypted using AES-256.
> ⚠️ **Warning:** Do not rely solely on the device encryption; you must still ensure your transfer protocols (like AzCopy) are using secure, authenticated methods.

**Q: Can I use Azure Data Factory to migrate an Oracle database to Azure SQL?**
**A:** Yes, ADF supports a wide variety of connectors, including Oracle, to target Azure SQL or Synapse.

**Q: Is the 'Online Migration' always better than 'Offline'?**
**A:** No. For petabyte-scale datasets, the 'Online' approach can take months and consume all your available bandwidth.

**Q: Is there a cost for using Azure Data Box?**
**A:** Yes, you are charged for the device rental and the data processing/ingestion into Azure.

**Q: If I use Rehosting, do I still need to manage the OS?**
**A:** Yes. In a Rehost (VM) scenario, you are still responsible for patching and OS-level maintenance.
> ⚠️ **Warning:** A common mistake is thinking Rehosting eliminates all operational overhead. It only moves the overhead to a different data center.

**Q: Does AzCopy work with both Blob and ADLS Gen2?**
**A:** Yes, it is a unified tool for all Azure Blob storage flavors.

---

### Exam & Certification Focus
*Mapping to DP-203: Implement and manage data storage.*

*   **Identify Migration Tools:** Knowing when to use **Data Box** vs. **DMS** vs. **ADF** (High Frequency). 📌
*   **Migration Strategies:** Distinguishing between **Rehost, Replatform, and Refactor** in scenario-based questions. 📌
*   **Connectivity Patterns:** Understanding the role of the **Self-Hosted Integration Runtime (SHIR)** in hybrid environments.
*   **Security:** Selecting the correct encryption and network isolation (Private Link) methods for data in transit.
*   **Data Movement Patterns:** Identifying the difference between **Bulk Load** and **Incremental/Change Data Capture (CDC)**.

---

### Quick Recap
- **Strategy defines cost/benefit:** Rehost is fast; Refactor is powerful.
- **Size dictates method:** Use Data Box for massive volumes; use ADF/DMS for continuous sync.
- **Bandwidth is the bottleneck:** Online migration depends entirely on your network throughput.
- **Security is non-negotiable:** Use Private Link and Managed Identities to secure the pipeline.
- **Minimize Downtime:** Use DMS and CDC patterns to achieve near-zero downtime cutovers.

---

### Further Reading
**Azure Migration Guide** — The foundational guide for planning and executing migrations to Azure.
**Azure Data Box Documentation** — Technical details on device types, capacities, and shipping procedures.
**Azure Database Migration Service (DMS) Overview** — Deep dive into managing schema and data migration for SQL/PostgreSQL/MySQL.
**Azure Cloud Adoption Framework (CAF)** — The industry-standard framework for enterprise-scale cloud transitions.
**Azure Data Factory Connectivity Guide** — Detailed list of all supported on-premises and cloud data sources.