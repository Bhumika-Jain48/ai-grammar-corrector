async function correctText() {

    const text =
        document.getElementById("text").value;

    if (!text.trim()) {
        alert("Please enter text");
        return;
    }

    document.getElementById("loading")
        .innerText = "Correcting...";

    document.getElementById("result")
        .innerText = "";

    document.getElementById("explanation")
        .innerText = "";

    try {

        const response =
            await fetch("/correct", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text
                })
            });

        const data =
            await response.json();

        document.getElementById("loading")
            .innerText = "";

        if (data.error) {

            document.getElementById("result")
                .innerText = data.error;

            return;
        }

        document.getElementById("result")
            .innerText =
            data.corrected_text;

        document.getElementById("explanation")
            .innerText =
            data.explanation;

    }
    catch (error) {

        document.getElementById("loading")
            .innerText = "";

        document.getElementById("result")
            .innerText =
            "Something went wrong.";
    }
}


function copyResult() {

    navigator.clipboard.writeText(
        document.getElementById("result")
            .innerText
    );

    alert("Copied!");
}