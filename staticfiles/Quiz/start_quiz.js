const quiz_box = document.querySelector('.quiz_box')
const quiz_wrapper = document.querySelector('.quiz_box .swiper-wrapper')
const page_box = document.querySelector('.page_box')

createPagination = (counter) => {
  var page_span = document.createElement('span')
  page_span.innerHTML = counter + 1
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
      sessionStorage.setItem('current_slide', i)
    }
  })

  if (sessionStorage.getItem('current_slide')) {
    quiz_swiper.slideTo(sessionStorage.getItem('current_slide'))
  }
}

autoSaveQuiz = () => {
  let answer_box = []
  document.querySelectorAll('.quiz_box .swiper-slide').forEach(question_slide => {
    if (question_slide.id === 'mcq_mode') {
      var choiceBox = [];
      [...question_slide.children[2].children].forEach(answer => {
        var ans_rad = answer.children[0]
        if (ans_rad.checked) {
          choiceBox.push(ans_rad.value)
          choice = ans_rad.value
        }
      })
      if (choiceBox.length < 1) {
        answer_box.push('')
      } else {
        answer_box.push(choiceBox[0])
      }
    } else if (question_slide.id === 'steps_mode') {
      var cor_ans = '';
      [...question_slide.children[2].children].forEach(step_child => {
        cor_ans = cor_ans + `${step_child.dataset.index}`
      })
      answer_box.push(cor_ans)
    } else if (question_slide.id === 'fill_in_mode') {
      let answer_list = [];
      [...question_slide.children[1].children].forEach(fill_in => {
        answer_list.push(fill_in.children[1].value)
      })
      answer_box.push(answer_list)
    }
  })
  sessionStorage.setItem('answer_box', JSON.stringify(answer_box))
  return answer_box
}

restoreQuizState = () => {
  if (sessionStorage.getItem('answer_box')) {
    var answer_box = JSON.parse(sessionStorage.getItem('answer_box'))

    document.querySelectorAll('.quiz_box .swiper-slide').forEach((question_slide, qi) => {
      if (question_slide.id === 'mcq_mode') {
        [...question_slide.children[2].children].forEach(answer => {
          var ans_rad = answer.children[0]
          if (ans_rad.value === answer_box[qi]) {
            ans_rad.checked = true
          }
        })
      } else if (question_slide.id === 'steps_mode') {
        let step_tags = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];
        var step_box = question_slide.children[2];
        let answers = [...question_slide.children[4].children]
        answer_box[qi].split('').forEach((el, i) => {
          answers.forEach(answer => {
            var ans = answer.children[0]
            if (ans.name === el) {
              ans.checked = true
              var box = document.createElement('div')
              box.id = step_tags[ans.name]
              box.classList.add('box')
              box.dataset.index = ans.name
              box.innerHTML = step_tags[ans.name]
              step_box.appendChild(box)
            }
          })
        });
      } else if (question_slide.id === 'fill_in_mode') {
        [...question_slide.children[1].children].forEach((fill_in, i) => {
          var ans = fill_in.children[1]
          ans.value = answer_box[qi][i]
        })
      }
    })
  }
}
restoreQuizState()


fixSteps = () => {
  const step_questions = document.querySelectorAll('[id="steps_mode"]')
  let step_tags = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];
  step_questions.forEach(question => {
    var step_box = question.children[2];
    [...question.children[4].children].forEach((answer, i) => {
      var q_check = answer.children[0]
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
            complete: () => {
              autoSaveQuiz()
            }
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
                  autoSaveQuiz()
                }
              })
            }
          })
        }
      }

    })
    //clear step box
    question.children[3].onclick = () => {
      console.log(step_box)
      step_box.innerHTML = '';
      step_box.innerHTML = 'list';
      [...question.children[4].children].forEach((answer, i) => {
        var q_check = answer.children[0]
        q_check.checked = false
      })
      autoSaveQuiz()
    }
  })
}



triggerSave = () => {
  document.querySelectorAll('input').forEach(input => {
    input.oninput = () => {
      autoSaveQuiz()
    }
  })
}