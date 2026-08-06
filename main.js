document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("resumeFile");
  const dropzone = document.getElementById("dropzone");
  const fileBadge = document.getElementById("selectedFileBadge");
  const jobDescriptionInput = document.getElementById("jobDescription");
  
  const btnAnalyze = document.getElementById("btnAnalyze");
  const btnSample = document.getElementById("btnSample");
  
  const loadingSpinner = document.getElementById("loadingSpinner");
  const resultsSection = document.getElementById("resultsSection");

  // Drag & Drop handlers
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'), false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'), false);
  });

  dropzone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
      fileInput.files = files;
      updateFileBadge(files[0].name);
    }
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      updateFileBadge(fileInput.files[0].name);
    }
  });

  function updateFileBadge(filename) {
    fileBadge.textContent = `Selected: ${filename}`;
    fileBadge.style.display = 'inline-block';
  }

  // Analyze Action
  btnAnalyze.addEventListener("click", async () => {
    if (!fileInput.files || fileInput.files.length === 0) {
      alert("Please select a resume file (PDF, DOCX, or TXT) first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("job_description", jobDescriptionInput.value.trim());

    await sendAnalysisRequest("/api/review", formData);
  });

  // Sample Resume Action
  btnSample.addEventListener("click", async () => {
    await sendAnalysisRequest("/api/sample", null, "GET");
  });

  async function sendAnalysisRequest(url, bodyData = null, method = "POST") {
    // Show spinner & hide previous results
    resultsSection.style.display = "none";
    loadingSpinner.style.display = "block";

    try {
      const options = { method: method };
      if (bodyData) {
        options.body = bodyData;
      }

      const response = await fetch(url, options);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Error processing request.");
      }

      renderResults(data);

    } catch (err) {
      alert(`Error: ${err.message}`);
    } finally {
      loadingSpinner.style.display = "none";
    }
  }

  function renderResults(data) {
    resultsSection.style.display = "block";
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    const ats = data.ats_analysis;
    const meta = data.metadata;

    // 1. Render ATS Circular Gauge
    const scoreVal = ats.overall_ats_score;
    document.getElementById("scoreNumber").textContent = Math.round(scoreVal);
    
    // Gauge SVG dashoffset logic (full circumference ~ 440)
    const gaugeFill = document.getElementById("gaugeFill");
    const offset = 440 - (440 * (scoreVal / 100));
    setTimeout(() => {
      gaugeFill.style.strokeDashoffset = offset;
    }, 100);

    // 2. Metadata Info
    document.getElementById("metaWordCount").textContent = meta.word_count || "N/A";
    document.getElementById("metaEmail").textContent = meta.email || "Not found";
    document.getElementById("metaPhone").textContent = meta.phone || "Not found";

    // 3. Sub-scores Progress Bars
    setProgressBar("barContentMatch", "valContentMatch", ats.sub_scores.content_match);
    setProgressBar("barSkillsAlign", "valSkillsAlign", ats.sub_scores.skills_alignment);
    setProgressBar("barStructure", "valStructure", ats.sub_scores.section_structure);
    setProgressBar("barActionVerbs", "valActionVerbs", ats.sub_scores.action_oriented);

    // 4. Render Skills (Matched vs Missing)
    const matchedContainer = document.getElementById("matchedSkillsContainer");
    matchedContainer.innerHTML = "";
    if (ats.matched_skills && ats.matched_skills.length > 0) {
      ats.matched_skills.forEach(skill => {
        matchedContainer.appendChild(createBadge(skill, "tag-matched", "fa-check-circle"));
      });
    } else {
      matchedContainer.innerHTML = "<span class='text-muted' style='font-size:0.85rem;'>No explicit matched job skills detected.</span>";
    }

    const missingContainer = document.getElementById("missingSkillsContainer");
    missingContainer.innerHTML = "";
    if (ats.missing_skills && ats.missing_skills.length > 0) {
      ats.missing_skills.forEach(skill => {
        missingContainer.appendChild(createBadge(skill, "tag-missing", "fa-exclamation-triangle"));
      });
    } else {
      missingContainer.innerHTML = "<span class='text-muted' style='font-size:0.85rem;'>No critical skill gaps detected!</span>";
    }

    const detectedSkillsContainer = document.getElementById("detectedSkillsContainer");
    detectedSkillsContainer.innerHTML = "";
    const allExtracted = ats.skills_extracted._all || [];
    allExtracted.forEach(skill => {
      detectedSkillsContainer.appendChild(createBadge(skill, "tag-neutral", "fa-code"));
    });

    // 5. Render Suggestions
    const suggestionsContainer = document.getElementById("suggestionsContainer");
    suggestionsContainer.innerHTML = "";
    ats.suggestions.forEach(item => {
      const li = document.createElement("li");
      li.className = "suggestion-item";
      li.innerHTML = `<i class="fas fa-lightbulb"></i> <span>${item}</span>`;
      suggestionsContainer.appendChild(li);
    });

    // 6. Render Career Recommendations
    const recGrid = document.getElementById("recommendationsGrid");
    recGrid.innerHTML = "";
    data.recommendations.forEach(rec => {
      const card = document.createElement("div");
      card.className = "rec-card";
      card.innerHTML = `
        <div>
          <div class="rec-header">
            <div class="rec-title">${rec.title}</div>
            <span class="rec-match-pill">${rec.match_percentage}% Match</span>
          </div>
          <p class="rec-desc">${rec.description}</p>
          <div style="font-size: 0.8rem; margin-bottom: 8px; color: var(--text-muted);">
            <strong>Matching Skills:</strong> ${rec.matching_skills.join(", ") || "None"}
          </div>
          <div style="font-size: 0.8rem; color: #f87171;">
            <strong>To Learn:</strong> ${rec.missing_skills_to_learn.join(", ") || "None"}
          </div>
        </div>
      `;
      recGrid.appendChild(card);
    });
  }

  function setProgressBar(barId, valId, value) {
    const bar = document.getElementById(barId);
    const valText = document.getElementById(valId);
    if (bar && valText) {
      valText.textContent = `${Math.round(value)}%`;
      setTimeout(() => {
        bar.style.width = `${Math.round(value)}%`;
      }, 150);
    }
  }

  function createBadge(text, className, iconClass) {
    const span = document.createElement("span");
    span.className = `tag ${className}`;
    span.innerHTML = `<i class="fas ${iconClass}"></i> ${text}`;
    return span;
  }
});
