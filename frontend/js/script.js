const predictButton = document.querySelector('.predict-button');
const statusText = document.querySelector('.status-text');
const resultTitle = document.querySelector('.result-title');
const confidenceValue = document.querySelector('.confidence-value');
const resultDescription = document.querySelector('.result-description');
const topList = document.querySelector('.top-list');

const inputs = {
  nitrogen: document.querySelector('#nitrogen'),
  phosphorus: document.querySelector('#phosphorus'),
  potassium: document.querySelector('#potassium'),
  ph: document.querySelector('#ph'),
  temperature: document.querySelector('#temperature'),
  humidity: document.querySelector('#humidity'),
  rainfall: document.querySelector('#rainfall')
};

const setLoading = (loading) => {
  predictButton.disabled = loading;
  predictButton.textContent = loading ? 'Predicting...' : 'Predict Best Crop';
  statusText.textContent = loading ? 'Analyzing the crop conditions...' : '';
};

const updateResult = (data) => {
  resultTitle.textContent = data.recommended_crop;
  confidenceValue.textContent = `${data.confidence_score}%`;
  resultDescription.textContent = data.message || 'This recommendation is based on your submitted soil and weather values.';
  topList.innerHTML = '';
  data.top_3_predictions.forEach((prediction, index) => {
    const item = document.createElement('span');
    item.textContent = `${index + 1}. ${prediction}`;
    topList.appendChild(item);
  });
};

predictButton.addEventListener('click', async () => {
  setLoading(true);

  const payload = {
    nitrogen: Number(inputs.nitrogen.value),
    phosphorus: Number(inputs.phosphorus.value),
    potassium: Number(inputs.potassium.value),
    ph: Number(inputs.ph.value),
    temperature: Number(inputs.temperature.value),
    humidity: Number(inputs.humidity.value),
    rainfall: Number(inputs.rainfall.value)
  };

  try {
    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error('Prediction request failed');
    }

    const data = await response.json();
    updateResult(data);
    statusText.textContent = 'Prediction completed successfully.';
  } catch (error) {
    statusText.textContent = 'Unable to get prediction. Please try again.';
    console.error(error);
  } finally {
    setLoading(false);
  }
});
