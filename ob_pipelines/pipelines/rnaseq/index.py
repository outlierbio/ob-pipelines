def get_index(tool, species='human', build='latest'):
    indexes = {
        'star': {
            'human': {
                'test': '/reference/star/b38.chr21.gencode_v25.101',
                'latest': '/reference/star/b38.gencode_v25.101'
            },
            'mouse': {
                'latest': '/reference/star/m38.gencode_vM12.101'
            }
        },
        'kallisto': {
            'human': {
                'test': '/reference/kallisto/gencode_v25.chr21/gencode_v25.chr21.idx',
                'latest': '/reference/kallisto/gencode_v25/gencode.v25.ercc.idx'
            }
        }
    }
    return indexes[tool][species][build]
