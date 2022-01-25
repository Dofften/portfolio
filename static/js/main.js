// var prevScrollpos = window.pageYOffset;
//   window.onscroll = function() {
//   var currentScrollPos = window.pageYOffset;
//   if (prevScrollpos > currentScrollPos) {
//     document.getElementById("navbar").style.top = "0";
//   } else {
//     document.getElementById("navbar").style.top = "-100px";
//   }
//   prevScrollpos = currentScrollPos;
// }

function showOptions(clickId) {
  if (clickId == 'myMenu') {
    $('#bgId').hide();
    $('#optionpage').show();
  }
}

function closeOptions(clickId) {
  if (clickId == 'closeId') {
    $('#optionpage').hide();
    $('#bgId').show();
  }
}

function backToLastPage(clickId) {
  location.href = 'project.html' + '#pid' + clickId;
}

// copy email function.
function copyEmail() {
  var ele = document.getElementById("myEmail");
  var eleText = "frankomondi311@gmail.com";
  copyText(eleText);

  var tooltip = document.getElementById("myTooltip");
  tooltip.innerHTML = "Copied: " + eleText;
}

function copyText(text) {
  navigator.clipboard.writeText(text);
}

function outFunc() {
  var tooltip = document.getElementById("myTooltip");
  tooltip.innerHTML = "Copy to clipboard";
}