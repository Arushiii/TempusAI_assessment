process REGRESSION_MODEL {

    container 'docker.io/arushi08/linear_regression:1.0.0'

    input:
    path(file)

    output:
    path('*.csv')

    script:
    """
    regression_model.r $file $params.x_var $params.y_var

    """
}