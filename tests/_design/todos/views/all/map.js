function (doc) {
	if (doc.doc_type === 'Todo') {
		emit(doc.title, doc.text);
	}
}
