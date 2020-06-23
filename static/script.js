/* -------- Bootstrap Val function -------- */
(function() {
    'use strict';
    window.addEventListener('load', () => {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    let forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    let validation = Array.prototype.filter.call(forms, (form) => {
        form.addEventListener('submit', (event) => {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
        form.classList.add('was-validated');
        }, false);
    });
    }, false);
})();

/* ------------ View password ------------ */
function show_hide_password(target){
    let input = document.getElementById('validationCustom04');
    let input2 = document.getElementById('validationCustom05');

    if (input != null){
        if (input.getAttribute('type') === 'password' || input2.getAttribute('type') === 'password') {
            target.classList.add('view');
            input.setAttribute('type', 'text');
            input2.setAttribute('type', 'text');
        } else {
            target.classList.remove('view');
            input.setAttribute('type', 'password');
            input2.setAttribute('type', 'password');
        }
    } else {
        if (input2.getAttribute('type') === 'password') {
            target.classList.add('view');
            input2.setAttribute('type', 'text');
        } else {
            target.classList.remove('view');
            input2.setAttribute('type', 'password');
        }
    }
    return false;
}
function show_hide_password2(target){
    let input = document.getElementById('validationCustom101');

    if (input.getAttribute('type') === 'password') {
        target.classList.add('view');
        input.setAttribute('type', 'text');
    } else {
        target.classList.remove('view');
        input.setAttribute('type', 'password');
    }
    return false;
}

/* ------------ View search ------------ */
function searchView() {
    document.querySelector(".search_form").classList.add("view");
    document.querySelector(".search_text").classList.add("view");
    document.querySelector(".search_text").focus();
    document.querySelector(".search_btn").classList.add("view");
    document.querySelector(".close_b").classList.add("view");
    document.querySelector(".person_form").style.display = "none";
    document.querySelector(".info_form").style.display = "none";
    document.querySelector(".logout_form").style.display = "none";
    document.querySelector(".navigat").classList.add("top");
}
function closeSearchView() {
    // Delete the "view" class from the block of the old result
    if (document.querySelector(".result_block") !== null) {
        RemoveView(".result_block");
    }
    // Delete the block of the old result
    if (document.querySelector(".result_block") !== null) {
        RemoveChild(".result_search");
    }
    // Delete the "view" class from the page list of the old result
    document.querySelector(".pagination").classList.remove("view");
    // Delete the page of the old result
    RemoveChild(".start_page");
    document.querySelector(".search_form").classList.remove("view");
    document.querySelector(".search_text").classList.remove("view");
    document.querySelector(".search_btn").classList.remove("view");
    document.querySelector(".close_b").classList.remove("view");
    document.querySelector(".person_form").style.display = "flex";
    document.querySelector(".info_form").style.display = "flex";
    document.querySelector(".logout_form").style.display = "flex";
    document.querySelector(".navigat").classList.remove("top");
}

/* ------------ View profile ------------ */
function profileView() {
    document.querySelector(".info_form").style.display = "none";
    document.querySelector(".search_form").style.display = "none";
    document.querySelector(".exit").style.display = "none";
    document.querySelector(".person_background").classList.add("view");
    document.querySelector(".navigat").classList.add("top");
    document.querySelector(".close_window").classList.add("view");
    document.querySelector(".person_header").classList.add("view");
    document.querySelector(".others_form").classList.add("view");
    document.querySelector(".person_btn").style.display = "none";
    document.querySelectorAll(".hr")
        .forEach((e) => {
            e.classList.add("view")
        });
    document.querySelector(".reset_pass_email").classList.add("view");
}
function closeProfileView() {
    document.querySelector(".info_form").style.display = "flex";
    document.querySelector(".search_form").style.display = "flex";
    document.querySelector(".exit").style.display = "flex";
    document.querySelector(".person_background").classList.remove("view");
    document.querySelector(".navigat").classList.remove("top");
    document.querySelector(".close_window").classList.remove("view");
    document.querySelector(".person_header").classList.remove("view");
    document.querySelector(".others_form").classList.remove("view");
    document.querySelector(".person_btn").style.display = "flex";
    document.querySelectorAll(".hr")
        .forEach((e) => {
            e.classList.remove("view")
        });
    document.querySelector(".reset_pass_email").classList.remove("view");
}

