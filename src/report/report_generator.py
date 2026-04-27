class ReportGenerator:

    def generate_depcheck_report(self, depcheck_output, dependencies):

        unused_prod = depcheck_output.get("dependencies", [])
        unused_dev = depcheck_output.get("devDependencies", [])
        missing = depcheck_output.get("missing", {})

        md = []

        md.append("# Relatório de Análise de Dependências\n")

        # --------------------
        # UNUSED DEPENDENCIES
        # --------------------
        md.append("## Dependências não utilizadas\n")

        all_unused = unused_prod + unused_dev

        if all_unused:
            for dep in all_unused:
                md.append(f"- {dep}")
        else:
            md.append("- Nenhuma")

        # --------------------
        # MISSING
        # --------------------
        md.append("\n## Dependências não declaradas\n")

        if missing:
            for dep, files in missing.items():
                md.append(f"- **{dep}** usado em {len(files)} ficheiros")
        else:
            md.append("- Nenhuma")

        # --------------------
        # BLOATED
        # --------------------
        md.append("\n## Bloated dependencies\n")

        total_used = len(depcheck_output.get("using", {}))

        if total_used > 10:
            md.append(f"- Projeto com {total_used} dependências usadas → possível excesso")
        else:
            md.append("- Sem sinais de excesso de dependências")

        return "\n".join(md)