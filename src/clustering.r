clusterable_data = read.csv('../data/DocumentWords_onehot_filter_100.csv')

kc <- kmeans(clusterable_data, 4, algorithm="Hartigan-Wong")
kc$sizes

doc_ids = clusterable_data[,c(1)]
clusters_ids = kc$cluster
doc_plus_cluster = c(doc_ids, clusters_ids)
doc_cluster = matrix(doc_plus_cluster, ncol=2)

write.table(doc_cluster, file = "doc_cluster.csv", row.names=FALSE, col.names=FALSE, sep=',')
