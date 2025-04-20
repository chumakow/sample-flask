const form = document.querySelector("#form");
form.addEventListener("submit", function (e) {
    e.preventDefault();
    console.log("Hello, World!");
    getOutput();
});

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
