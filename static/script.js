const input = document.getElementById("command");
const output = document.getElementById("output");

input.addEventListener("keydown", async function(e) {
    if (e.key === "Enter") {
        const cmd = input.value;
        output.innerHTML += "$ " + cmd + "\n";
        input.value = "";

        const res = await fetch("/command", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({command: cmd})
        });

        const data = await res.json();
        output.innerHTML += data.output + "\n";
        output.scrollTop = output.scrollHeight;
    }
});
