const form = document.querySelector("#form");
form.addEventListener("submit", function (e) {
    e.preventDefault();
    getOutput();
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
            document.getElementById("output_box").textContent = output
        })
}