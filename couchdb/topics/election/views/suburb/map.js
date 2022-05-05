function (doc) {
  if (doc.suburb !== null){
    emit([doc.suburb,doc.sentiment],1);
  }
}