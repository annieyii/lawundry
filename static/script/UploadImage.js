let image1Url = '';
let image2Url = '';

function uploadImage(imageBoxId, fileInputId) {
    const fileInput = document.getElementById(fileInputId);
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('box_id', imageBoxId);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 上傳圖片＆顯示圖片
            document.getElementById(imageBoxId).innerHTML = '<img src="' + data.url + '" alt="Uploaded Image" style="width: 100%; height: 100%;">';
            if (imageBoxId === 'image-box1') {
                image1Url = data.url;
            } else if (imageBoxId === 'image-box2') {
                image2Url = data.url;
            }
        } else {
            alert('Image upload failed.');
        }
    })
    .catch(error => {
        console.error('Error uploading image:', error);
        alert('Image upload failed.');
    });
}

function handleSubmit() {
    if (image1Url && image2Url) {
        // 傳送上傳的圖片之後跳轉到compare.html
        const url = `/index/compare?image1=${encodeURIComponent(image1Url)}&image2=${encodeURIComponent(image2Url)}`;
        window.location.href = url;
    } else {
        alert('Please upload both images before submitting.');
    }
}