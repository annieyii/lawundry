function toIntroSSIM(image1, image2) {
    // 連接到後端來讀取資料夾名稱
    fetch('/get-folder-name')
        .then(response => response.json())
        .then(data => {
            const folderName = data.folder_name;
            fetch(`/${folderName}/SSIMCUTresult.txt`)
                .then(response => response.text())
                .then(ssimCutData => {
                    const ssimCutValues = ssimCutData.split('\n').map(value => value.trim());
                    fetch(`/${folderName}/SSIMresult.txt`)
                        .then(response => response.text())
                        .then(ssimData => {
                            const ssimValue = ssimData.trim();
                            // 導向新的頁面
                            location.href = `/index/compare/introSSIM?image1=${image1}&image2=${image2}&ssimcut1=${ssimCutValues[0]}&ssimcut2=${ssimCutValues[1]}&ssimcut3=${ssimCutValues[2]}&ssim=${ssimValue}`;                
                        })
                    .catch(error => console.error('Error:', error));
                })
                .catch(error => console.error('Error:', error));
        })
        .catch(error => console.error('Error:', error));
}

function toIntroHSV(image1, image2){
    fetch('/get-folder-name')
        .then(response => response.json())
        .then(data => {
            // const folderName = data.folder_name;
            fetch(`/process-images?image1=${image1}&image2=${image2}`)
            .then(response => response.json())
            .then(data => {
                console.log('Images processed:', data);
                // 導向新的頁面
                location.href = `/index/compare/introHSV?image1=${image1}&image2=${image2}`;
            })
            .catch(error => console.error('Error:', error));
            })
        .catch(error => console.error('Error:', error));
}