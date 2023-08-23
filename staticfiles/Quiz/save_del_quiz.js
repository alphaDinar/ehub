//add questions mcq / steps / fill in
add_question.onclick = () => {
  var counter = document.querySelectorAll('.question_slide').length + 1
  if (question_mode.value === 'mcq') {
    generateMcq(counter)
  } else if (question_mode.value === 'steps') {
    generateSteps(counter)
  } else if (question_mode.value === 'fill_in') {
    fill_in_add(generateFill_in(counter), 1)
    handleFill_in()
    delFill_ins()
  }
  createPagination(counter)
  makeQuizSwiper()
  delQuestion()
}
// end questions mcq / steps / fill in

delQuestion = () => {
  const questions = document.querySelectorAll('.quiz_box .swiper-slide')
  const remove_question = document.querySelectorAll('.remove_question')
  const pagination = document.querySelectorAll('.page_box span')

  questions.forEach((question, i) => {
    remove_question[i].onclick = () => {
      anime({
        targets: question,
        scale: [1, 0.5],
        duration: 600,
        complete: () => {
          question.remove()
          pagination[i].remove()
          let questions_left = document.querySelectorAll('.quiz_box .swiper-slide')
          let paginations_left = document.querySelectorAll('.page_box span')
          questions_left.forEach((q, i) => {
            q.children[0].innerHTML = `Question ${i + 1}`
            q.children[1].placeholder = `Q${i + 1}`
          })
          paginations_left.forEach((span, i) => {
            span.innerHTML = i + 1
          })
          makeQuizSwiper()
        }
      })
    }
  })
}


