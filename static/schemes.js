const sideBar = document.querySelector('.sideBar')
const sideBar_tag = document.getElementById('sideBar_tag')

if (sideBar) {
  sideBar_tag.onclick = () => {
    main.classList.toggle('change')
    sideBar.classList.toggle('change')
  }
}

const toggle_main = document.querySelector('.main .con form button')
const main_header = document.querySelector('.main header')
const main_con = document.querySelector('.main .con')

if(toggle_main){
  toggle_main.onclick = () => {
    main.classList.toggle('toggle')
  }
}

const hide_nav = document.getElementById('hide_nav')
const main = document.querySelector('.main')

if (hide_nav) {
  hide_nav.onclick = () => {
    main.classList.toggle('hide')
  }
}

const toggle_stats = document.getElementById('toggle_stats')
const stat_box = document.querySelector('.stat_box')

if (toggle_stats) {
  toggle_stats.onclick = () => {
    stat_box.classList.toggle('change')
  }
}

const image_search = document.querySelector('.image_search')
const image_res = document.querySelectorAll('[id="image_res"]')
const video_search = document.querySelector('.video_search')
const video_res = document.querySelectorAll('[id="video_res"]')
const passage_search = document.querySelector('.passage_search')
const passage_res = document.querySelectorAll('[id="passage_res"]')

if (image_search) {
  image_search.oninput = () => {
    image_res.forEach(el => {
      var el_name = el.dataset.name.toLowerCase()
      if (!el_name.includes(image_search.value.toLowerCase())) {
        el.style.display = 'none'
      } else {
        el.style.display = 'flex'
      }
      runSearchAnime(el)
    })
  }
}

if (video_search) {
  video_search.oninput = () => {
    video_res.forEach(el => {
      var el_name = el.dataset.name.toLowerCase()
      if (!el_name.includes(video_search.value.toLowerCase())) {
        el.style.display = 'none'
      } else {
        el.style.display = 'flex'
      }
      runSearchAnime(el)
    })
  }
}

if (passage_search) {
  passage_search.oninput = () => {
    passage_res.forEach(el => {
      var el_name = el.dataset.name.toLowerCase()
      if (!el_name.includes(passage_search.value.toLowerCase())) {
        el.style.display = 'none'
      } else {
        el.style.display = 'flex'
      }
      runSearchAnime(el)
    })
  }
}

const runSearchAnime = (el) => {
  anime({
    targets: el,
    duration: 500,
    easing: 'spring(1, 80, 10, 0)',
    opacity: [0, 1],
  })
}