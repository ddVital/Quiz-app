const updateProfilePicBtn = document.querySelector('#updateProfilePicBtn');
const picOptions = document.querySelector('#pic-options');
const deleteNotificationForm = document.querySelector('#deleteNot-form');
const nextQuestionBtn = document.querySelectorAll('.next-question-btn');
const burguerMenuIcon = document.querySelector('#burger-icon');
const menu = document.querySelector('#menu')
const avatarOptions = document.querySelectorAll('.list-options')
const currentQuestion = 0; // name it better

if (burguerMenuIcon) {
  burguerMenuIcon.addEventListener('click', () => {
    menu.classList.toggle("open");
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