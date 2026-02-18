document.addEventListener("change", function (e){
    const input = e.target;

    if(input.type !== "file" || !input.files || !input.files[0]) return;

    const file = input.files[0];


    // mainpreview 

    if(input.id === "id_image"){
        const mainPreview = document.getElementById("main-image-preview");

        if(mainPreview){
            const container = mainPreview.closest(".main-image-container");
            const noPhotoText = container.querySelector(".no-photo-text");

            mainPreview.src = URL.createObjectURL(file);
            mainPreview.style.display = "block";

            mainPreview.style.opacity = "1"

            if(noPhotoText){
                noPhotoText.style.display = 'none'
            }
        }
        return;
    }

    // inlinePreview

    const inlineRow = input.closest(".inline-related, tr.form-row");
    if(!inlineRow) return;

    const preview = inlineRow.querySelectorAll(".inline-preview-img");
    const noPhotoText = inlineRow.querySelector(".no-photo-text");

    preview.forEach(preview => {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    })
    if(noPhotoText){
        noPhotoText.style.display = "none"
    }
})