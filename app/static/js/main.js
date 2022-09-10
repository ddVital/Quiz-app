const updateProfilePicBtn = document.querySelector('#updateProfilePicBtn');
const picOptions = document.querySelector('#pic-options');
const deleteNotificationForm = document.querySelector('#deleteNot-form');
const nextQuestionBtn = document.querySelectorAll('.next-question-btn');
const burguerMenuIcon = document.querySelector('#burger-icon'); // burger-icon
const menu = document.querySelector('#menu')
const avatarOptions = document.querySelectorAll('.list-options')
const currentQuestion = 0; // name it better

if (burguerMenuIcon) {
  burguerMenuIcon.addEventListener('click', () => {
    menu.classList.toggle("open");
    burguerMenuIcon.classList.toggle('burguer-open')
  })
}

avatarOptions.forEach(option  => {
  option.addEventListener('change', () => {
    removePreviousSelection()
    option.parentElement.classList.add('selected');
    console.log(option.parentElement);
  })
})

function removePreviousSelection() {
  const selectedOptions = document.querySelectorAll('.selected')

  selectedOptions.forEach(ele => {
    ele.classList.remove('selected');
    console.log(ele);
  })
}

// nextQuestionBtn.forEach(btn => {
//   btn.addEventListener('click', () => {
//     displayQuestion(currentQuestion + 1)
//     // hidePreviousQuestion(currentQuestion)
//   })
// })


function displayQuestion(current) {
  const ele = document.querySelector(`#question-${current}`)
  console.log(ele);
  
  decideIfShowOrHide(ele)
}

function hidePreviousQuestion(current) {
  const ele = document.querySelector(`#question-${current}`)
  
  decideIfShowOrHide(ele)
}

function progressBar(percent) {
  let ele = document.querySelector("#myBar");
  ele.style.width = percent + "%"

}

if (deleteNotificationForm) {
    deleteNotificationForm.addEventListener('submit', (e) => {
        e.preventDefault();
    });
}

nextQuestionBtn.forEach(btn => {
    btn.addEventListener('click', () => {
      let nextQuestion = parseInt(btn.dataset.question) + 1
      let numberOfQuestion = parseInt(btn.dataset.max)
      progressBar((nextQuestion/numberOfQuestion)*100)
      displayQuestion(nextQuestion)
      hidePreviousQuestion(nextQuestion - 1)
    })
})

if (updateProfilePicBtn) { 
  updateProfilePicBtn.addEventListener('click', () => {
    decideIfShowOrHide(picOptions)
  })
}

function profilePictures() {

    decideIfShowOrHide(picOptions);
}

function decideIfShowOrHide(ele) {
    if (ele.classList.contains("visible")) hide(ele)
    else show(ele)
}

function show(ele) {
    ele.classList.add('visible');
    ele.classList.remove('hide');
}

function hide(ele) {
    ele.classList.add('hide');
    ele.classList.remove('visible');
}

// ============================
function scrollEv(leftArrow, rightArrow, carousel) {
  if (carousel.scrollLeft <= 0) {
    leftArrow.classList.add("arrow-inactive");
  } else {
    leftArrow.classList.remove("arrow-inactive");
  }
  if (carousel.scrollLeft >= carousel.scrollWidth - carousel.offsetWidth - 1) {
    rightArrow.classList.add("arrow-inactive");
  } else {
    rightArrow.classList.remove("arrow-inactive");
  }
}
function clicleftArrow(carousel, rectList) {
  let shiftScroll;
  for (let i = 0; i < rectList.length; i++) {
    if (carousel.scrollLeft > rectList[rectList.length - 1]) {
      shiftScroll = rectList[rectList.length - 1];
    } else if (
      carousel.scrollLeft > rectList[i] &&
      carousel.scrollLeft <= rectList[i + 1]
    ) {
      shiftScroll = rectList[i];
    }
  }
  carousel.scrollTo({
    left: shiftScroll,
    behavior: "smooth"
  });
}
function clickRight(carousel, rectList) {
  let shiftScroll;
  for (let i = 0; i < rectList.length; i++) {
    if (
      carousel.scrollLeft >= rectList[i] - 1 &&
      carousel.scrollLeft < rectList[i + 1]
    ) {
      shiftScroll = rectList[i + 1];
    }
  }
  carousel.scrollTo({
    left: shiftScroll,
    behavior: "smooth"
  });
}
function listRectCarousel(carouselNumber, carousels) {
  let divs = carousels[carouselNumber].getElementsByClassName("carousel-item");
  let rectList = [];
  let rectGauche = carousels[carouselNumber].getBoundingClientRect().left;
  for (let i = 0; i < divs.length; i++) {
    let rect = divs[i].getBoundingClientRect();
    rectList.push(rect.left - rectGauche);
  }
  for (let i = rectList.length - 1; i >= 0; i--) {
    rectList[i] = rectList[i] - rectList[0];
  }
  return rectList;
}
function autoSlidePosLeft(carouselNumber, carousels, leftArrows) {
  let rectList = listRectCarousel(carouselNumber, carousels);
  leftArrows[carouselNumber].addEventListener("click", () => {
    clicleftArrow(carousels[carouselNumber], rectList);
  });
}
function autoSlidePosRight(carouselNumber, carousels, rightArrows) {
  let rectList = listRectCarousel(carouselNumber, carousels);
  rightArrows[carouselNumber].addEventListener("click", () => {
    clickRight(carousels[carouselNumber], rectList);
  });
}
window.onload = () => {
  let leftArrows = document.getElementsByClassName("left-arrow");
  let rightArrows = document.getElementsByClassName("right-arrow");
  let carousels = document.getElementsByClassName("carousel");
  for (let i = 0; i < leftArrows.length; i++) {
    autoSlidePosLeft(i, carousels, leftArrows);
    window.onresize = () => {
      autoSlidePosLeft(i, carousels, leftArrows);
    };
  }
  for (let i = 0; i < rightArrows.length; i++) {
    autoSlidePosRight(i, carousels, rightArrows);
    window.onresize = () => {
      autoSlidePosRight(i, carousels, rightArrows);
    };
  }
  for (let i = 0; i < carousels.length; i++) {
    carousels[i].addEventListener("scroll", () => {
      scrollEv(leftArrows[i], rightArrows[i], carousels[i]);
    });
  }
  for (let i = 0; i < carousels.length; i++) {
    scrollEv(leftArrows[i], rightArrows[i], carousels[i]);
    window.onresize = () => {
      scrollEv(leftArrows[i], rightArrows[i], carousels[i]);
    };
  }
  
};