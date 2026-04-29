class ReportGenerator:

    def generate_full_report(
        self,
        depcheck_output,
        sniffer_output,
        snyk_output,
        dependencies
    ):

        md = []
        md.append("# Dependency Analysis Report\n")

        total_smells = 0

        # DEPCHECK
        md.append("# Depcheck\n")

        # UNUSED
        unused = depcheck_output.get("dependencies", []) + \
                 depcheck_output.get("devDependencies", [])

        md.append(f"##-Unused dependencies ({len(unused)})")
        if unused:
            md.extend([f"- {d}" for d in unused])
        else:
            md.append("- None")

        total_smells += len(unused)

        # MISSING
        missing = depcheck_output.get("missing", {})
        md.append(f"\n##-Missing dependencies ({len(missing)})")

        if missing:
            for dep, files in missing.items():
                md.append(f"- {dep} used in {len(files)} files")
                md.append(
                    f"  → {', '.join(files[:3])}"
                    f"{'...' if len(files) > 3 else ''}"
                )
        else:
            md.append("- None")

        total_smells += len(missing)

        # BLOATED
        bloated = depcheck_output.get("bloated", [])
        md.append(f"\n## Bloated dependencies ({len(bloated)})")

        if bloated:
            md.extend([f"- {b}" for b in bloated])
        else:
            md.append("- None")

        total_smells += len(bloated)

        # SNIFFER
        md.append("\n# DependencySniffer\n")

        pinned = sniffer_output.get("pinned", [])
        url = sniffer_output.get("url_dependencies", [])
        restrict = sniffer_output.get("restrict_constraints", [])
        perm = sniffer_output.get("permission_constraints", [])
        risks = sniffer_output.get("version_risks", [])

        def section(title, data):
            md.append(f"\n## {title} ({len(data)})")
            if data:
                md.extend([f"- {d}" for d in data])
            else:
                md.append("- None")

        section("-Pinned dependencies", pinned)
        section("-URL dependencies", url)
        section("-Restrict constraints", restrict)
        section("-Permission constraints", perm)

        # VERSION RISKS
        md.append(f"\n## Version Risk Analysis ({len(risks)})")
        if risks:
            md.extend([
                f"- {r['dependency']} → {r['risk']}"
                for r in risks
            ])
        else:
            md.append("- None")

        total_smells += len(pinned) + len(url) + len(restrict) + len(perm) + len(risks)
        # SNYK
        md.append("\n#Snyk\n")

        install = snyk_output.get("install_scripts", [])
        license_issues = snyk_output.get("license_anomalies", [])
        transitive = snyk_output.get("transitive_dependencies", [])

        section("- Install scripts", install)
        section("- Problematic licenses", license_issues)
        section("- Transitive dependencies", transitive)

        total_smells += len(install) + len(license_issues) + len(transitive)

        md.append("\n---\n")
        md.append("## General summary\n")

        depcheck_total = len(unused) + len(missing) + len(bloated)
        sniffer_total = len(pinned) + len(url) + len(restrict) + len(perm) + len(risks)
        snyk_total = len(install) + len(license_issues) + len(transitive)

        md.append(f"- Depcheck: {depcheck_total} smells")
        md.append(f"- DependencySniffer: {sniffer_total} smells")
        md.append(f"- Snyk: {snyk_total} smells")

        md.append(f"\n### TOTAL: {total_smells} smells\n")

        if total_smells == 0:
            md.append("- No smells detected.")
        elif total_smells < 5:
            md.append(f"- Low risk ({total_smells})")
        elif total_smells < 15:
            md.append(f"- Moderate risk ({total_smells})")
        else:
            md.append(f"- High risk ({total_smells})")

        return "\n".join(md)