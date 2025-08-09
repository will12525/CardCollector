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
/**
 * A utility object for managing cookies.
 * Provides getter and setter functions to easily access and modify cookies.
 */
const cookieManager = {
  /**
   * Sets a cookie with a given name, value, and optional expiration days.
   * @param {string} name - The name of the cookie.
   * @param {string} value - The value to store in the cookie.
   * @param {number} [days] - The number of days until the cookie expires. If not provided, it's a session cookie.
   */
  set: function(name, value, days) {
    let expires = "";
    if (days) {
      const date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  },

  /**
   * Gets the value of a cookie with a given name.
   * @param {string} name - The name of the cookie to retrieve.
   * @returns {string|null} The value of the cookie, or null if the cookie is not found.
   */
  get: function(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) {
        return c.substring(nameEQ.length, c.length);
      }
    }
    return null;
  }
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

function createEditableTable(set_name, jsonData) {
    let set_cards = jsonData["set_cards"]; // Store the JSON data globally for further use
    // Create a container for the table and save button
    const container = document.createElement('div');

    // Create the table element
    const table = document.createElement('table');
    table.border = '1';

    // Extract unique keys for table headers
    const fields = jsonData["fields"]

    // Create the table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    fields.forEach((field, index) => {
        const th = document.createElement('th');
        th.textContent = field;
        th.style.cursor = 'pointer'; // Indicate that the header is clickable

        // Add sorting functionality
        th.addEventListener('click', () => {
            const isAscending = th.dataset.sortOrder !== 'asc';
            th.dataset.sortOrder = isAscending ? 'asc' : 'desc';

            // Sort rows based on the column
            set_cards.sort((a, b) => {
                const valA = a[field];
                const valB = b[field];

                if (valA < valB) return isAscending ? -1 : 1;
                if (valA > valB) return isAscending ? 1 : -1;
                return 0;
            });

            // Re-render the table body
            renderTableBody();
        });

        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create the table body
    const tbody = document.createElement('tbody');
    table.appendChild(tbody);

    function renderTableBody() {
        tbody.innerHTML = ''; // Clear existing rows
        set_cards.forEach((row, rowIndex) => {
            const tr = document.createElement('tr');
            tr.dataset.card_id = row["id"];
            fields.forEach(key => {
                const td = document.createElement('td');

                if (key === 'card_class') { // Example: Make 'card_class' a dropdown
                    const select = document.createElement('select');
                    ['creature', 'trainer', 'energy'].forEach(optionValue => {
                        const option = document.createElement('option');
                        option.value = optionValue;
                        option.textContent = optionValue;
                        select.appendChild(option);
                    });
                    select.value = row[key]; // Set the current value
                    select.dataset.key = key;
                    select.dataset.rowIndex = rowIndex;
                    td.appendChild(select);
                    tr.appendChild(td);
                } else if (key === 'card_rarity') { // Example: Make 'card_class' a dropdown
                    const select = document.createElement('select');
                    jsonData["card_rarity"].forEach(optionValue => {
                        const option = document.createElement('option');
                        option.value = optionValue;
                        option.textContent = optionValue;
                        select.appendChild(option);
                    });
                    select.value = row[key]; // Set the current value
                    select.dataset.key = key;
                    select.dataset.rowIndex = rowIndex;
                    td.appendChild(select);
                    tr.appendChild(td);
                } else if (key === 'card_type') { // Example: Make 'card_class' a dropdown
                    const select = document.createElement('select');
                    jsonData["card_type"].forEach(optionValue => {
                        const option = document.createElement('option');
                        option.value = optionValue;
                        option.textContent = optionValue;
                        select.appendChild(option);
                    });
                    select.value = row[key]; // Set the current value
                    select.dataset.key = key;
                    select.dataset.rowIndex = rowIndex;
                    td.appendChild(select);
                } else if (key === 'id' || key === 'tcgp_id' || key === 'set_id' || key === 'set_index' || key === 'set_name' || key === 'set_card_count') { // Example: Disable 'id' and 'tcgp_id'
                    const input = document.createElement('input');
                    input.value = row[key];
                    input.type = typeof row[key] === 'number' ? 'number' : 'text';
                    input.disabled = true; // Disable the field
                    td.appendChild(input);
                    tr.appendChild(td);
                } else if (key === 'tcgp_path') { // Display an image and make it clickable
                    const link = document.createElement('a');
                    let url = `https://www.tcgplayer.com/product/${row['tcgp_id']}/pokemon-${row[key]}`;
                    link.href = url; // Set the URL
                    link.target = '_blank'; // Open in a new tab
                    let img_url = `https://tcgplayer-cdn.tcgplayer.com/product/${row['tcgp_id']}_200w.jpg`
                    const img = document.createElement('img');
                    img.src = img_url; // Set the image source
                    img.alt = 'Image'; // Set alt text for accessibility
                    img.style.width = '70px'; // Adjust image size
                    img.style.height = '100px';

                    link.appendChild(img);
                    td.appendChild(link);
                    tr.insertBefore(td, tr.firstChild);
                } else {
                    const input = document.createElement('input');
                    input.value = row[key];
                    input.type = typeof row[key] === 'number' ? 'number' : 'text';
                    input.dataset.key = key;
                    input.dataset.rowIndex = rowIndex;
                    td.appendChild(input);
                    tr.appendChild(td);
                }
                tr.appendChild(td);

            });
            tbody.appendChild(tr);
        });
    }
    renderTableBody();

    // Create the save button
    const saveButton = document.createElement('button');
    saveButton.textContent = 'Save';
    saveButton.addEventListener('click', () => {
        const updatedData = [];
        tbody.querySelectorAll('tr').forEach((tr, rowIndex) => {
            const rowData = {};
            rowData["id"] = parseFloat(tr.dataset.card_id)
            tr.querySelectorAll('input, select').forEach(element => {
                const key = element.dataset.key;
                const value = element.tagName === 'SELECT' ? element.value :
                              element.type === 'number' ? parseFloat(element.value) : element.value;
                rowData[key] = isNaN(value) ? element.value : value; // Ensure integers remain integers
            });
            updatedData.push(rowData);
        });
        response_data = fetchAndSetData("/editor/save_set", updatedData);
        console.log(response_data); // Replace this with a function to update the database
    });

    // Append the table and button to the container
    container.appendChild(saveButton);
    container.appendChild(table);

    // Append the container to the body or a specific element
    document.getElementById("card_container").innerHTML = "";
    document.getElementById("card_container").appendChild(container);
    document.getElementById("rainbow_loading_bar").hidden = true

}
function load_set(set_name){
    var url = "/editor/load_set";
    response_data = fetchAndSetData(url, {"set_name": set_name})
    response_data.then(data => {
        if (data) {
            createEditableTable(set_name, data);
        } else {
            console.error("No set data found or invalid response format.");
        }
    });
    cookieManager.set("set_name", set_name);
    document.getElementById("primary_card_set_title").textContent = set_name;
}
function handleImageClick(imgElement) {
    const imageType = imgElement.getAttribute("data-collection-type");
    // Perform actions with the imgElement
    const deckInput = document.getElementById("deck_list_dropdown_selected_deck");
    if (deckInput && !document.getElementById("deck_navbar").hidden) {
        var deck_id = deckInput.getAttribute("data-deck-id");

        if (imageType === "collection") {
            let data = {"action_id": 2, "deck_id": parseInt(deck_id, 10), "card_id": parseInt(imgElement.getAttribute("data-card-id"), 10), "user-collection-id": parseInt(imgElement.getAttribute("data-user-collection-id"), 10), };
            queryDeckBuilder(data)
            // Handle collection-specific logic here
        } else if (imageType === "deck") {
            let data = {"action_id": 3, "deck_id": parseInt(deck_id, 10), "card_id": parseInt(imgElement.getAttribute("data-card-id"), 10), };
            queryDeckBuilder(data)
            // Handle deck-specific logic here
        } else {
            console.log("Unknown image type:", imgElement);
        }
    }
}

