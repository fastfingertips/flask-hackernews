function deleteThisRow(_this) {
  var row = _this.parentNode.parentNode;
  row.parentNode.removeChild(row);
  if (document.getElementsByTagName('tbody')[0].childElementCount == 0) {
    window.location.reload();
  }
}