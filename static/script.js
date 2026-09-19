// =====================================
// GT MEDIA PUBLIC PORTFOLIO
// =====================================


// =====================================
// ELEMENTS
// =====================================

const categoryButtons =
    document.querySelectorAll(".category");

const designCards =
    document.querySelectorAll(".design-card");

const designSearch =
    document.getElementById("designSearch");

const clearSearch =
    document.getElementById("clearSearch");

const noSearchResults =
    document.getElementById("noSearchResults");


// =====================================
// CURRENT FILTER
// =====================================

let selectedCategory = "all";


// =====================================
// FILTER DESIGNS
// =====================================

function filterDesigns() {

    const searchText =
        designSearch
            ? designSearch.value.trim().toLowerCase()
            : "";

    let visibleDesigns = 0;


    designCards.forEach(function (card) {

        const title =
            (card.dataset.title || "").toLowerCase();

        const category =
            (card.dataset.category || "").toLowerCase();

        const description =
            (card.dataset.description || "").toLowerCase();


        // CATEGORY MATCH

        const categoryMatch =
            selectedCategory === "all" ||
            category === selectedCategory;


        // SEARCH MATCH

        const searchMatch =
            searchText === "" ||
            title.includes(searchText) ||
            category.includes(searchText) ||
            description.includes(searchText);


        // FINAL MATCH

        if (categoryMatch && searchMatch) {

            card.style.display = "";

            visibleDesigns++;

        } else {

            card.style.display = "none";

        }

    });


    // SHOW / HIDE NO RESULTS MESSAGE

    if (noSearchResults) {

        if (designCards.length > 0 && visibleDesigns === 0) {

            noSearchResults.classList.add("show");

        } else {

            noSearchResults.classList.remove("show");

        }

    }


    // SHOW / HIDE CLEAR BUTTON

    if (clearSearch) {

        if (searchText.length > 0) {

            clearSearch.classList.add("show");

        } else {

            clearSearch.classList.remove("show");

        }

    }

}


// =====================================
// CATEGORY FILTER
// =====================================

categoryButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        // Remove active class

        categoryButtons.forEach(function (btn) {

            btn.classList.remove("active");

        });


        // Add active class

        this.classList.add("active");


        // Get category

        selectedCategory =
            this.dataset.category;


        // Apply filters

        filterDesigns();

    });

});


// =====================================
// SEARCH
// =====================================

if (designSearch) {

    designSearch.addEventListener(
        "input",
        function () {

            filterDesigns();

        }
    );

}


// =====================================
// CLEAR SEARCH
// =====================================

if (clearSearch) {

    clearSearch.addEventListener(
        "click",
        function () {

            designSearch.value = "";

            filterDesigns();

            designSearch.focus();

        }
    );

}


// =====================================
// IMAGE MODAL
// =====================================

const imageModal =
    document.getElementById("imageModal");

const modalImage =
    document.getElementById("modalImage");

const modalTitle =
    document.getElementById("modalTitle");

const modalCategory =
    document.getElementById("modalCategory");

const modalDescription =
    document.getElementById("modalDescription");

const modalClose =
    document.getElementById("modalClose");


designCards.forEach(function (card) {

    const image =
        card.querySelector("img");


    if (!image) {
        return;
    }


    image.addEventListener(
        "click",
        function () {

            const title =
                card.dataset.title;

            const category =
                card.dataset.type;

            const description =
                card.dataset.description || "";


            modalImage.src =
                image.src;

            modalImage.alt =
                title;


            modalTitle.textContent =
                title;

            modalCategory.textContent =
                category;

            modalDescription.textContent =
                description;


            imageModal.classList.add(
                "active"
            );

        }
    );

});


// =====================================
// CLOSE MODAL
// =====================================

if (modalClose) {

    modalClose.addEventListener(
        "click",
        function () {

            imageModal.classList.remove(
                "active"
            );

        }
    );

}


// =====================================
// CLOSE MODAL OUTSIDE
// =====================================

if (imageModal) {

    imageModal.addEventListener(
        "click",
        function (event) {

            if (
                event.target === imageModal
            ) {

                imageModal.classList.remove(
                    "active"
                );

            }

        }
    );

}


// =====================================
// CLOSE WITH ESC
// =====================================

document.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Escape") {

            if (imageModal) {

                imageModal.classList.remove(
                    "active"
                );

            }

        }

    }
);