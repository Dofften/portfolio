function showNumber(id) {
  let matches = id.match(/\d+$/);
  const number = "#num" + matches[0];
  $(number).show();
}

function hideNumber(id) {
  let matches = id.match(/\d+$/);
  const number = "#num" + matches[0];
  $(number).hide();
}

function expandPage(clickId) {
  let matches = clickId.match(/\d+$/);
  let htmlArr = ['johnson_j.html', 'river_of_rhythm.html', 'roots.html', 
  'personal_gospel.html', 'boat_film.html', 'music.html',  'blues.html', 'biolever.html', 'onio.html', 'read_beyond_headlines.html','niravo.html','stnicholas.html'];
  const idx = parseInt(matches, 10) - 1;
  location.href = htmlArr[idx];
}

// Check active classes
var checkClass = function() {
  if ( $('.filter_item').hasClass('hide') ) {
    $('.filter_item').removeClass('hide');
  }
};

// Category filters
$('.all').click( function() {
  checkClass();
});
$('.story').click( function() {
  checkClass();
  $('.filter_item:not(.story)').toggleClass('hide');
});
$('.web').click( function() {
  checkClass();
  $('.filter_item:not(.web)').toggleClass('hide');
});
$('.digital').click( function() {
  checkClass();
  $('.filter_item:not(.digital)').toggleClass('hide');
});
$('.branding').click( function() {
  checkClass();
  $('.filter_item:not(.branding)').toggleClass('hide');
});


// Active tag
$('.button').click(function(){
  $('.button').removeClass('active');
  $(this).addClass('active');
})