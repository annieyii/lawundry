function submitFeatures() {
    const checkboxes1 = document.querySelectorAll('.feature-selection-row1 input[type="checkbox"]');
    const checkboxes2 = document.querySelectorAll('.feature-selection-row2 input[type="checkbox"]');

    // Check if any checkbox is checked in both rows
    const isAnyCheckboxChecked1 = Array.from(checkboxes1).some(checkbox => checkbox.checked);
    const isAnyCheckboxChecked2 = Array.from(checkboxes2).some(checkbox => checkbox.checked);

    console.log('Checkboxes in Row 1 checked:', isAnyCheckboxChecked1);
    console.log('Checkboxes in Row 2 checked:', isAnyCheckboxChecked2);

    const content = document.getElementById('partial-selection');
    const submitButtonContainer = document.getElementById('submit-button-container');
    
    if (isAnyCheckboxChecked1 && isAnyCheckboxChecked2 && submitButtonContainer.style.display === 'block') {
        // 讀取被勾選的圖的img src
        const getImageSrc = (checkboxes) => {
            const checkedCheckboxes = Array.from(checkboxes).find(checkbox => checkbox.checked);
            if (checkedCheckboxes) {
                const label = checkedCheckboxes.nextElementSibling; // Assuming label is directly after checkbox
                const img = label.querySelector('img');
                return img ? img.src : '';
            }
            return '';
        };

        const image1 = document.getElementById('image-feature1');
        const image2 = document.getElementById('image-feature2');

        // Get image sources from checked checkboxes
        const src1 = getImageSrc(checkboxes1);
        console.log('Image src for feature 1:', src1);
        image1.innerHTML = `<img src="${src1}" alt="Image 1" style="width: 100%; height: 100%;">`;

        const src2 = getImageSrc(checkboxes2);
        console.log('Image src for feature 2:', src2);
        image2.innerHTML = `<img src="${src2}" alt="Image 2" style="width: 100%; height: 100%;">`;

        content.style.display = 'block';
    } else {
        content.style.display = 'none';
    }
}