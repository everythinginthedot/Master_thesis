# Master thesis project

This is a pilot version of the NAT-annotation pipeline using long-read RNA-seq (Nanopore). These libraries were prepared using cDNA (PCR-amplified) protocol.

## Data

### RNA-seq datasets

RNA-seq of _healthy person_ **SRR36191871** was downloaded from [NCBI SRA](https://www.ncbi.nlm.nih.gov/sra/SRX31228964[accn])

```
prefetch SRR36191871
fatserq-dump SRR36191871/
```

Resulting file: `SRR36191871.fastq`
Shasum: `d2162ac850b042b2b9ccf1fb740442da5e652fa6`

---

RNA-seq from patient with lung cancer **SRR36191863** was downloaded from [NCBI SRA](https://www.ncbi.nlm.nih.gov/sra/SRX31228972[accn])

```
prefetch SRR36191863
fatserq-dump SRR36191863/
```

Resulting file: `SRR36191863.fastq`
Shasum: `027b2ce68de83c1e7947519f25a5ccd8ad2fe243`


### Reference genome

Reference genome **GRCh38.p14** was downloaded from [NCBI FTP](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/) using command:

```
wget "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.fna.gz"
```



## Data Quality

### NanoPlot

**Healthy**
'''
NanoPlot --fastq SRR36191871.fastq  -o SRR36191871_nanoplot  
'''

![NanoPlot SRR36191871]('./data/images/Nanoplot_SRR36191871_header.png')



**Cancer**
'''
NanoPlot --fastq SRR36191863.fastq  -o SRR36191863_nanoplot 
'''


Filtlong
Porechop

