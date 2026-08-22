// Frontend interactions for the crop recommendation experience.
const form = document.getElementById('prediction-form-element');
const predictButton = document.getElementById('predict-btn');
const resetButton = document.getElementById('reset-btn');
const resultCard = document.getElementById('result-card');
const resultCrop = document.getElementById('result-crop');
const resultMessage = document.getElementById('result-message');
const resultConfidence = document.getElementById('result-confidence');
const statusMessage = document.getElementById('status-message');
const themeToggle = document.querySelector('[data-theme-toggle]');
const themeIcon = document.querySelector('.theme-icon');
const themeText = document.querySelector('.theme-text');
const diseaseForm = document.getElementById('disease-form');
const diseaseFile = document.getElementById('disease-file');
const uploadZone = document.getElementById('upload-zone');
const imagePreviewWrap = document.getElementById('image-preview-wrap');
const diseasePreview = document.getElementById('disease-preview');
const replaceImageButton = document.getElementById('replace-image-btn');
const removeImageButton = document.getElementById('remove-image-btn');
const analyzeDiseaseButton = document.getElementById('analyze-disease-btn');
const diseaseResult = document.getElementById('disease-result');
const diseaseResultTitle = document.getElementById('disease-result-title');
const diseaseResultMessage = document.getElementById('disease-result-message');
const diseaseStatus = document.getElementById('disease-status');

const STORAGE_KEY = 'ai-crop-theme';

// Apply the selected theme and persist it in local storage.
function setTheme(theme) {
  document.body.setAttribute('data-theme', theme);
  const isDark = theme === 'dark';
  themeIcon.textContent = isDark ? '☀️' : '🌙';
  themeText.textContent = isDark ? 'Light' : 'Dark';
  localStorage.setItem(STORAGE_KEY, theme);
}

function initializeTheme() {
  const savedTheme = localStorage.getItem(STORAGE_KEY);
  const preferredTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  setTheme(savedTheme || preferredTheme);
}

function showStatus(message, type = '') {
  statusMessage.textContent = message;
  statusMessage.className = `status-message ${type}`.trim();
}

function showDiseaseStatus(message, type = '') {
  diseaseStatus.textContent = message;
  diseaseStatus.className = `status-message ${type}`.trim();
}

function setLoading(isLoading) {
  predictButton.disabled = isLoading;
  predictButton.classList.toggle('is-loading', isLoading);
}

// Validate the form inputs before submitting them.
function validateInputs() {
  const fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall'];
  const values = {};

  for (const field of fields) {
    const input = document.getElementById(field);
    const value = input.value.trim();

    if (!value) {
      showStatus(`Please fill in ${field}.`, 'error');
      input.focus();
      return null;
    }

    const numericValue = Number(value);
    if (Number.isNaN(numericValue)) {
      showStatus(`Please enter a valid number for ${field}.`, 'error');
      input.focus();
      return null;
    }

    values[field] = numericValue;
  }

  return values;
}

// Send the prediction payload to the connected FastAPI endpoint.
async function predictCrop(payload) {
  const response = await fetch('/api/crop/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error?.message || errorData.detail || 'Prediction request failed.');
  }

  return response.json();
}

let selectedDiseaseFile = null;
let previewUrl = null;

function setDiseaseFile(file) {
  if (!file) {
    return;
  }

  const supportedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!supportedTypes.includes(file.type)) {
    showDiseaseStatus('Please choose a JPEG, PNG, or WebP image.', 'error');
    return;
  }

  selectedDiseaseFile = file;
  if (previewUrl) {
    URL.revokeObjectURL(previewUrl);
  }
  previewUrl = URL.createObjectURL(file);
  diseasePreview.src = previewUrl;
  uploadZone.classList.add('hidden');
  imagePreviewWrap.classList.remove('hidden');
  analyzeDiseaseButton.disabled = false;
  diseaseResult.classList.add('hidden');
  showDiseaseStatus('Image ready for analysis.');
}

