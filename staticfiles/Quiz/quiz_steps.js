// generate steps
let step_tags = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];
generateSteps = (i, question, answers, cor_ans) => {
  var slide_sheet = prefix_1(i, question)
  slide_sheet.id = 'steps_mode'

  var step_box = document.createElement('div')
  step_box.classList.add('step_box')
  step_box.classList.add('material-symbols-outlined')
  step_box.innerHTML = 'list'
  slide_sheet.appendChild(step_box)
  var clear_ans = document.createElement('span')
  clear_ans.id = 'clear_ans'
  clear_ans.innerHTML = 'Clear Answers'
  slide_sheet.appendChild(clear_ans)
  

  var answer_box = document.createElement('div')
  answer_box.classList.add('answer_box')

  // create check list to match stepbox with checked answers
  let check_list = []
  genQ = (ii) => {
    var answer = document.createElement('div')
    answer.classList.add('answer')
    answer_box.appendChild(answer)
    var answer_tag = document.createElement('small')
    answer_tag.innerHTML = step_tags[ii]
    answer.appendChild(answer_tag)
    var answer_text = document.createElement('textarea')
    answer_text.required = true
    answer_text.placeholder = '*'
    if (answers) {
      if (answers[ii]) {
        answer_text.value = answers[ii]
      }
    }
    answer.appendChild(answer_text)
    var answer_label = document.createElement('label')
    answer.appendChild(answer_label)
    var answer_checkbox = document.createElement('input')
    answer_checkbox.type = 'checkbox'
    answer_checkbox.required = true
    answer_checkbox.name = step_tags[ii]

    if (cor_ans) {
      cor_ans.split('').forEach(ans => {
        if (answer_checkbox.name === step_tags[ans]) {
          answer_checkbox.checked = true
          check_list.push(ans)
        }
      })
    }

    answer_label.appendChild(answer_checkbox)
    var ans_check = document.createElement('div')
    ans_check.classList.add('ans_check')
    answer_label.appendChild(ans_check)
    var ans_check_i = document.createElement('i')
    ans_check_i.classList.add('material-symbols-outlined')
    ans_check_i.innerHTML = 'step_out'
    ans_check.appendChild(ans_check_i)
  }


  if (answers) {
    for (var ii = 0; ii < answers.length; ii++) {
      genQ(ii)
    }
  } else {
    for (var ii = 0; ii < 3; ii++) {
      genQ(ii)
    }
  }
  

  if (cor_ans) {
    cor_ans.split('').forEach(ans => {
      if (check_list.includes(ans)) {

        var box = document.createElement('div')
        box.classList.add('box')
        box.id = step_tags[ans]
        box.dataset.index = [ans]
        box.innerHTML = step_tags[ans]
        step_box.appendChild(box)
      }
    })
  }

  slide_sheet.appendChild(answer_box)
  var step_nav = document.createElement('nav')
  step_nav.classList.add('step_nav')
  slide_sheet.appendChild(step_nav)
  var step_nav_add = document.createElement('button')
  step_nav_add.type = 'button'
  step_nav_add.innerHTML = '+'
  step_nav.appendChild(step_nav_add)
  var step_nav_rem = document.createElement('button')
  step_nav_rem.type = 'button'
  step_nav_rem.innerHTML = '-'
  step_nav.appendChild(step_nav_rem)
  create_remove_question(slide_sheet)

  fixSteps()
  runHandleSteps()
}

// fix steps into stepbox
fixSteps = () => {
  const step_questions = document.querySelectorAll('[id="steps_mode"]')
  step_questions.forEach(question => {
    var step_box = question.children[2];
    [...question.children[4].children].forEach((answer, i) => {
      var q_check = answer.children[2].children[0]
      q_check.onchange = () => {
        if (q_check.checked) {
          var box = document.createElement('div')
          box.classList.add('box')
          box.id = step_tags[i]
          box.dataset.index = i
          box.innerHTML = step_tags[i]
          step_box.appendChild(box)
          anime({
            targets: box,
            translateY: [30, 0],
            opacity: [0, 1],
            duration: 600,
          })
        } else {
          [...step_box.children].forEach((box, ii) => {
            if (box.id === step_tags[i]) {
              anime({
                targets: box,
                translateY: [0, 30],
                opacity: [1, 0],
                duration: 400,
                complete: () => {
                  box.remove()
                }
              })
            }
          })
        }
      }

    })
    //clear step box
    question.children[3].onclick = () => {
      step_box.innerHTML = '';
      step_box.innerHTML = 'list';
      [...question.children[4].children].forEach((answer, i) => {
        var q_check = answer.children[2].children[0]
        q_check.checked = false
      })
    }
  })
}
// end of fix steps

//add answer field to steps question
handleSteps = (step_questions, answer_box) => {
  step_questions.forEach((question, i) => {
    if ([...question.children[4].children].length < 8) {
      var answer = document.createElement('div')
      answer.classList.add('answer')
      var answer_tag = document.createElement('small')
      answer_tag.innerHTML = step_tags[[...question.children[4].children].length]
      answer.appendChild(answer_tag)
      var answer_text = document.createElement('textarea')
      answer.appendChild(answer_text)
      var answer_label = document.createElement('label')
      answer.appendChild(answer_label)
      var ans_checkbox = document.createElement('input')
      ans_checkbox.type = 'checkbox'
      ans_checkbox.required = true
      answer_label.appendChild(ans_checkbox)
      var ans_check = document.createElement('div')
      ans_check.classList.add('ans_check')
      answer_label.appendChild(ans_check)
      answer_box[i].appendChild(answer)
      var ans_check_i = document.createElement('i')
      ans_check_i.classList.add('material-symbols-outlined')
      ans_check_i.innerHTML = 'step_out'
      ans_check.appendChild(ans_check_i)
    }
    fixSteps()
  })
}

runHandleSteps = () => {
  const step_questions = document.querySelectorAll('#steps_mode')
  const answer_box = document.querySelectorAll('#steps_mode .answer_box')

  step_questions.forEach((question, i) => {
    question.children[5].children[0].onclick = () => {
      handleSteps(step_questions, answer_box)
    }
    question.children[5].children[1].onclick = () => {
      if ([...question.children[4].children].length > 3) {
        answer_box[i].children[answer_box[i].children.length - 1].remove()
        // fixSteps()
      }
    }
  })
}
// end handle steps