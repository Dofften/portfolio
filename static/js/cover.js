function showTime() {
  var date = new Date();
  var h = date.getHours(); // 0 - 23
  var m = date.getMinutes(); // 0 - 59
  var s = date.getSeconds(); // 0 - 59
  
  h = (h < 10) ? "0" + h : h;
  m = (m < 10) ? "0" + m : m;
  s = (s < 10) ? "0" + s : s;
  
  var time = h + ":" + m;
  document.getElementById("myClockDisplay").innerText = time;
  document.getElementById("myClockDisplay").textContent = time;
  setTimeout(showTime, 1000);
}
showTime();

function hover(element) {
  element.setAttribute('src', '../images/button-disvovermore-hover.svg');
}

function unhover(element) {
  element.setAttribute('src', '../images/button-disvovermore.svg');
}