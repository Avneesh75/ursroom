function openNav() {
    document.getElementById("mySidepanel").style.width = "250px";
  }
  
  function closeNav() {
    document.getElementById("mySidepanel").style.width = "0";
  }

  $('#myTab a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
  })


// Room Slider Part
var swiper = new Swiper(".gallery_slider", {
  cssMode: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  loop: true,
  pagination: {
    el: ".swiper-pagination",
  },
  autoPlay:{
    delay: 3000,
  },
  
  mousewheel: true,
  keyboard: true,
  
});

const homeSlider = new Swiper(".home_slider", {
  cssMode: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  loop: true,
  pagination: {
    el: ".swiper-pagination",
  },
  autoPlay:{
    delay: 3000,
  },
  mousewheel: true,
  keyboard: true,
});

setInterval(function() {
  swiper.slideNext(3000, true);
}, 3000);

setInterval(function() {
  homeSlider.slideNext(3000, true);
}, 3000);


function searchPage(){
  let page = document.getElementById('pageSearchFilter').value;
  if(page ==="room")
  window.open('ursroom-details-share');
  if(page ==="boys,girls,works");
  window.open('ursroom-details-share');
  if(page ==="room for boys,room for girls,room for work professionla");
  window.open('ursroom-details-share');
}

document.getElementById("testimonial-slide-left").addEventListener("click", () => {
  document.getElementById("testimonials").scrollLeft -= 300;
});

document.getElementById("testimonial-slide-right").addEventListener("click", () => {
  document.getElementById("testimonials").scrollLeft += 300;
});