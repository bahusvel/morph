from rules import rule
rule("if\s+(?!\(){{anything:condition}}\s*{", "if ({condition}) {")
rule("(?<![;\{\}\n])\n", ";\n")