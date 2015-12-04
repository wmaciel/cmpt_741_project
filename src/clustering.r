clusterable_data = read.csv('../data/DocumentWords_onehot_filter_1.csv')
doc_ids = clusterable_data$doc_id
clusterable_data$doc_id = NULL

kc <- kmeans(clusterable_data, 4, nstart=100)
print(kc$size)

clusters_ids = kc$cluster
doc_plus_cluster = c(doc_ids, clusters_ids)
doc_cluster = matrix(doc_plus_cluster, ncol=2)

write.table(doc_cluster, file = "doc_cluster.csv", row.names=FALSE, col.names=FALSE, sep=',')
