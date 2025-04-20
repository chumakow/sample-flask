const form = document.querySelector("#form");
form.addEventListener("submit", function (e) {
    e.preventDefault();;
    getOutput();
    setTimeout(updateOutputBoxes, 5000);   // update current prompt and message history; wait long enough for output to feed through
});

const second_form = document.querySelector("#second_form");
second_form.addEventListener("submit", function (e) {
    e.preventDefault();
    updatePrompt();
    updateOutputBoxes();    // update current prompt and message history
});

//function fillLlmOutput(incoming_text) {
//    document.getElementById("output_box").textContent = incoming_text;
//};

function getOutput() {
    const query = form.elements.query.value;
    fetch("execute", {
            method: "POST",
            headers: {
            "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                query: query
            })
        })
        .then((response) => response.json())
        .then(data => {
            const output = data.output;
            console.log(output);
            //const output_box = document.querySelector(".output_box");   // selecting container thing declared above
            document.getElementById("llm_output").textContent = output
        })
}

function updatePrompt() {
    const prompt = second_form.elements.prompt.value;
    fetch("update", {
            method: "POST",
            headers: {
            "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                prompt: prompt
            })
        })
        .then((response) => response.json())
        .then(data => {
            const output = data.output;
            console.log("updating");
            //const output_box = document.querySelector(".output_box");   // selecting container thing declared above
            //document.getElementById("llm_output").textContent = output
        })
}

// Enable form submit on Enter (without Shift) in textarea
document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('query-input');
    var form = document.getElementById('form');
    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        form.requestSubmit();
        }
        });
    });

document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('prompt-input');
    var form = document.getElementById('second_form');
    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        form.requestSubmit();
        }
        });
    });


// Reset button
document.querySelector('#second_form button[type="button"]').onclick = function() {
    fetch('/reset', {method: 'POST'})
      .then(response => response.json())
      .then(data => {
          // Optionally, reload the page or show a message
          window.location.reload();
      });
    sessionStorage.clear();     // trying to clear cache etc
};

// Get current prompt and message history
function updateOutputBoxes() {
    fetch('/get_vars')
        .then(response => response.json())
        .then(data => {
            document.getElementById('current_prompt_box').textContent = data.current_prompt;
            document.getElementById('message_history_box').textContent = data.message_history;
        });
}

    // Update on initial page load
document.addEventListener('DOMContentLoaded', updateOutputBoxes);
