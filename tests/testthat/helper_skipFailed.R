helperSkipFailed <- FALSE

expectSuccessStatus <- function(output) {
    status <- attr(output, "status", exact = TRUE)
    if (0 != status) {
        helperSkipFailed <<- TRUE
    }
    expect_equal(status, 0)
}
expectFailStatus <- function(output) {
    status <- attr(output, "status", exact = TRUE)
    if (1 != status) {
        helperSkipFailed <<- TRUE
    }
    expect_equal(status, 1)
}

skipIfPreviousFailed <- function() {
    if (helperSkipFailed) {
        skip("A previous test failed.")
    } else {
        return(invisible(TRUE))
    }
}
