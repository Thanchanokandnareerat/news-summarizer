function summarizeNews() {
    let url = document.getElementById("newsUrl").value;
    
    fetch("/summarize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("summary").innerText = data.summary || "No summary available.";
        document.getElementById("summary_translation").innerText = data.summary_translation || "No summary translation available.";
        
        document.getElementById("full_text").innerText = data.full_text || "No full text available.";
        document.getElementById("full_translation").innerText = data.full_translation || "No full translation available.";

        let vocabList = document.getElementById("vocabulary");
        vocabList.innerHTML = "";
        for (const [word, translation] of Object.entries(data.vocabulary || {})) {
            let li = document.createElement("li");
            li.innerText = `${word} - ${translation}`;
            vocabList.appendChild(li);
        }
    })
    .catch(error => console.error("Error:", error));
}
