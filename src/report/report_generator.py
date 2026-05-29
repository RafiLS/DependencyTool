class ReportGenerator:

    def generate_full_report(
        self,
        results,
        dependencies,
        project_meta=None,
        project_repo=None,
        sbom=None,
        sbom_path=None
    ):

        md = []
        md.append("# Dependency Analysis Report\n")

        total_smells = 0

        results = results or {}
        project_repo = project_repo or {}

        sniffer_meta = results.get("dependency_sniffer", {}).get("project_meta", {})

        has_package_json = sniffer_meta.get("has_package_json", False)
        has_package_lock = sniffer_meta.get("has_package_lock", False)

        md.append("\n## Project Structure")

        if project_repo:
            md.append(f"## Project: {project_repo}\n")
            md.append(f"- package.json: {'Yes' if has_package_json else 'No'}")
            md.append(f"- package-lock.json: {'Yes' if has_package_lock else 'No'}")

        if sbom:
            md.append("\n## SBOM Summary")

            md.append(f"- SBOM file: {sbom_path}")
            md.append(f"- Total components: {sbom.get('total_components', 0)}")

            license_dist = sbom.get("license_distribution", {})

            md.append(
                "- License distribution: " +
                ", ".join([f"{k} ({v})" for k, v in license_dist.items()]) if license_dist else "- License distribution: N/A"
            )

            no_license = sbom.get("no_license", [])
            md.append(f"- Components with no license: {len(no_license)}")

        unused_deps = [
            d.name for d in dependencies
            if not getattr(d, "is_used", True)
        ]

        missing_deps = [
            d.name for d in dependencies
            if any(
                s.description == "Undeclared dependency"
                for s in getattr(d, "smell_indicators", [])
            )
        ]
        md.append(f"\n## Unused dependencies ({len(unused_deps)})")
        md.extend([f"- {d}" for d in unused_deps] if unused_deps else ["- None"])

        md.append(f"\n## Missing dependencies ({len(missing_deps)})")
        md.extend([f"- {d}" for d in missing_deps] if missing_deps else ["- None"])

        total_smells += len(unused_deps) + len(missing_deps)

        sniffer = results.get("dependency_sniffer", {})

        def section(title, data):
            md.append(f"\n## {title} ({len(data)})")
            md.extend([f"- {d}" for d in data] if data else ["- None"])

        section("Pinned dependencies", sniffer.get("pinned", []))
        section("URL dependencies", sniffer.get("url_dependencies", []))
        section("Restrict constraints", sniffer.get("restrict_constraints", []))
        section("Permission constraints", sniffer.get("permission_constraints", []))

        risks = [
            r for r in sniffer.get("version_risks", [])
            if r.get("risk") not in ("SAFE", "UNKNOWN")
        ]

        md.append(f"\n## Version Risk Analysis ({len(risks)})")
        md.extend([
            f"- {r['dependency']} → {r['risk']}"
            for r in risks
        ] if risks else ["- None"])

        total_smells += len(risks)

        snyk = results.get("snyk", {})

        section("Install scripts", snyk.get("install_scripts", []))
        section("Problematic licenses", snyk.get("license_anomalies", []))
        section("Transitive dependencies", snyk.get("transitive_dependencies", []))

        total_smells += (
            len(snyk.get("install_scripts", [])) +
            len(snyk.get("license_anomalies", [])) +
            len(snyk.get("transitive_dependencies", []))
        )

        dirty = results.get("dirty_waters", {}).get("stats", {})

        md.append("\n## Other Smells Detected")

        dirty_total = sum(v for v in dirty.values() if isinstance(v, int))

        for k, v in dirty.items():
            md.append(f"- {k}: {v}")

        total_smells += dirty_total

        md.append(f"\n### Total Smells: {total_smells}")

        return "\n".join(md)