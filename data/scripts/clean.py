import re

with open("example.gtf") as fin, open("example.clean.gtf", "w") as fout:
    for line in fin:
        if line.startswith("#") or not line.strip():
            fout.write(line)
            continue

        parts = line.rstrip().split("\t")
        attrs = parts[8]

        cleaned = []
        for attr in attrs.split(";"):
            attr = attr.strip()
            if not attr:
                continue

            key, value = attr.split(None, 1)
            value = value.strip().strip('"')   # убираем кавычки
            cleaned.append(f"{key} {value}")

        parts[8] = "; ".join(cleaned) + ";"
        fout.write("\t".join(parts) + "\n")
