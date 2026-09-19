// =====================================
// GT MEDIA ADMIN JAVASCRIPT
// =====================================

// DESIGN FORM
const designForm = document.getElementById("designForm");

if (designForm) {

    designForm.addEventListener("submit", function (event) {

        // IMPORTANT:
        // Do NOT prevent the form from submitting.
        // Flask needs to receive this form.

        // Let the browser submit normally to:
        // /admin/add-design

    });

}


// =====================================
// IMAGE PREVIEW
// =====================================

const designImage = document.getElementById("designImage");
const imagePreview = document.getElementById("imagePreview");

if (designImage && imagePreview) {

    designImage.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) {
            imagePreview.innerHTML = "";
            return;
        }

        const reader = new FileReader();

        reader.onload = function (event) {

            imagePreview.innerHTML = `
                <img
                    src="${event.target.result}"
                    alt="Design Preview"
                    style="
                        max-width: 100%;
                        max-height: 350px;
                        display: block;
                        margin: 15px auto;
                        border-radius: 10px;
                    "
                >
            `;

        };

        reader.readAsDataURL(file);

    });

}