function clearDeckContainer() {
    const deckInput = document.getElementById("deck_list_dropdown_selected_deck");
    const deck_scroll_container_card_list = document.getElementById("deck_scroll_container_card_list");
    if (deck_scroll_container_card_list) {
        deck_scroll_container_card_list.innerHTML = "";
    }
    if (deckInput) {
        deckInput.value = "";
        deckInput.setAttribute("data-deck-id", "");
    }
}

async function queryDeckBuilder(data) {
    const url = "/get_deck_data_html";
    console.log(data)
    let response = await fetch(url, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    }).then(response => {
        const contentType = response.headers.get("Content-Type");
        if (contentType && contentType.includes("application/json")) {
            return response.json(); // Parse JSON if the response is JSON
        } else if (contentType && contentType.includes("text/html")) {
            return response.text(); // Parse text if the response is HTML
        } else {
            throw new Error("Unsupported content type: " + contentType);
        }
    }).then(content => {
        if (typeof content === "object") {
            // Handle JSON content
            console.log("JSON response:", content);
        } else {
            const dynamicContent = document.getElementById("deck_container");
            dynamicContent.innerHTML = content;
            const deckInput = document.getElementById("deck_list_dropdown_selected_deck");
            const new_deck_button = document.getElementById("new_deck_button");
            if (new_deck_button) {
                new_deck_button.addEventListener("click", function() {
                    clearDeckContainer()
                });
            }
            if (deckInput) {
                // User presses "Enter"
                deckInput.addEventListener("keydown", function(e) {
                    if (e.key === "Enter") {
                        const deckId = deckInput.getAttribute("data-deck-id");
                        loadDeck(4, deckId, deckInput.value);
                    }
                });
                // input loses focus
                deckInput.addEventListener("blur", function() {
                    const deckId = deckInput.getAttribute("data-deck-id");
                    loadDeck(4, deckId, deckInput.value);
                });
            }
            document.getElementById("deck_navbar").hidden = false
        }}).catch(error => {
            console.error("Error processing response:", error);
        });
}

