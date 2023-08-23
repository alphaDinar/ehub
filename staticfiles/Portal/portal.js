const pass1 = document.querySelector('.pass1')
const pass2 = document.querySelector('.pass2')
const pass_prompt = document.getElementById('pass_prompt')

const teacherForm = document.getElementById('teacher_form')
const teacherFormButton = document.querySelector('#teacher_form button')

teacherForm.onsubmit = (event) => {
  event.preventDefault()
}

teacherFormButton.onclick = () => {
  // if (pass1.value != pass2.value) {
  //   console.log('pass Dont match')
  // }
  if (course_box.children.length < 1) {
    course_box.innerHTML = `<span style="font-weight:600;padding:5px; background:whitesmoke;color:salmon;">Add a Course</span> `
  }
  else {
    if (teacherForm.checkValidity()) {
      teacherForm.submit()
    }
  }
}

// pass1.oninput = () => {
//   passMatch()
// }
// pass2.oninput = () => {
//   passMatch()
// }

// passMatch = () => {
//   if (pass2.value.length > 0) {
//     if (pass1.value != pass2.value) {
//       pass_prompt.innerHTML = 'dangerous'
//       pass_prompt.style.color = 'salmon'
//     } else {
//       pass_prompt.innerHTML = 'verified'
//       pass_prompt.style.color = 'springgreen'
//     }
//     anime({
//       targets: pass_prompt,
//       translateY: [30, 0],
//       opacity: [0, 1],
//       duration: 400
//     })
//   }
// }
