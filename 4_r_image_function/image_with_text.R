imageWithText <- function (mat, prefix='x=', xlab='Rows', ylab='Cols',
                           main='table', col=terrain.colors(100)) {
  #' Extends standard `image` function adding text to every cell.
  #' 
  #' matrix `mat` - input matrix;
  #' character `prefix` - prefix to be printed with every values in cells;
  #' character `xlab` - label of X axis, default: 'Rows'
  #' character `ylab` - label of Y axis, default: 'Cols'
  #' character `main` - main title of the figure;
  #' character `col` - colours of cells, default: `terrain.colors(100)`.
  #' Nothing is returned.

  rows <- 1:nrow(mat)
  cols <- 1:ncol(mat)
  image(rows, cols, mat, col=col, xaxt='n', yaxt='n', main=main,
        xlab=xlab, ylab=ylab,)
  axis(1, rows, labels=rownames(mat))
  axis(2, cols, labels=colnames(mat))
  for (i in rows)
    for (j in cols)
      text(i, j, paste0(prefix, mat[i,j]))
}