process SPLIT {
    container 'arushi08/linear_regression:1.0.0'

    input:
    tuple val(dataset),  path(dataset_file_path)

    output:
    tuple val(dataset), path('*.csv')

    script:
    """
    split.r $dataset $dataset_file_path $params.split_column
    """
}