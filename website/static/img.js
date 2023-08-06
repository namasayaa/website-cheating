const imgDiv = document.querySelector('.img-circle');
const img = document.querySelector('#photo');
const file = document.querySelector('#file');
const uploadbtn = document.querySelector('#uploadbtn');

file.addEventListener( 'change' , function(){
    const chosenFile = this.files[0];
    if(chosenFile){
        const formData = new FormData();
        formData.append('file', chosenFile);

        fetch('/upload_profile_picture', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    img.setAttribute('src', data.profile_picture_url);
                    window.location.href = '/setting';
                } else {
                    console.error('Error updating profile picture:', data.error);
                }
            })
            .catch(error => {
                console.error('Error uploading profile picture:', error);
            });
    }
});
