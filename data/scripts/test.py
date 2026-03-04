import gffutils

##################
## agat_convert_sp_gxf2gxf.pl -g example_big.gtf -o example_big.gff
##################

db = gffutils.create_db(
    "example_big.gff",
    dbfn="example.db",
    force=True,

    keep_order=True,
    sort_attribute_values=True,

    merge_strategy="merge",

    # для GFF3 инференс НЕ нужен
    disable_infer_genes=True,
    disable_infer_transcripts=True
)

db = gffutils.FeatureDB("example.db", keep_order=True)

genes = list(db.features_of_type("gene"))
print("Genes:", len(genes))
print("Gene ID:", genes[0].id)

transcripts = list(db.features_of_type("transcript"))
print("Transcripts:", len(transcripts))
print("Transcript ID:", transcripts[0].id)


print('')


gene_id = "ENSG00000310526.1"
gene = db[gene_id]

transcripts = list(db.children(gene, featuretype="transcript"))
print("Gene transcripts:", len(transcripts))

for t in transcripts[:3]:
    print(" ", t.id)



print('')


exons = list(db.children(transcripts[0], featuretype="exon", order_by="start"))
print("Exons:", len(exons))

for e in exons:
    print(e.start, e.end)



# --------- 2. Получаем все гены, сортированные по хромосоме и старту ---------
genes = list(db.features_of_type("gene"))
genes.sort(key=lambda g: (g.seqid, g.start))

print('')
print('Genes: ')
for gene in genes:
    print(gene.id)
print('')


# --------- 3. Функция для проверки перекрытия двух транскриптов ---------
def overlap(tx1, tx2):
    """
    Возвращает длину перекрытия двух транскриптов.
    Если перекрытия нет, возвращает 0.
    """
    start = max(tx1.start, tx2.start)
    end = min(tx1.end, tx2.end)
    if start <= end:
        return end - start + 1  # длина перекрытия в нуклеотидах
    return 0


# --------- 4. Функция определения типа перекрытия генов ---------
def classify_overlap(gene1, gene2):
    """
    Определяет тип перекрытия между двумя генами:
    head-to-head, tail-to-tail или embedded
    """

    # embedded: один ген полностью внутри другого
    if gene1.start >= gene2.start and gene1.end <= gene2.end:
        return "embedded (gene1 in gene2)"
    if gene2.start >= gene1.start and gene2.end <= gene1.end:
        return "embedded (gene2 in gene1)"

    # дальше считаем, что гены на разных цепях
    if gene1.strand == "+" and gene2.strand == "-":
        # gene1 слева, gene2 справа
        if gene1.start < gene2.start:
            return "tail-to-tail"
        else:
            return "head-to-head"

    if gene1.strand == "-" and gene2.strand == "+":
        # gene2 слева, gene1 справа
        if gene2.start < gene1.start:
            return "tail-to-tail"
        else:
            return "head-to-head"

    return "unknown"


# --------- 4. Список для результатов ---------
results = []


# --------- 5. Идем по соседним генам ---------
for i in range(len(genes)-1):
    gene1 = genes[i]
    gene2 = genes[i+1]

    # проверяем, что гены на одной хромосоме
    if gene1.seqid != gene2.seqid:
        continue

    if gene1.strand == gene2.strand:
        #print('THE SAME STRAND')
        continue

    # получаем транскрипты
    txs1 = list(db.children(gene1, featuretype="transcript"))
    txs2 = list(db.children(gene2, featuretype="transcript"))

    overlapping_pairs = []

    # сравниваем каждый транскрипт первого гена с каждым второго
    for t1 in txs1:
        for t2 in txs2:
            ol_len = overlap(t1, t2)
            if ol_len > 0:
                overlapping_pairs.append((t1.id, t2.id, ol_len))

    # если есть перекрытия, сохраняем
    if overlapping_pairs:
        overlap_type = classify_overlap(gene1, gene2)

        results.append({
            "gene1": gene1.id,
            "gene2": gene2.id,
            "overlap_type": overlap_type,
            "overlapping_transcripts": overlapping_pairs
        })




import csv

def write_overlaps_to_csv(results, out_csv):
    """
    Сохраняет результаты перекрытий в CSV.
    Одна строка = одно перекрытие транскриптов.
    """

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)

        # заголовок
        writer.writerow([
            "gene1",
            "gene2",
            "overlap_type",
            "transcript1",
            "transcript2",
            "overlap_bp"
        ])

        # данные
        for r in results:
            gene1 = r["gene1"]
            gene2 = r["gene2"]
            overlap_type = r["overlap_type"]

            for tx1, tx2, ol_len in r["overlapping_transcripts"]:
                writer.writerow([
                    gene1,
                    gene2,
                    overlap_type,
                    tx1,
                    tx2,
                    ol_len
                ])

write_overlaps_to_csv(results, "gene_transcript_overlaps.csv")