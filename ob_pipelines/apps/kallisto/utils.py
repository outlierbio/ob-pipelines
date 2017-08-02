import pandas as pd


def load_abundance_gencode(fpath, split_id):
    df = pd.read_csv(fpath, sep='\t')
    if split_id:
        target_attr = df.target_id.str.split('|', expand=True)
        target_attr.columns = ['gencode_tx', 'gencode_gene', 'havana_gene', 'havana_tx', 
            'hugo_tx', 'hugo_symbol', 'tx_length', 'gene_type', 'undefined']
        merged = df.join(target_attr)
        return merged[['gencode_tx', 'gencode_gene', 'hugo_symbol', 'gene_type', 
            'length', 'eff_length', 'est_counts', 'tpm']]
    else:
        return df

def merge_column(input_files, labels, data_col='est_counts', annot=False):
    """Merge Kallisto samples into a matrix

    Gather one column from all input_files into a single merged
    table, matching the index column to the first column of the 
    annotation file.
    """

    # Grab annotations from the first file
    first = input_files[0]
    first_df = load_abundance_gencode(first, split_id=annot)
    if annot:
        annotations = first_df[['gencode_tx', 'gencode_gene', 'hugo_symbol', 'gene_type', 'length']]
    else:
        annotations = first_df[['target_id', 'length']]

    # Add the first file to the list
    sample_col = first_df[data_col]
    sample_col.name = labels[0]
    all_data = [sample_col]

    # Loop to add the rest
    for i, fpath in enumerate(input_files[1:]):
        sample_df = load_abundance_gencode(fpath, split_id=annot)
        sample_col = sample_df[data_col]
        sample_col.name = labels[i + 1]
        all_data.append(sample_col)

    # Merge columns into a single matrix
    merged = pd.concat(all_data, axis=1)

    if annot:
        # Use Gencode Transcript ID as index
        merged.index = annotations['gencode_tx']
    else:
        merged.index = annotations['target_id']

    return annotations, merged