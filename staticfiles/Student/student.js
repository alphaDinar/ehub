items.forEach((item, i) => {
  anime({
    translateY: [-50, 0],
    targets: item,
    delay: i * 100,
    duration: 700,
    opacity: [0, 1],
  })

})


runSchemeSearch = (val) => {
  items.forEach(item => {
    if (!item.dataset.name.toLowerCase().includes(val) && !item.dataset.subject.toLowerCase().includes(val)) {
      item.style.display = 'none'
    } else {
      item.style.display = 'flex'
    }
    runAnime(item)
  })
}

runAnime = (item) => {
  anime({
    targets: item,
    translateX: [50, 0],
    opacity: [0, 1],
    duration: 500,
    easing: 'spring(1, 80, 10, 0)',
    begin: () => {
      item.style.transition = 'none'
    },
    complete: () => {
      item.style.transition = '0.4s ease;'
    }
  })
}