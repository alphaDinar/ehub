runSuperAnime = (grade, i) => {
  anime({
    targets: grade,
    translateY: [-30, 0],
    opacity: [0, 1],
    duration: 1800,
    delay: 30 * i,
    // easing : 'easeInOutExpo'
  })
}

grades.forEach((grade, i) => {
  runSuperAnime(grade, i)
})