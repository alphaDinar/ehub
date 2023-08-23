create_remove_question = (slide_sheet) => {
  var remove_question = document.createElement('i')
  remove_question.classList.add('remove_question')
  remove_question.classList.add('material-symbols-outlined')
  remove_question.innerHTML = 'delete'
  slide_sheet.appendChild(remove_question)
}

prefix_1 = (i, question) => {
  var slide_sheet = document.createElement('div')
  slide_sheet.classList.add('swiper-slide')
  slide_sheet.classList.add('question_slide')

  var question_tag = document.createElement('span')
  question_tag.classList.add('question_tag')
  question_tag.innerHTML = `Question ${i}`
  slide_sheet.appendChild(question_tag)
  var question_box = document.createElement('textarea')
  question_box.placeholder = `Q${i}`
  question_box.required = true
  if (question) {
    question_box.value = question
  }
  question_box.classList.add('question_box')
  slide_sheet.appendChild(question_box)
  quiz_wrapper.appendChild(slide_sheet)

  return slide_sheet
}

createPagination = (counter) => {
  var page_span = document.createElement('span')
  page_span.innerHTML = counter
  page_box.appendChild(page_span)
}


makeQuizSwiper = () => {
  var quiz_swiper = new Swiper('.quiz_box', {
    loop: false,
    speed: 700,
    allowTouchMove: false,
    navigation: {
      nextEl: '.quiz_box_next',
      prevEl: '.quiz_box_prev',
    },
  });

  const page_spans = document.querySelectorAll('.page_box span')
  page_spans.forEach((el, i) => {
    el.onclick = () => {
      quiz_swiper.slideTo(i)
    }
  })
}