/* ------------ View info ------------ */
function infoView() {
    document.querySelector(".person_form").style.display = "none";
    document.querySelector(".search_form").style.display = "none";
    document.querySelector(".exit").style.display = "none";
    document.querySelector(".info_background").classList.add("view");
    document.querySelector(".navigat").classList.add("top");
    document.querySelector(".close_window_info").classList.add("view");
    document.querySelector(".row_info_text").classList.add("view");
    document.querySelector(".info_btn").style.display = "none";
}
function closeInfoView() {
    document.querySelector(".person_form").style.display = "flex";
    document.querySelector(".search_form").style.display = "flex";
    document.querySelector(".exit").style.display = "flex";
    document.querySelector(".info_background").classList.remove("view");
    document.querySelector(".navigat").classList.remove("top");
    document.querySelector(".close_window_info").classList.remove("view");
    document.querySelector(".row_info_text").classList.remove("view");
    document.querySelector(".info_btn").style.display = "flex";
}

/* ------------ View review in book page ------------ */
function reviewBackground() {
    document.querySelector(".add_btn_view").style.display = "none";
    document.querySelector(".review_form").classList.add("view");
    document.querySelector(".review_background").classList.add("view");
    document.querySelector(".close_btn_view").classList.add("view");
}
function closeReviewBackground() {
    document.querySelector(".add_btn_view").style.display = "flex";
    document.querySelector(".review_form").classList.remove("view");
    document.querySelector(".review_background").classList.remove("view");
    document.querySelector(".close_btn_view").classList.remove("view");
}

/* ------------ Function add review in book page ------------ */
function addReview(isbn) {
    // Check value form
    if (document.querySelector(".custom-select").value !== "" && document.querySelector(".form-control").value !== "") {
        // Add value in object
        const review = {
            isbn: isbn,
            score: document.querySelector(".custom-select").value,
            text: document.querySelector(".form-control").value
        }
        // Convert to JSON
        const jsonReview = JSON.stringify(review);
        // Send json to server
        sendReview(jsonReview);
    }
}
/* ------------ Function send review from server and return JSON ------------ */
function sendReview(text) {
    // Send POST JSON from server (/page_book)
    $.post("page_book", { text: text }, (data) => {
        // Return data
        // We change the rating
        document.getElementById("rating_score").innerHTML = `${data.score} / ${data.count}`;
        // Create new block "div"
        const resultNewReview = document.createElement("div");
        // Add class "review_result"
        resultNewReview.classList.add("review_result");
        // Add fragment html code
        resultNewReview.innerHTML =
            `<div class="review_header">
                <div class="avatar_review" style="background-image: url(/static/ava/${ data.ava });"></div>
                <div class="name_lastname_review">
                    ${ data.firstname } ${ data.lastname }
                </div>
            </div>
            <hr>
            <div class="text_rev">
                ${ data.text }
            </div>`;
        // New rating percent for stars
        let newPercent = parseFloat(data.score) * 100 / 5;
        // Add style background
        document.querySelector(".rating").style.background = "linear-gradient(to right, #f55f2c " + newPercent +
            "%," + " #f3f3f3 " + (100 - newPercent) + "%)";
        document.querySelector(".rating").style.WebkitBackgroundClip = "text";
        // Add new review and hide botton review
        document.querySelector(".review_block").appendChild(resultNewReview);
        document.querySelector(".review_background").classList.remove("view");
        document.querySelector(".review_background").classList.add("opacity");
        setTimeout(() => {
            document.querySelector(".review_background").style.display = "none";
        }, 200);
    });
}
/* -------- Function search -------- */
function search() {
    // Get value string for search
    let val = document.getElementById("search").value.trim();
    // Convert to JSON
    const json = JSON.stringify(val);
    // Send json to server
    send_data(json);
}
// Page list
let pageList = [];
// List of results in each page
let page = [];

