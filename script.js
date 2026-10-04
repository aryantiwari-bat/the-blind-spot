const $ = (id) => document.getElementById(id);

const exampleDecision = "Should I accept a 6-month internship?";
const exampleReasoning =
  "The stipend is good, the company is close to home, and it will give me industry experience.";

$("exampleBtn").addEventListener("click", () => {
  $("decision").value = exampleDecision;
  $("reasoning").value = exampleReasoning;
  $("status").textContent = "Example loaded. Click Analyze My Blind Spots.";
});

function renderList(id, items) {
  const el = $(id);
  el.innerHTML = "";
  (Array.isArray(items) ? items : []).forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    el.appendChild(li);
  });
}

$("analyzeBtn").addEventListener("click", async () => {
  const decision = $("decision").value.trim();
  const reasoning = $("reasoning").value.trim();

  if (!decision || !reasoning) {
    $("status").textContent = "Please enter both the decision and your reasoning.";
    return;
  }

  $("analyzeBtn").disabled = true;
  $("status").textContent = "Analyzing your reasoning...";
  $("results").classList.add("hidden");

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision, reasoning })
    });

    const data = await response.json();

    if (!response.ok) throw new Error(data.error || "Something went wrong.");

    $("summary").textContent = data.summary || "";
    renderList("blind_spots", data.blind_spots);
    renderList("assumptions", data.assumptions);
    renderList("questions", data.questions);
    renderList("conflicts", data.conflicts);
    renderList("verify", data.verify);

    $("results").classList.remove("hidden");
    $("status").textContent = "Analysis complete.";
    $("results").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    $("status").textContent = error.message;
  } finally {
    $("analyzeBtn").disabled = false;
  }
});
