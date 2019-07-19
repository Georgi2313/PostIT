const shareButton = document.querySelector('.share-button');
const shareDialog = document.querySelector('.share-dialog');
const closeButton = document.querySelector('.close-button');
const shareData = { files: 'https://postit.pythonanywhere.com/media/images/pythonanywhere.jpg' };


shareButton.addEventListener('click', event => {
  if (navigator.share) { 
   navigator.share({
      title: 'PostIT (title)',
      text: 'sample text',
      url: 'https://postit.pythonanywhere.com',
      files: 'https://postit.pythonanywhere.com/media/images/pythonanywhere.jpg', 
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