/* -------- Function send requests to server -------- */
function send_data(text) {
    // POST request and receive response
	$.post("search", { name: text }, (data) => {
        // Delete the "view" class from the block of the old result
        if (document.querySelector(".result_block") !== null) {
            RemoveView(".result_block");
        }
        // Delete the block of the old result
        if (document.querySelector(".result_block") !== null) {
            setTimeout(RemoveChild, 200, ".result_search");
        }
        // Delete the "view" class from the page list of the old result
        document.querySelector(".pagination").classList.remove("view");
        // Delete the page of the old result
        RemoveChild(".start_page");
        if (data.length === 0) {
            setTimeout(() => {
                // Create new block "div"
                const resultNewBlock = document.createElement("div");
                // Add class "row" and "result_block"
                resultNewBlock.classList.add("row", "result_block");
                // Add fragment html code
                resultNewBlock.innerHTML =
                    `<div class="col text_result_block" style="text-align: center; align-self: center;">
                            <div class="text_not_found">Sorry, nothing was found :(.</div>
                            <div class="text_not_found_footer"> Try changing the query.</div>
                     </div>`;

                document.querySelector(".result_search").appendChild(resultNewBlock);
                document.querySelector(".result_search").classList.add("view");
                document.querySelector(".result_block").style.height = "200px";
                document.querySelector(".result_block").classList.add("view");
            }, 200);

        } else {
            // Count page number
            let pageCount = 1;
            // Clear the list of result pages
            page = [];

            setTimeout(() => {
                // List cards books
                let card = [];
                // Single page card counter
                let count_card = 0;
                // All value response
                data.forEach((e) => {
                    // Create new block "div"
                    const resultNewBlock = document.createElement("div");
                    // Add class "row" and "result_block"
                    resultNewBlock.classList.add("row", "result_block");
                    // To smoothly change the page, we add the “view” class only for the first 20 results.
                    if (count_card !== 20) {
                        resultNewBlock.classList.add("view");
                        count_card += 1;
                    }
                    let percent = e.average_score * 100 / 5;
                    let color;
                    if (e.average_score > 0)
                    {
                        color = "#f55f2c";
                    } else {
                        color = "#c1c1c1";
                    }
                    // Add fragment html code
                    resultNewBlock.innerHTML =
                        `<a href="/page_book/${ e.isbn }" class="card_result_search">
                            <div class="col-auto img_result_block">
                                <img src="static/img/${ e.img_name }" width="100px" alt="">
                            </div>
                            <div class="col text_result_block">
                                <div class="title">${ e.title } ${ e.year }</div>
                                <div class="author">${ e.author }</div>
                                <div class="rat_star" style="display: flex;">
                                <div class="rating" style="background: linear-gradient(to right, ${ color } ${ percent }%, #c1c1c1  ${ (100 - percent) }%); -webkit-background-clip: text;">
                                    <i id="11" class="fas fa-star"></i>
                                    <i id="12" class="fas fa-star"></i>
                                    <i id="13" class="fas fa-star"></i>
                                    <i id="14" class="fas fa-star"></i>
                                    <i id="15" class="fas fa-star"></i>
                                </div>
                                <div>${ e.average_score.toFixed(2) }</div>
                                </div>
                                <div class="text_less">${ e.less }</div>
                            </div>
                        </a>`;
                    // Form pages by 20 results
                    if (pageCount < 21) {
                        card.push(resultNewBlock);
                        pageCount += 1;
                    }
                    if (pageCount === 21) {
                        page.push(card);
                        card = [];
                        pageCount = 1;
                    }
                });
                // Add card in page
                page.push(card);
                // Add first page in block result_search
                page[0].forEach((e) => {
                    document.querySelector(".result_search").appendChild(e);
                });
                // Count for page list
                let list = 1;
                // Clear the page list
                pageList = [];
                // Create number page for list page
                page.forEach(() => {
                    if (list < 21) {
                        renderPageItem(list);
                        list += 1;
                    } else {
                        renderPageItem(list);
                        list += 1;
                    }
                });
            }, 200);
            // Add class "view" for block "result_search"
            setTimeout(() => {
                document.getElementById('result_search').classList.add('view')
            }, 150);
        }
    });
}

