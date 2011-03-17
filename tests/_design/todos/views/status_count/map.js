function (doc) {
	if (doc.doc_type === 'Todo') {
		emit(doc.done, 1);
	}
}