async function loadDeck(action_id=1, deck_id=null, deck_name="") {
    let data = {"action_id": action_id, "deck_id": parseInt(deck_id, 10), "deck_name": deck_name};
    queryDeckBuilder(data)
}


// Parse ISO8601 duration (e.g., "0H:59M:30S") into total seconds
function parseISODuration(duration) {
    const match = duration.match(/(\d+)H:(\d+)M:(\d+)S/);
    if (match) {
        const hours = parseInt(match[1], 10);
        const minutes = parseInt(match[2], 10);
        const seconds = parseInt(match[3], 10);
        return hours * 3600 + minutes * 60 + seconds;
    }
    return 0;
}
let isCountdownRunning = false; // Flag to track if the countdown is running
function startCountdown() {
    if (isCountdownRunning) return; // Prevent multiple timers
    isCountdownRunning = true;

    const button = document.getElementById("generate_pack_button");
    function updateTimer() {
        const endTime = parseInt(button.getAttribute("data-end-time"), 10); // Retrieve end time
        const now = Date.now();
        const remaining = Math.max(0, Math.floor((endTime - now) / 1000));

        const hours = Math.floor(remaining / 3600);
        const minutes = Math.floor((remaining % 3600) / 60);
        const seconds = remaining % 60;

        button.innerHTML = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
        if (remaining > 0) {
            setTimeout(updateTimer, 1000);
        } else {
            button.innerHTML = "Open Pack";
            isCountdownRunning = false; // Reset the flag when the countdown ends
        }
    }

    updateTimer();
}

