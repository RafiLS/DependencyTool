class ReportGenerator:

    def generate_full_report(
        self,
        depcheck_output,
        sniffer_output,
        snyk_output,
        dirty_waters_output,
        dependencies,
        project_meta=None,
        project_repo=None
    ):

        md = []
        md.append("# Dependency Analysis Report\n")

        total_smells = 0

        depcheck_output = depcheck_output or {}
        sniffer_output = sniffer_output or {}
        snyk_output = snyk_output or {}
        dirty_waters_output = dirty_waters_output or {}
        project_meta = project_meta or {}
        project_repo = project_repo or {}

        has_package_json = project_meta.get("has_package_json", False)
        has_package_lock = project_meta.get("has_package_lock", False)

        md.append("\n## Project Structure")

        if project_repo:
            md.append(f"## Project: {project_repo}\n")
            
        md.append(f"- package.json: {'Yes' if has_package_json else 'No'}")
        md.append(f"- package-lock.json: {'Yes' if has_package_lock else 'No'}")

        # depcheck

        unused_deps = [
            d for d in dependencies
            if not getattr(d, "is_used", True)
        ]

        missing_deps = [
            d for d in dependencies
            if any(
                s.description == "Undeclared dependency"
                for s in getattr(d, "smell_indicators", [])
            )
        ]

        md.append(f"\n## Unused dependencies/Bloated Dependencies ({len(unused_deps)})")

        if unused_deps:
            md.extend([f"- {d.name}" for d in unused_deps])
        else:
            md.append("- None")

        md.append(f"\n## Missing dependencies ({len(missing_deps)})")

        if missing_deps:
            md.extend([f"- {d.name}" for d in missing_deps])
        else:
            md.append("- None")

        depcheck_risks = len(unused_deps) + len(missing_deps)
        total_smells += depcheck_risks

        # DependencySniffer

        pinned = sniffer_output.get("pinned", []) or []
        url = sniffer_output.get("url_dependencies", []) or []
        restrict = sniffer_output.get("restrict_constraints", []) or []
        perm = sniffer_output.get("permission_constraints", []) or []
        risks = sniffer_output.get("version_risks", []) or []

        def section(title, data):
            md.append(f"\n## {title} ({len(data)})")
            md.extend([f"- {d}" for d in data] if data else ["- None"])

        section("Pinned dependencies", pinned)
        section("URL dependencies", url)
        section("Restrict constraints", restrict)
        section("Permission constraints", perm)

        filtered_risks = [
            r for r in risks
            if r.get("risk") not in ("SAFE", "UNKNOWN")
        ]

        md.append(f"\n## Version Risk Analysis ({len(filtered_risks)})")

        if filtered_risks:
            md.extend([
                f"- {r['dependency']} → {r['risk']}"
                for r in filtered_risks
            ])
        else:
            md.append("- None")

        sniffer_smells = (
            len(pinned) +
            len(url) +
            len(restrict) +
            len(perm) +
            len(filtered_risks)
        )

        total_smells += sniffer_smells

        # snyk

        install = snyk_output.get("install_scripts", []) or []
        license_issues = snyk_output.get("license_anomalies", []) or []
        transitive = snyk_output.get("transitive_dependencies", []) or []

        section("Install scripts", install)
        section("Problematic licenses", license_issues)
        section("Transitive dependencies", transitive)

        snyk_smells = len(install) + len(license_issues) + len(transitive)
        total_smells += snyk_smells

        # dirty waters

        stats = dirty_waters_output.get("stats", {}) or {}

        missing_source_code = stats.get("missing_source_code", 0)
        repo_404 = stats.get("repo_404", 0)
        inaccessible_sha = stats.get("inaccessible_sha", 0)
        deprecated = stats.get("deprecated", 0)
        no_code_signature = stats.get("no_code_signature", 0)
        invalid_code_signature = stats.get("invalid_code_signature", 0)
        forks = stats.get("forks", 0)
        aliased = stats.get("aliased", 0)

        md.append("\n")
        md.append(f"- Missing source code: {missing_source_code}")
        md.append(f"- Repo 404: {repo_404}")
        md.append(f"- Inaccessible SHA: {inaccessible_sha}")
        md.append(f"- Deprecated: {deprecated}")
        md.append(f"- No code signature: {no_code_signature}")
        md.append(f"- Invalid code signature: {invalid_code_signature}")
        md.append(f"- Forks: {forks}")
        md.append(f"- Aliased: {aliased}")

        dirty_smells = (
            missing_source_code
            + repo_404
            + inaccessible_sha
            + deprecated
            + no_code_signature
            + invalid_code_signature
            + forks
            + aliased
        )

        total_smells += dirty_smells

        # final summary

        md.append(f"\n### Total Smells: {total_smells}")

        return "\n".join(md)