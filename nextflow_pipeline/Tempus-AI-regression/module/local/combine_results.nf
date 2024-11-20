process COMBINE_RESULTS {

    container 'docker.io/arushi08/linear_regression:1.0.0'

    input:
    path(files)
    
    output:
    path('*.csv')
    
    script:
    """
    combine_results.r $files
    """
}