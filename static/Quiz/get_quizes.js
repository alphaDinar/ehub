const add_quiz = document.querySelector('.add_quiz')
const show_add_quiz = () => {
  add_quiz.classList.add('show')
}
const close_add_quiz = () => {
  add_quiz.classList.remove('show')
}


const item_in = document.getElementById('item_in')
const item_select = document.getElementById('item_select')
const items = document.querySelectorAll('#item')

item_in.oninput = () => {
  items.forEach(el => {
    var el_name = el.dataset.name.toLowerCase()
    if (!el_name.includes(item_in.value)) {
      el.style.display = 'none'
    } else {
      el.style.display = 'flex'
    }
    runSearchAnime(el)
  })
}

item_select.onchange = () => {
  items.forEach(el => {
    var el_status = el.dataset.status.toLowerCase()
    if (item_select.value === 'all') {
      el.style.display = 'flex'
    } else {
      if (el_status != item_select.value.toLowerCase()) {
        el.style.display = 'none'
      } else {
        el.style.display = 'flex'
      }
    }
    runSearchAnime(el)
  })
}

items.forEach((el, i) => {
  anime({
    targets: el,
    translateX: [-50, 0],
    opacity: [0, 1],
    duration: 300,
    easing: 'spring(1, 80, 10, 0)',
    delay: i * 100
  })
})

document.querySelectorAll('.main header .box').forEach((el, i) => {
  anime({
    targets: el,
    translateY: [-50, 0],
    opacity: [0, 1],
    scale: [0.8, 1],
    duration: 500,
    easing: 'spring(1, 80, 10, 0)',
    delay: i * 100
  })
})

