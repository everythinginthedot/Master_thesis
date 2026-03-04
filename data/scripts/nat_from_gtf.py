import gffutils

fn = gffutils.example_filename('example.gff')
fn = './example.gtf'

def transform_func(x):
    # adds some text to the end of transcript IDs
    if 'transcript_id' in x.attributes:
        x.attributes['transcript_id'][0] += '_transcript'
    return x

db = gffutils.create_db(fn, 
                        dbfn='test.db', 
                        force=True, 
                        merge_strategy='create_unique', 
                        sort_attribute_values=True,
                        id_spec={'gene': 'gene_id', 'transcript': "transcript_id"},
                        transform=transform_func,
                        keep_order=True)



db = gffutils.FeatureDB('test.db', keep_order=True)

gene = db['ENSG00000310526.1']
print(gene)
print('')
print(gene.start)
print(gene.end)


print('')

print('')

for i in db.children(gene, featuretype='transcript', order_by='start'):
    print(i)

print('')



