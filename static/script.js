 var likeBtns = document.getElementsByClassName('form-submit')
 for (let index = 0; index < likeBtns.length; index++) {
     const btn = likeBtns[index];
     btn.addEventListener('click', (e) => {
         // btn.parentElement().submit
         console.log(e.target.parentElement.submit());
     })
     btn.removeEventListener('click', () => {})
 }
 // Comment Section

 var commentBtns = document.querySelectorAll('.comment__toggle')
 commentBtns.forEach(element => {
     element.addEventListener('click', e => toggleComment(e.target))
 });

 function toggleComment(target) {
     let id = target.getAttribute('panel')
     let commentWrapper = document.getElementById(`panel__id-${id}`)
     commentWrapper.classList.toggle('d-none')

 }