const shareButton = document.querySelector('.share-button');
const shareDialog = document.querySelector('.share-dialog');
const closeButton = document.querySelector('.close-button');
var img = "https://postit.pythonanywhere.com/media/images/pythonanywhere.jpg"


shareButton.addEventListener('click', event => {
  if (navigator.share) { 
   navigator.share({
      title: "{{ post.title }}",
      text: "{{ post.body }}",
      image: img,  mimeType: 'image/jpg'

    }).then(() => {
      console.log('Thanks for sharing!');
    })
    .catch(console.error);
    } else {
        shareDialog.classList.add('is-open');
    }
});

closeButton.addEventListener('click', event => {
  shareDialog.classList.remove('is-open');
});