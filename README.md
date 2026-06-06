# Dependency Analysis Tool

## Description

This application was developed to detect *Software Supply Chain Smells* and dependency-related risks in software projects. The tool focuses on analyzing project dependencies and identifying indicators of potential risks and dependency-related issues rather than directly detecting vulnerabilities.

The application integrates three external tools:

- **Dirty-Waters** - https://github.com/chains-project/dirty-waters
- **Depcheck** - https://github.com/depcheck/depcheck
- **Snyk** - https://snyk.io

Each tool is responsible for different types of analysis:

- **[Dirty-Waters](https://github.com/chains-project/dirty-waters)**: detection of supply chain smells and provenance-related issues;
- **[Depcheck](https://github.com/depcheck/depcheck)**: detection of unused or missing dependencies;
- **[Snyk](https://snyk.io)**: analysis of dependency security indicators.

> **Note:**  
> This application is not intended to directly detect software vulnerabilities.  
> Instead, it identifies indicators of vulnerabilities, risky dependency patterns, and *Software Supply Chain Smells* that may represent potential security, maintenance, or reliability risks within the project's dependency ecosystem.


# Objectives and Approach

The main goal of this project is to study the concept of *Software Supply Chain Smells* and develop a tool capable of analyzing dependency-related risks in React applications.

The application focuses on analyzing project manifest files such as `package.json` in order to identify suspicious patterns, dependency management issues, and indicators associated with software supply chain smells.

The tool acts as a preventive analysis mechanism, helping developers identify situations that may require further security assessment or dependency review.


# Project Objectives

- Study and understand the concept of *Software Supply Chain Smells*;
- Analyze dependency-related indicators and risks in React applications;
- Develop an automated mechanism to analyze manifest files such as `package.json`;
- Identify potentially problematic dependencies and risky dependency configurations;
- Improve software maintainability and dependency management practices;
- Increase awareness of secure dependency management practices aligned with recommendations such as OWASP Top 10.

---

# Prerequisites

Before running the application, make sure the system has all required dependencies installed.

---

## 1. Python

The DirtyWaters tool was developed in Python, therefore Python 3 must be installed in order to run the application.


## 2. Python Virtual Environment (Windows)

To run the application on Windows, it is recommended to create a Python virtual environment (e.g., `venv`) in order to isolate the project's dependencies from the global system environment.


## 3. Node.js and npm

Depcheck and Snyk require Node.js and npm.

## 4. GitHub

Dirty Waters analyzes GitHub repositories, therefore the target project must be hosted on GitHub.

---

# Tool Installation

After installing all required tools and dependencies, the repository must be cloned locally.

```bash
git clone <repository-url>
cd DependencyTool
```

# Application Structure

```text
DependencyTool/
│
├── env/
├── Docs/
├── save_reports/
├── src/
├── tests/
├── config.toml
└── README.md
```

---

# Running the Application

The application performs local dependency analysis while also accessing GitHub repositories for additional metadata and supply chain evaluation:

```bash
dependencyTool analyze <owner/repository> --path <local_project_path>
```
# Report

After running the tool, the smells results are in the report in the "save_reports" directory, which contains the name of the analyzed project along with the report and the SBOM code.

# General System Requirements

The application requires:

- Internet access;
- command-line execution permissions;
- access to project dependency files (`package.json`);
- configured GitHub and Snyk authentication.


# Technologies Used

- Python
- Node.js
- Dirty-Waters
- Depcheck
- Snyk
- Git
- PowerShell

---

# Future Improvements

Possible future improvements include:

- support for additional dependency ecosystems;
- detection of new *Software Supply Chain Smells*;
- new tools for smells detection.
- integration with CI/CD pipelines;
- automatic dependency risk scoring;
- support for additional manifest formats.

---

# Related Work

- **[Dirty-Waters: Detecting Software Supply Chain Smells](https://arxiv.org/abs/2410.16049)**


- **[Demystifying the vulnerability propagation and its evolution via dependency trees in the NPM ecosystem](https://dl.acm.org/doi/10.1145/3510003.3510142)**

- **[Dependency Smells in JavaScript Projects](https://dl.acm.org/doi/abs/10.1109/tse.2021.3106247)**

- **[What are weak links in the npm supply chain?](https://dl.acm.org/doi/10.1145/3510457.3513044)**

- **[Software Supply Chain Smells Lightweight Analysis](https://arxiv.org/abs/2603.24282)**
# License

MIT License