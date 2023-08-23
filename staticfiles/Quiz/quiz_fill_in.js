// generate fill_in
generateFill_in = (i) => {
  var slide_sheet = document.createElement('div')
  slide_sheet.classList.add('swiper-slide')
  slide_sheet.classList.add('question_slide')
  slide_sheet.id = 'fill_in_mode'
  var question_tag = document.createElement('span')
  question_tag.classList.add('question_tag')
  question_tag.innerHTML = `Question ${i}`
  slide_sheet.appendChild(question_tag)
  var fill_in_box = document.createElement('div')
  fill_in_box.classList.add('fill_in_box')
  slide_sheet.appendChild(fill_in_box)

  var addFill_button = document.createElement('button')
  addFill_button.innerHTML = '+'
  addFill_button.type = 'button'
  slide_sheet.appendChild(addFill_button)
  create_remove_question(slide_sheet)

  quiz_wrapper.appendChild(slide_sheet)

  return fill_in_box
}

fill_in_add = (fill_in_box, counter, mini_q, mini_a, width) => {
  var fill_in = document.createElement('p')
  fill_in.classList.add('fill_in')
  fill_in_box.appendChild(fill_in)
  var fill_in_tag = document.createElement('span')
  fill_in_tag.innerHTML = counter
  fill_in.appendChild(fill_in_tag)
  var new_textarea = document.createElement('textarea')
  new_textarea.placeholder = `Statement ${counter}`
  new_textarea.required = true

  if (mini_q) {
    new_textarea.value = mini_q
    new_textarea.style.width = `${width}px`
  }
  fill_in.appendChild(new_textarea)
  var new_input = document.createElement('input')
  new_input.placeholder = `blank ${counter}`
  new_input.required = true
  if (mini_a) {
    new_input.value = mini_a
  }
  fill_in.appendChild(new_input)
  var fill_in_del = document.createElement('small')
  fill_in_del.classList.add('material-symbols-outlined')
  fill_in_del.innerHTML = 'delete'
  fill_in.appendChild(fill_in_del)
}

handleFill_in = () => {
  const fill_in_boxes = document.querySelectorAll('.fill_in_box')
  const addFill_button = document.querySelectorAll('#fill_in_mode button')

  fill_in_boxes.forEach((fill_in_box, i) => {
    addFill_button[i].onclick = () => {
      console.log('aasc')
      var counter = fill_in_box.children.length + 1
      fill_in_add(fill_in_box, counter)
      delFill_ins()
    }
  })

}

delFill_ins = () => {
  document.querySelectorAll('.fill_in_box').forEach(fill_in_box => {
    [...fill_in_box.children].forEach((el, i) => {
      el.children[3].onclick = () => {
        el.remove();
        [...fill_in_box.children].forEach((mini_el, ii) => {
          var counter = parseInt(ii + 1)
          mini_el.children[0].innerHTML = counter
          mini_el.children[1].placeholder = `blank ${counter}`
          mini_el.children[2].placeholder = `ans ${counter}`
        })
      }
    })
  })
}
//end of generate fill_in