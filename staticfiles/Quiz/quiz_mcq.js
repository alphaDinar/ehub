// generate mcq's 
generateMcq = (i, question, answers, cor_ans) => {
  var slide_sheet = prefix_1(i, question)
  slide_sheet.id = 'mcq_mode'

  var answer_box = document.createElement('div')
  answer_box.classList.add('answer_box')
  let answer_tags = ['A', 'B', 'C', 'D']
  for (var ii = 0; ii < 4; ii++) {
    var answer = document.createElement('div')
    answer.classList.add('answer')
    answer_box.appendChild(answer)
    var answer_tag = document.createElement('small')
    answer_tag.innerHTML = answer_tags[ii]
    answer.appendChild(answer_tag)
    var answer_text = document.createElement('textarea')
    if (ii < 2) {
      answer_text.placeholder = '*'
      answer_text.required = true
    }
    if (answers) {
      if (answers[ii]) {
        answer_text.value = answers[ii]
       
      }
    }
    // answer_text.name
    answer.appendChild(answer_text)
    var answer_label = document.createElement('label')
    answer.appendChild(answer_label)
    var answer_radio = document.createElement('input')
    answer_radio.type = 'radio'
    if(cor_ans){
      if (answer_text.value === cor_ans) {
        answer_radio.checked = true
      }
    }
    answer_radio.name = `ar${i}`
    answer_label.appendChild(answer_radio)
    var ans_rad = document.createElement('small')
    ans_rad.classList.add('ans_rad')
    ans_rad.classList.add('material-symbols-outlined')
    ans_rad.innerHTML = 'verified'
    answer_label.appendChild(ans_rad)
  }
  slide_sheet.appendChild(answer_box)
  create_remove_question(slide_sheet)
}
// end of generate mcq's