function clearDiseaseFile() {
  selectedDiseaseFile = null;
  diseaseFile.value = '';
  if (previewUrl) {
    URL.revokeObjectURL(previewUrl);
    previewUrl = null;
  }
  diseasePreview.removeAttribute('src');
  uploadZone.classList.remove('hidden');
  imagePreviewWrap.classList.add('hidden');
  analyzeDiseaseButton.disabled = true;
  diseaseResult.classList.add('hidden');
  showDiseaseStatus('');
}

async function analyzeDisease() {
  const response = await fetch('/api/disease/predict', {
    method: 'POST',
    body: (() => {
      const formData = new FormData();
      formData.append('file', selectedDiseaseFile);
      return formData;
    })()
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error?.message || 'Disease analysis request failed.');
  }
  return data;
}

diseaseFile.addEventListener('change', () => setDiseaseFile(diseaseFile.files[0]));
replaceImageButton.addEventListener('click', () => diseaseFile.click());
removeImageButton.addEventListener('click', clearDiseaseFile);

['dragenter', 'dragover'].forEach((eventName) => {
  uploadZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    uploadZone.classList.add('is-dragging');
  });
});

['dragleave', 'drop'].forEach((eventName) => {
  uploadZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    uploadZone.classList.remove('is-dragging');
  });
});

uploadZone.addEventListener('drop', (event) => setDiseaseFile(event.dataTransfer.files[0]));

diseaseForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!selectedDiseaseFile) {
    showDiseaseStatus('Choose an image before analyzing.', 'error');
    return;
  }

  analyzeDiseaseButton.disabled = true;
  analyzeDiseaseButton.classList.add('is-loading');
  showDiseaseStatus('Analyzing plant image…');

  try {
    const data = await analyzeDisease();
    diseaseResultTitle.textContent = data.model_available ? data.disease : 'Analysis unavailable';
    diseaseResultMessage.textContent = data.model_available
      ? data.recommendation || 'Disease analysis complete.'
      : data.error?.message || 'Disease analysis model is not available yet.';
    diseaseResult.classList.remove('hidden');
    showDiseaseStatus(data.model_available ? 'Analysis completed successfully.' : 'Model unavailable.', data.model_available ? 'success' : 'error');
  } catch (error) {
    diseaseResult.classList.add('hidden');
    showDiseaseStatus(error.message || 'Disease analysis failed. Please try again.', 'error');
  } finally {
    analyzeDiseaseButton.disabled = false;
    analyzeDiseaseButton.classList.remove('is-loading');
  }
});

function resetResult() {
  resultCard.classList.add('hidden');
  resultCrop.textContent = '—';
  resultMessage.textContent = 'Waiting for analysis.';
  resultConfidence.textContent = 'Confidence: —';
  showStatus('');
}

// Handle prediction submission and display the result card.
form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = validateInputs();
  if (!payload) {
    return;
  }

  setLoading(true);
  showStatus('Analyzing field conditions…');

  try {
    const data = await predictCrop({
      nitrogen: payload.nitrogen,
      phosphorus: payload.phosphorus,
      potassium: payload.potassium,
      temperature: payload.temperature,
      humidity: payload.humidity,
      ph: payload.ph,
      rainfall: payload.rainfall
    });

    resultCrop.textContent = data.recommended_crop;
    resultMessage.textContent = data.message || 'Recommendation ready.';
    resultConfidence.textContent = `Confidence: ${data.confidence_score}%`;
    resultCard.classList.remove('hidden');
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
    showStatus('Prediction completed successfully.', 'success');
  } catch (error) {
    showStatus(error.message || 'Prediction failed. Please try again.', 'error');
  } finally {
    setLoading(false);
  }
});

resetButton.addEventListener('click', () => {
  form.reset();
  resetResult();
  const firstInput = document.querySelector('input');
  firstInput?.focus();
});

themeToggle.addEventListener('click', () => {
  const currentTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  setTheme(currentTheme);
});

initializeTheme();
resetResult();
clearDiseaseFile();
