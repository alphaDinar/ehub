createQuiz = (quiz_con) => {
  let quiz_json = quiz_con
  quiz_json.forEach((question, qi) => {
    var slide_sheet = document.createElement('div')
    slide_sheet.classList.add('swiper-slide')
    quiz_wrapper.appendChild(slide_sheet)
    var question_tag = document.createElement('span')
    question_tag.innerHTML = `Question ${qi + 1}/${quiz_json.length}`
    question_tag.classList.add('question_tag')
    slide_sheet.appendChild(question_tag)
    if (question.type === 'mcq_mode') {
      slide_sheet.id = 'mcq_mode'
      var question_box = document.createElement('div')
      question_box.classList.add('question_box')
      question_box.innerHTML = question.question
      slide_sheet.appendChild(question_box)

      var answer_box = document.createElement('div')
      answer_box.classList.add('answer_box')
      slide_sheet.appendChild(answer_box)
      let tags = ['A', 'B', 'C', 'D']
      question.answers.forEach((answer, ai) => {
        var answer_label = document.createElement('label')
        answer_box.appendChild(answer_label)
        var answer_radio = document.createElement('input')
        answer_radio.type = 'radio'
        answer_radio.value = answer
        answer_radio.name = `ar${qi}`
        answer_label.appendChild(answer_radio)
        var ans_rad = document.createElement('div')
        ans_rad.classList.add('ans_rad')
        answer_label.appendChild(ans_rad)
        var answer_tag = document.createElement('small')
        answer_tag.innerHTML = tags[ai]
        ans_rad.appendChild(answer_tag)
        var answer_span = document.createElement('span')
        answer_span.innerHTML = answer
        ans_rad.appendChild(answer_span)
        var answer_i = document.createElement('small')
        answer_i.classList.add('material-symbols-outlined')
        answer_i.innerHTML = 'verified'
        ans_rad.appendChild(answer_i)
      })
    } else if (question.type === 'steps_mode') {
      slide_sheet.id = 'steps_mode'
      var question_box = document.createElement('div')
      question_box.classList.add('question_box')
      question_box.innerHTML = question.question
      slide_sheet.appendChild(question_box)

      var step_box = document.createElement('div')
      step_box.classList.add('step_box')
      step_box.classList.add('material-symbols-outlined')
      step_box.innerHTML = 'list'
      slide_sheet.appendChild(step_box)
      var clear_ans = document.createElement('span')
      clear_ans.id = 'clear_ans'
      clear_ans.innerHTML = 'Clear Choice'
      slide_sheet.appendChild(clear_ans)

      var answer_box = document.createElement('div')
      answer_box.classList.add('answer_box')
      slide_sheet.appendChild(answer_box)
      let tags = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];
      question.answers.forEach((answer, ai) => {
        var answer_label = document.createElement('label')
        answer_box.appendChild(answer_label)
        var answer_radio = document.createElement('input')
        answer_radio.type = 'checkbox'
        answer_radio.name = ai
        answer_label.appendChild(answer_radio)
        var ans_rad = document.createElement('div')
        ans_rad.classList.add('ans_rad')
        answer_label.appendChild(ans_rad)
        var answer_tag = document.createElement('small')
        answer_tag.innerHTML = tags[ai]
        ans_rad.appendChild(answer_tag)
        var answer_span = document.createElement('span')
        answer_span.innerHTML = answer
        ans_rad.appendChild(answer_span)
        var answer_i = document.createElement('small')
        answer_i.classList.add('material-symbols-outlined')
        answer_i.innerHTML = 'step_out'
        ans_rad.appendChild(answer_i)
      })
    } else if (question.type === 'fill_in_mode') {
      var fill_in_box = document.createElement('div')
      fill_in_box.classList.add('fill_in_box')
      slide_sheet.id = 'fill_in_mode'
      slide_sheet.appendChild(fill_in_box)
      question.question_list.forEach((que, qi) => {
        var fill_in = document.createElement('div')
        fill_in.classList.add('fill_in')
        fill_in_box.appendChild(fill_in)
        var q = document.createElement('p')
        q.style.minWidth = `${question.width_list[qi]}px`
        q.innerHTML = que
        fill_in.appendChild(q)
        var a = document.createElement('input')
        a.placeholder = `ans ${qi + 1}`
        fill_in.appendChild(a)
      })
    }
    createPagination(qi)
  })
  var submit_sheet = document.createElement('div')
  submit_sheet.classList.add('swiper-slide')
  var submit_button = document.createElement('button')
  submit_button.type = 'submit'
  submit_button.id = 'submit_button'
  submit_button.innerHTML = '<i class="material-symbols-outlined">psychology_alt</i>submit<i class="material-symbols-outlined">psychology_alt</i>'
  submit_sheet.appendChild(submit_button)
  quiz_wrapper.appendChild(submit_sheet)
  var submit_pagination = document.createElement('span')
  submit_pagination.classList.add('material-symbols-outlined')
  submit_pagination.id = 'submit_pagination'
  submit_pagination.innerHTML = 'send'
  page_box.appendChild(submit_pagination)
  makeQuizSwiper()
  fixSteps()
  triggerSave()
  restoreQuizState()
  if (submit_button) {
    submit_button.onclick = () => {
      submitQuiz()
    }
  }
}
createQuiz(quiz_con)