/* -------- Next page function -------- */
function go_page(event) {
    // If the first or last page is selected, then turn off the left and right buttons
    if (event === 1 && pageList.length === 2) {
        document.querySelector('.left_page').classList.add('disabled');
        document.querySelector('.right_page').classList.remove('disabled');
    } else if (event === pageList.length && pageList.length === 2) {
        document.querySelector('.right_page').classList.add('disabled');
        document.querySelector('.left_page').classList.remove('disabled');
    } else if (event === 1 && pageList.length !== 2) {
        document.querySelector('.left_page').classList.add('disabled');
        document.querySelector('.right_page').classList.remove('disabled');
    } else if (event === pageList.length && pageList.length !== 2) {
        document.querySelector('.right_page').classList.add('disabled');
        document.querySelector('.left_page').classList.remove('disabled');
    } else {
        document.querySelector('.left_page').classList.remove('disabled');
        document.querySelector('.right_page').classList.remove('disabled');
    }
    // Delete class "active"
    document.querySelector(".page-item.active").classList.remove('active')
    // Find selected page
    let newActivePage = document.getElementById("page_" + event)
    // Add "active"
    newActivePage.parentElement.classList.add('active')

    if (document.querySelector('.result_block') !== null) {
        // Delete the "view" class from the block of the old result
        RemoveView(".result_block");
        // Delete the block of the old result
        RemoveChild(".result_search");
    }
    // Counter for pages
    let countPN = 0;
    // Move page list provided
    if (pageList.length > 20 && event > 10 && (pageList.length - event) >= 10) {
        // Delete the "view" class from the page list of the old result
        document.querySelector(".pagination").classList.remove("view");
        // Delete the page of the old result
        RemoveChild(".start_page");
        while (countPN !== 20) {
            document.querySelector('.start_page').appendChild(pageList[event - 10 + countPN]);
            document.querySelector(".pagination").classList.add("view");
            countPN += 1;
        }
    }
    // Add search results for the current page
    page[event - 1]
        .forEach((event) => {
            document.querySelector(".result_search").appendChild(event);
        });
    // Add class "view" for result_block
    setTimeout(opacity, 300);
}
/* -------- Function add class "view" only next/previous page -------- */
function opacity() {
    document.querySelectorAll(".result_block")
    .forEach((e) => {
        e.classList.add('view')
    });
}

/* -------- Function delete child parent -------- */
function RemoveChild(classParent) {
    while (document.querySelector(classParent).firstChild) {
        document.querySelector(classParent)
            .removeChild(document.querySelector(classParent)
                .firstChild);
    }
}

/* -------- Function delete class "view" -------- */
function RemoveView(classParent) {
    document.querySelectorAll(classParent)
        .forEach((e) => {
            e.classList.remove('view')
    });
}

/* -------- Function of changing the page to the previous one -------- */
function previous() {
    let active = document.querySelector(".page-item.active");
    let value = parseInt(active.firstElementChild.getAttribute("value"));
    if (value !== 1) {
        go_page(value - 1);
    }
}

/* -------- Next page function -------- */
function next() {
    let active = document.querySelector(".page-item.active");
    let value = parseInt(active.firstElementChild.getAttribute("value"));
    if (value !== pageList.length) {
        go_page(value + 1);
    }
}

function renderPageItem(list) {
    // Create new html block "li"
    const newNumberPage = document.createElement("li");
    // Add Bootstrap class
    document.querySelector('.left_page').classList.add('disabled');
    // Add class no active (Bootstrap), and for first add "active"
    if (list !== 1) {
        newNumberPage.classList.add("page-item");
    } else {
        newNumberPage.classList.add("page-item", "active");
    }
    newNumberPage.innerHTML =
        `<botton id="page_${ list }" class="page-link page_number" value="${ list }" onclick="go_page(${ list })">${ list }</botton>`;
    // Add in list
    pageList.push(newNumberPage);
    if (list < 21) {
        // Add children in block and class "view" for children
        document.querySelector('.start_page').appendChild(newNumberPage);
        document.querySelector(".pagination").classList.add("view");
    }
}




