async function applySortFilter(filter_str) {
    let data = {
        "set_name": document.getElementById("primary_card_set_title").innerText,
        "filter_str": filter_str,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "filter_ownership": document.getElementById("filter_ownership").textContent
    };
    queryDB(data)
    updateSpanText("sort_by_selected_item", filter_str)
}
async function generatePackButton() {
    let set_name = document.getElementById("primary_card_set_title").innerText
    let data = {
        "set_name": set_name
    };
    cookieManager.set("set_name", set_name);
    let response = await fetch("/generate_pack", {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    }).then(response => {
        const contentType = response.headers.get("Content-Type");
        if (contentType && contentType.includes("application/json")) {
            return response.json(); // Parse JSON if the response is JSON
        } else if (contentType && contentType.includes("text/html")) {
            return response.text(); // Parse text if the response is HTML
        } else {
            throw new Error("Unsupported content type: " + contentType);
        }
    }).then(content => {
        if (typeof content === "object") {
            // Handle JSON content
            console.log("JSON response:", content);
            const button = document.getElementById("generate_pack_button");
            button.setAttribute("data-end-time", content["next_allowed_time"]); // Store end time in a data attribute
            startCountdown();
        } else {
            const gifImage = document.createElement('img');
            gifImage.src = '/static/pack_opening.gif';
            const dynamicContent = document.getElementById("card_container");
            dynamicContent.innerHTML = ""
            dynamicContent.appendChild(gifImage);
            setTimeout(() => {dynamicContent.innerHTML = content;}, 2000);
        }
    }).catch(error => {
        console.error("Error processing response:", error);
    });
}
async function applySearchTerm() {
    let data = {
        "set_name": document.getElementById("primary_card_set_title").innerText,
        "filter_str": document.getElementById("sort_by_selected_item").textContent,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "filter_ownership": document.getElementById("filter_ownership").textContent
    };
    queryDB(data)
}
async function applyFilterOwnership(filter_ownership) {
    let data = {
        "set_name": document.getElementById("primary_card_set_title").innerText,
        "filter_str": document.getElementById("sort_by_selected_item").textContent,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "filter_ownership": filter_ownership
    };
    updateSpanText("filter_ownership", filter_ownership)
    queryDB(data)
}
async function getSetCardList(set_name) {
    cookieManager.set("set_name", set_name);
    let data = {
        "set_name": set_name,
        "filter_str": document.getElementById("sort_by_selected_item").textContent,
        "card_name_search_query": document.getElementById("card_name_search_query_text_field").value,
        "filter_ownership": document.getElementById("filter_ownership").textContent
    };
    queryDB(data)
    document.getElementById("primary_card_set_title").textContent = set_name;
};

document.addEventListener("DOMContentLoaded", function(event){
    let set_name = cookieManager.get("set_name");
    if (set_name === null) {
        set_name = "Base Set (Shadowless)"
    }
    document.getElementById("primary_card_set_title").innerText = set_name

    if (window.location.pathname === "/editor") {
        load_set(set_name)
    } else {
        let data = {
            "set_name": set_name,
            "filter_str": document.getElementById("sort_by_selected_item").textContent,
            "card_name_search_query": "",
            "filter_ownership": ""
        };

        var open_deck_builder_button = document.getElementById("open_deck_builder_button");
        if (open_deck_builder_button !== null)
        {
            open_deck_builder_button.addEventListener("click", function(e) {
                let deck_navbar = document.getElementById("deck_navbar")
                if (deck_navbar.hidden) {
                    loadDeck();
                } else {
                    deck_navbar.hidden = true
                }
            });
        }

        document.addEventListener("click", function(event) {
            if (event.target.tagName === "IMG") {
                handleImageClick(event.target);
            }
        });
    //    loadDeck();

        console.log(data)
        queryDB(data)
        startCountdown();
    }
});
