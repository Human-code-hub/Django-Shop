document.addEventListener("change", function (e){
    const input = e.target;

    if(input.type !== "file" || !input.files || !input.files[0]) return;

    const file = input.files[0];

    // mainpreview

    if(!input.closest(".inline-related, tr.form-row")){
        const mainPreview = document.getElementById("main-image-preview");
        const noPhotoText = mainPreview?.nextElementSibling;

        if(mainPreview){
            mainPreview.src = URL.createObjectURL(file);
            mainPreview.style.display = 'block';
        };
        if(noPhotoText && noPhotoText.classList.contains("no-photo-text")){
            noPhotoText.style.display = "none"
        };
        return;
    }

    // inlinepreview
    const inlineRow = input.closest(".inline-related, tr.form-row");
    if(!inlineRow) return;

    const preview = inlineRow.querySelectorAll(".inline-preview-img");
    const noPhotoText = inlineRow.querySelector(".no-photo-text");

    preview.ForEach(preview =>{
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block"
    });
    if(noPhotoText){
        noPhotoText.style.display = "none"
    }
})