default_image_array = ['10.jpg', '11.jpg', '12.png', '13.png', '14.png', '15.png', '16.png', '1.webp', '2.webp', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg']

String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10);
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+":"+minutes+":"+seconds;
};

function formatFloatToTwoDecimals(value) {
    // Handle different input types
    if (typeof value === 'string') {
        // Remove leading/trailing whitespace
        value = value.trim();
        // Try parsing the string as a number
        const parsedValue = parseFloat(value);
        // Check if parsing was successful (returns NaN if not a number)
        if (!isNaN(parsedValue)) {
            return parsedValue;
        }
    } else if (typeof value === 'number') {
        // Check if it's a finite number
        if (Number.isFinite(value)) {
            // If float, convert to two decimal places
            if (value % 1 !== 0) {
                return value.toFixed(2);
            } else {
                // Ensure the number is within safe integer limits
                const safeNumber = Math.floor(Math.max(Number.MIN_SAFE_INTEGER, Math.min(Number.MAX_SAFE_INTEGER, value)));
                return safeNumber;
            }
        }
    }
    // Return 0 as default for any other input type or parsing failure
    return 0;
}

async function fetchAndSetData(url, data) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const response_data = await response.json();
    return response_data;
  } catch (error) {
    console.error('Error fetching data:', error);
    // Handle errors (display message, retry, etc.)
  }
}

async function updateSpanText(spanElementId, newText) {
  const spanElement = document.getElementById(spanElementId);
  if (spanElement) {
    spanElement.textContent = newText; // Use textContent for plain text updates
  } else {
    console.warn(`Span element with ID "${spanElementId}" not found.`);
  }
}
async function gifted(tcgp_id) {
    var url = "/gifted";
    let data = {
        "tcgp_id": tcgp_id
    };
    response_data = fetchAndSetData(url, data)
}
async function swap_own(event) {
    var url = "/swap_own";
    console.log(event)
    let data = {
        "tcgp_id": event.target.dataset.extraData,
        "own_count": parseInt(event.target.value, 10)
    };
//    response_data = fetchAndSetData(url, data)
}
async function update_have(event) {
    var url = "/update_have";
    let data = {
        "tcgp_id": event.target.dataset.extraData,
        "own_count": parseInt(event.target.value, 10)
    };
    response_data = fetchAndSetData(url, data)
}
async function update_want(event) {
    var url = "/update_want";
    let data = {
        "tcgp_id": event.target.dataset.extraData,
        "state_want": parseInt(event.target.value, 10)
    };
    response_data = fetchAndSetData(url, data)
}
async function update_card_index(event) {
    var url = "/update_card_index";
    let data = {
        "tcgp_id": event.target.dataset.extraData,
        "card_index": parseInt(event.target.value, 10)
    };
    response_data = fetchAndSetData(url, data)
}

async function apply_default_image(imageElement) {
    imageElement.src = "http://192.168.1.175:8000/images/" + default_image_array[Math.floor(Math.random()*default_image_array.length)];
}

async function queryDB(data) {
    document.getElementById("rainbow_loading_bar").hidden = false
    const url = "/get_set_card_list_html";
    let response = await fetch(url, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    }).then(response => response.text())
        .then(htmlContent => {
            const dynamicContent = document.getElementById("card_container");
            dynamicContent.innerHTML = htmlContent;
        })
        .catch(error => console.error(error));
    document.getElementById("rainbow_loading_bar").hidden = true
}
async function generatePack(data) {
    const url = "/generate_pack";
    const dynamicContent = document.getElementById("card_container");
    rainbow_loading_bar = document.getElementById("rainbow_loading_bar")
    rainbow_loading_bar.hidden = false
    const gifImage = document.createElement('img');
    gifImage.src = '/static/pack_opening.gif';
    dynamicContent.innerHTML = ""
    dynamicContent.appendChild(gifImage);
    await new Promise(resolve => setTimeout(resolve, 2000));

    let response = await fetch(url, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    }).then(response => response.text())
        .then(htmlContent => {
            const dynamicContent = document.getElementById("card_container");
            dynamicContent.innerHTML = htmlContent;
        }).catch(error => console.error(error));
    rainbow_loading_bar.hidden = true
}

async function applySortFilter(filter_str) {
    let data = {
        "set_name": document.getElementById("primary_card_set_title").innerText,
        "filter_str": filter_str,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "card_season_search_query": document.getElementById("card_season_search_query_text_field").value,
        "filter_ownership": document.getElementById("filter_ownership").textContent
    };
    queryDB(data)
    updateSpanText("sort_by_selected_item", filter_str)
}
async function generatePackButton(filter_str) {
    let data = {
        "set_name": document.getElementById("primary_card_set_title").innerText,
        "filter_str": filter_str,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "card_season_search_query": document.getElementById("card_season_search_query_text_field").value,
        "filter_ownership": document.getElementById("filter_ownership").textContent,
        "user_id": 1
    };
    generatePack(data)
}
async function applySearchTerm() {
    let data = {
        "set_name": document.getElementById("primary_card_set_title").innerText,
        "filter_str": document.getElementById("sort_by_selected_item").textContent,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "card_season_search_query": document.getElementById("card_season_search_query_text_field").value,
        "filter_ownership": document.getElementById("filter_ownership").textContent
    };
    queryDB(data)
}
async function applySeasonSearchTerm() {
    let data = {
        "set_name": document.getElementById("primary_card_set_title").innerText,
        "filter_str": document.getElementById("sort_by_selected_item").textContent,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "card_season_search_query": document.getElementById("card_season_search_query_text_field").value,
        "filter_ownership": document.getElementById("filter_ownership").textContent
    };
    queryDB(data)
}
async function applyFilterOwnership(filter_ownership) {
    let data = {
        "set_name": document.getElementById("primary_card_set_title").innerText,
        "filter_str": document.getElementById("sort_by_selected_item").textContent,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "card_season_search_query": document.getElementById("card_season_search_query_text_field").value,
        "filter_ownership": filter_ownership
    };
    updateSpanText("filter_ownership", filter_ownership)
    queryDB(data)
}
async function getSetCardList(set_name) {
    let data = {
        "set_name": set_name,
        "filter_str": document.getElementById("sort_by_selected_item").textContent,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "card_season_search_query": document.getElementById("card_season_search_query_text_field").value,
        "filter_ownership": document.getElementById("filter_ownership").textContent
    };
    queryDB(data)
    document.getElementById("primary_card_set_title").textContent = set_name;
};

document.addEventListener("DOMContentLoaded", function(event){
    let data = {
        "set_name": "Base Set (Shadowless)",
        "filter_str": document.getElementById("sort_by_selected_item").textContent,
        "card_name_search_query": "",
        "filter_ownership": ""
    };
    console.log(data)
    queryDB(data)
});



